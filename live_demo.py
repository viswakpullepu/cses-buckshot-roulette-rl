"""
CSES Buckshot Roulette - Live Tournament CLI Visualizer
Engineered for NIT Warangal CSES Arcade RL Hackathon.
Demonstrates bot decision-making, Bayesian probability tracking, and step-by-step game actions.
Supports 2 to 4 bots in multi-player battle royale and multi-match tournament benchmarking.
"""
import sys
import os
import time
import argparse
import random
import importlib.util
import inspect

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add repo to python path
ROOT = os.path.dirname(os.path.abspath(__file__))
if os.path.exists(os.path.join(ROOT, "game_API.py")):
    sys.path.insert(0, ROOT)
elif os.path.exists(os.path.join(ROOT, "repo", "game_API.py")):
    ROOT = os.path.join(ROOT, "repo")
    sys.path.insert(0, ROOT)

import game_API
from schemas import (
    Stage,
    ActionType,
    UpgradeType,
    NextRound,
    Action_PLAY,
    Action_PICK_UPGRADES,
)

# ANSI Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"
MAGENTA = "\033[95m"
BLUE = "\033[94m"

PLAYER_COLORS = [CYAN, YELLOW, MAGENTA, GREEN]


def load_bot_instance(target_path: str, seed: int = 42):
    """Loads a bot class from a directory containing bot.py or directly from a .py file."""
    # Resolve path
    if not os.path.exists(target_path):
        alt = os.path.join(ROOT, target_path)
        if os.path.exists(alt):
            target_path = alt
        else:
            alt2 = os.path.join(ROOT, "bots", target_path)
            if os.path.exists(alt2):
                target_path = alt2

    if os.path.isdir(target_path):
        py_file = os.path.join(target_path, "bot.py")
        params_file = os.path.join(target_path, "params.json")
    else:
        py_file = target_path
        params_file = os.path.join(os.path.dirname(target_path), "params.json")

    if not os.path.exists(py_file):
        raise FileNotFoundError(f"Bot script not found: {target_path} (looked for {py_file})")

    params = {"seed": seed}
    if os.path.exists(params_file):
        try:
            import json
            with open(params_file, "r") as f:
                params.update(json.load(f))
        except Exception:
            pass

    mod_name = f"bot_{abs(hash(py_file))}_{random.randint(1000, 999999)}"
    spec = importlib.util.spec_from_file_location(mod_name, py_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, "Bot"):
        raise AttributeError(f"Module {py_file} does not define a 'Bot' class.")

    try:
        bot = module.Bot()
    except TypeError:
        bot = module.Bot(params)

    init_fn = getattr(bot, "init", None)
    if callable(init_fn):
        sig = inspect.signature(init_fn)
        if len(sig.parameters) > 0:
            init_fn(params)
        else:
            init_fn()

    return bot


def render_hp_bar(health: int, max_health: int = 5) -> str:
    filled = max(0, min(health, max_health))
    empty = max_health - filled
    color = GREEN if filled >= 4 else (YELLOW if filled >= 2 else RED)
    bar = f"{color}{'█' * filled}{DIM}{'░' * empty}{RESET} ({health}/{max_health} HP)"
    return bar


def render_inventory(upgrades) -> str:
    items = []
    if upgrades.juice > 0:
        items.append(f"🧃 Juice x{upgrades.juice}")
    if upgrades.mag_glass > 0:
        items.append(f"🔍 MagGlass x{upgrades.mag_glass}")
    if upgrades.hand_saw > 0:
        items.append(f"🪚 Saw x{upgrades.hand_saw}")
    if upgrades.pool_floatie > 0:
        items.append(f"🛟 Floatie x{upgrades.pool_floatie}")
    if upgrades.coffee > 0:
        items.append(f"☕ Coffee x{upgrades.coffee}")
    return " | ".join(items) if items else f"{DIM}(empty){RESET}"


def play_single_match(bot_paths: list, seed: int, delay: float = 0.25, step_mode: bool = False, verbose: bool = True):
    num_players = len(bot_paths)
    names = [os.path.basename(os.path.normpath(p)) for p in bot_paths]
    bots = [load_bot_instance(p, seed=seed + i * 17) for i, p in enumerate(bot_paths)]
    colored_names = [f"{PLAYER_COLORS[i % len(PLAYER_COLORS)]}{BOLD}{names[i]} (P{i}){RESET}" for i in range(num_players)]

    if verbose:
        print("\n" + "=" * 75)
        print(f"       🎮 {BOLD}CSES BUCKSHOT ROULETTE - LIVE TOURNAMENT MATCH{RESET} 🎮")
        print("=" * 75)
        print(f"Match Seed: {seed}")
        for i, name in enumerate(names):
            role = "Our Champion" if i == 0 else f"Opponent {i}"
            print(f"Player {i}:   {name} ({role})")
        print("=" * 75 + "\n")

    state = game_API.initGame(seed, num_players=num_players)

    step_num = 0
    current_session = -1

    while not state.game_over:
        if state.session_no != current_session and state.stage == Stage.PLAY:
            current_session = state.session_no
            if verbose:
                print("\n" + "─" * 75)
                print(f"🔔 {BOLD}SESSION {current_session + 1} BEGINS{RESET}")
                print(f"   Gun Chamber Loaded with {BOLD}{state.rounds_remaining} Shells{RESET}: "
                      f"{RED}{state.lives_init} Live (💥){RESET} | {BLUE}{state.blanks_init} Blank (💨){RESET}")
                print("─" * 75)

        turn = state.turn
        current_bot = bots[turn]
        current_name = colored_names[turn]

        # STAGE: PICK UPGRADE
        if state.stage == Stage.PICK_UPGRADE:
            obs = game_API.upgrade_observation(state)
            action = current_bot.pick_upgrade(obs)
            chosen_up = action.chosen_upgrade.name if hasattr(action.chosen_upgrade, "name") else str(action.chosen_upgrade)
            if verbose:
                print(f"🎁 {current_name} drafts upgrade: {BOLD}{chosen_up}{RESET}")
            game_API.step_PICK_UPGRADE(state, action)
            if delay > 0 and verbose:
                time.sleep(delay * 0.4)
            continue

        # STAGE: PLAY TURN
        step_num += 1
        obs = game_API.play_observation(state)

        if verbose:
            print(f"\n[{BOLD}STEP {step_num}{RESET}] Turn: {current_name}")
            for idx, p in enumerate(state.players):
                status = " [FLOATIE ON]" if p.has_pool_floatie_on else ""
                dead = f" {RED}{BOLD}[ELIMINATED]{RESET}" if p.health <= 0 else ""
                print(f"   P{idx} ({names[idx]}): {render_hp_bar(p.health)} | Items: {render_inventory(p.upgrades)}{status}{dead}")
            print(f"   Gun Status: {state.rounds_remaining} shells in chamber | Shot: {state.lives_shot} Live, {state.blanks_shot} Blank")

            if hasattr(current_bot, "_get_shell_counts"):
                try:
                    max_l, min_l, max_b, min_b, p_live, p_blank = current_bot._get_shell_counts(obs)
                    next_info = obs.next_round.name
                    print(f"   🧠 {DIM}[Cognitive Reasoning]{RESET} Chamber Est: "
                          f"{RED}P(Live)={p_live*100:.1f}%{RESET}, {BLUE}P(Blank)={p_blank*100:.1f}%{RESET} | "
                          f"Inspected: {BOLD}{next_info}{RESET}")
                except Exception:
                    pass

        action = current_bot.play(obs)

        if hasattr(current_bot, "last_q_values") and current_bot.last_q_values is not None and verbose:
            ACTION_NAMES = ["JUICE", "FLOATIE", "MAG_GLASS", "COFFEE", "SAW", "SHOOT_SELF", "SHOOT_OPP"]
            top_q = " | ".join(f"{ACTION_NAMES[i]}:{current_bot.last_q_values[i]:+.1f}" for i in range(len(ACTION_NAMES)))
            print(f"   🤖 {MAGENTA}[Deep Q-Network Inference]{RESET} Forward Pass Evaluated:")
            print(f"      Q(s, a): {DIM}[{top_q}]{RESET}")
            print(f"      Action Policy: {GREEN}{BOLD}argmax(Q) -> {current_bot.last_selected_action_name}{RESET}")

        if step_mode and verbose:
            input(f"{DIM}Press [Enter] to execute action...{RESET}")
        elif delay > 0 and verbose:
            time.sleep(delay)

        if action.action == ActionType.USE_UPGRADE:
            up_name = action.useUpgrade.name if hasattr(action.useUpgrade, "name") else str(action.useUpgrade)
            target_str = f" on Player {action.target}" if action.target is not None else ""
            if verbose:
                print(f"   ⚡ {BOLD}ACTION: USE ITEM{RESET} -> {BOLD}{up_name}{RESET}{target_str}")
                if action.useUpgrade == UpgradeType.JUICE:
                    print(f"      🧃 Restores +1 HP!")
                elif action.useUpgrade == UpgradeType.MAG_GLASS:
                    shell_idx = len(state.round_contents) - state.rounds_remaining
                    real_is_live = state.round_contents[shell_idx]
                    print(f"      🔍 Looked into chamber -> {BOLD}{'LIVE 💥' if real_is_live else 'BLANK 💨'}{RESET} discovered!")
                elif action.useUpgrade == UpgradeType.HAND_SAW:
                    print(f"      🪚 Hand Saw applied! Next live shot damage increased to {state.damage + 1}!")
                elif action.useUpgrade == UpgradeType.POOL_FLOATIE:
                    print(f"      🛟 Target Player {action.target} will SKIP their next play turn!")
                elif action.useUpgrade == UpgradeType.COFFEE:
                    print(f"      ☕ Coffee drank! Shell ejected from gun chamber.")

            game_API.step_PLAY(state, action)
            continue

        elif action.action == ActionType.SHOOT:
            target = action.target
            target_name = "THEMSELF 🎯" if target == turn else f"Opponent (Player {target} - {names[target]})"
            if verbose:
                print(f"   🎯 {BOLD}ACTION: SHOOT{RESET} -> Targeted {BOLD}{target_name}{RESET}")

            shell_idx = len(state.round_contents) - state.rounds_remaining
            is_live = state.round_contents[shell_idx]
            dmg = state.damage

            game_API.step_PLAY(state, action)

            if verbose:
                if is_live:
                    print(f"   💥 {RED}{BOLD}BANG! LIVE ROUND!{RESET} Deals {BOLD}{dmg} DAMAGE{RESET} to Player {target}!")
                else:
                    print(f"   💨 {BLUE}{BOLD}CLICK! BLANK ROUND!{RESET} No damage dealt.")
                    if target == turn:
                        print(f"   🔄 {GREEN}{BOLD}TACTICAL SUCCESS:{RESET} Shot themself with a BLANK -> {BOLD}FREE EXTRA TURN GAINED!{RESET}")

    winner_idx = None
    for i, p in enumerate(state.players):
        if p.health > 0:
            winner_idx = i
            break

    if verbose:
        print("\n" + "=" * 75)
        print(f"                     🏆 {BOLD}MATCH FINISHED!{RESET} 🏆")
        print("=" * 75)
        if winner_idx is not None:
            print(f"🥇 {BOLD}WINNER: Player {winner_idx} ({names[winner_idx]}){RESET}!")
            print(f"   Final Standings:")
            for idx, p in enumerate(state.players):
                print(f"   • Player {idx} ({names[idx]}): {p.health} HP")
            print(f"   Total Actions: {step_num}")
        else:
            print("🤝 Match Draw / Timeout reached.")
        print("=" * 75 + "\n")

    return winner_idx


def main():
    parser = argparse.ArgumentParser(description="Live CLI Match & Tournament Visualizer for CSES Buckshot Roulette")
    parser.add_argument("bots", nargs="*", default=["my_bot", "repo/bots/random_bot"],
                        help="List of 2 to 4 bot paths to compete (e.g. my_bot bot_a bot_b)")
    parser.add_argument("--matches", type=int, default=1, help="Number of matches to play in tournament mode (default: 1)")
    parser.add_argument("--seed", type=int, default=None, help="Fixed random seed (default: random)")
    parser.add_argument("--delay", type=float, default=0.25, help="Delay in seconds between steps (default: 0.25s)")
    parser.add_argument("--step", action="store_true", help="Step-by-step interactive mode (press Enter to advance)")
    args = parser.parse_args()

    bot_paths = args.bots
    if len(bot_paths) < 2:
        bot_paths.append("repo/bots/random_bot")
    if len(bot_paths) > 4:
        print(f"{YELLOW}Warning: Maximum 4 players supported. Truncating to 4 bots.{RESET}")
        bot_paths = bot_paths[:4]

    num_matches = args.matches
    base_seed = args.seed if args.seed is not None else random.randint(10000, 999999)

    if num_matches == 1:
        play_single_match(bot_paths, seed=base_seed, delay=args.delay, step_mode=args.step, verbose=True)
    else:
        print("\n" + "=" * 75)
        print(f"       🏆 {BOLD}CSES BUCKSHOT ROULETTE - TOURNAMENT BENCHMARK{RESET} 🏆")
        print(f"       Running {num_matches} Matches across {len(bot_paths)} Bots")
        print("=" * 75)
        names = [os.path.basename(os.path.normpath(p)) for p in bot_paths]
        wins = {i: 0 for i in range(len(bot_paths))}

        for m in range(num_matches):
            current_seed = base_seed + m * 97
            winner = play_single_match(bot_paths, seed=current_seed, delay=0.0, step_mode=False, verbose=False)
            if winner is not None:
                wins[winner] += 1
            w_name = names[winner] if winner is not None else "Draw"
            print(f"Match {m + 1:2d}/{num_matches}: Winner = {BOLD}{w_name}{RESET} (Seed: {current_seed})")

        print("\n" + "=" * 75)
        print(f"                 📊 {BOLD}FINAL TOURNAMENT SCOREBOARD{RESET} 📊")
        print("=" * 75)
        ranked = sorted(wins.items(), key=lambda x: x[1], reverse=True)
        for rank, (bot_idx, win_count) in enumerate(ranked, 1):
            pct = (win_count / num_matches) * 100
            color = GREEN if rank == 1 else (YELLOW if rank == 2 else RESET)
            seat_label = f"Seat {bot_idx} ({names[bot_idx]})"
            print(f"  Rank #{rank}: {color}{BOLD}{seat_label:<24}{RESET} - {win_count}/{num_matches} Wins ({pct:.1f}%)")
        print("=" * 75 + "\n")


if __name__ == "__main__":
    main()
