import os
import json
from schemas import (
    Action_PLAY,
    Action_PICK_UPGRADES,
    ActionType,
    UpgradeType,
    NextRound,
    Obs_PLAY,
    Obs_PICK_UPGRADES,
)

ACTION_NAMES = [
    "USE_JUICE",
    "USE_POOL_FLOATIE",
    "USE_MAG_GLASS",
    "USE_COFFEE",
    "USE_HAND_SAW",
    "SHOOT_SELF",
    "SHOOT_OPPONENT",
]


class DeepQNetwork:
    """
    Lightweight Multi-Layer Perceptron (18 -> 48 -> 24 -> 7)
    Evaluates Q(s, a) for the 7 actions with zero external dependencies (pure Python standard library).
    Fully compliant with competition limits: < 0.05s per decision, < 128 MB RAM.
    """
    def __init__(self, weights_path: str):
        with open(weights_path, "r") as f:
            weights = json.load(f)
        self.W1 = weights["W1"]  # 48 x 18
        self.b1 = weights["b1"]  # 48
        self.W2 = weights["W2"]  # 24 x 48
        self.b2 = weights["b2"]  # 24
        self.W3 = weights["W3"]  # 7 x 24
        self.b3 = weights["b3"]  # 7

    def predict_q_values(self, state_vec: list[float]) -> list[float]:
        # Layer 1: Linear + ReLU
        h1 = []
        for i in range(len(self.b1)):
            v = sum(self.W1[i][j] * state_vec[j] for j in range(len(state_vec))) + self.b1[i]
            h1.append(max(0.0, v))

        # Layer 2: Linear + ReLU
        h2 = []
        for i in range(len(self.b2)):
            v = sum(self.W2[i][j] * h1[j] for j in range(len(h1))) + self.b2[i]
            h2.append(max(0.0, v))

        # Layer 3: Linear output Q-values
        q = []
        for i in range(len(self.b3)):
            v = sum(self.W3[i][j] * h2[j] for j in range(len(h2))) + self.b3[i]
            q.append(v)

        return q


class Bot:
    def init(self, params=None):
        self.params = params or {}
        self.current_saw_stacked = 0
        self.last_q_values = None
        self.last_state_vec = None
        self.last_selected_action_name = None

        # Load Deep Q-Network weights
        base_dir = os.path.dirname(os.path.abspath(__file__))
        weights_file = os.path.join(base_dir, "model_weights.json")
        self.model = DeepQNetwork(weights_file)

    def _get_shell_counts(self, obs: Obs_PLAY):
        r = obs.rounds_remaining
        if r <= 0:
            return 0, 0, 0, 0, 0.0, 0.0

        if obs.next_round == NextRound.LIVE:
            return 1, 1, 0, 0, 1.0, 0.0
        if obs.next_round == NextRound.BLANK:
            return 0, 0, 1, 1, 0.0, 1.0

        known_lives_removed = obs.lives_shot + obs.ejections.lives_ejected
        known_blanks_removed = obs.blanks_shot + obs.ejections.blanks_ejected
        unknown_ejected = obs.ejections.unknowns_ejected

        max_lives_rem = max(0, obs.lives_init - known_lives_removed)
        max_blanks_rem = max(0, obs.blanks_init - known_blanks_removed)

        min_lives_rem = max(0, max_lives_rem - unknown_ejected)
        min_blanks_rem = max(0, max_blanks_rem - unknown_ejected)

        if max_blanks_rem == 0 or min_lives_rem == r:
            return r, r, 0, 0, 1.0, 0.0
        if max_lives_rem == 0 or min_blanks_rem == r:
            return 0, 0, r, r, 0.0, 1.0

        if unknown_ejected > 0:
            pool = r + unknown_ejected
            exp_lives = max_lives_rem * (r / pool)
        else:
            exp_lives = float(max_lives_rem)

        exp_lives = max(float(min_lives_rem), min(float(max_lives_rem), exp_lives))
        p_live = exp_lives / r
        p_blank = 1.0 - p_live

        return max_lives_rem, min_lives_rem, max_blanks_rem, min_blanks_rem, p_live, p_blank

    def _choose_best_target(self, obs: Obs_PLAY, me: int, damage: int) -> int:
        living = [i for i, p in enumerate(obs.players) if i != me and p.health > 0]
        if not living:
            return me
        if len(living) == 1:
            return living[0]

        # 1. Immediate elimination: Thin the field if lethal
        lethal = [i for i in living if obs.players[i].health <= damage]
        if lethal:
            lethal.sort(key=lambda idx: (obs.players[idx].upgrades.hand_saw * 3 + obs.players[idx].upgrades.pool_floatie * 3, idx), reverse=True)
            return lethal[0]

        # 2. Threat-Weighted Anti-Snowball Targeting:
        # Attack highest HP opponent, tie-breaking on threat score (Hand Saws & Pool Floaties)
        def threat(idx):
            p = obs.players[idx]
            u = p.upgrades
            return (p.health, u.hand_saw * 3 + u.pool_floatie * 2, idx)
        living.sort(key=threat, reverse=True)
        return living[0]

    def extract_state_vector(self, obs: Obs_PLAY) -> list[float]:
        me = obs.turn
        my_p = obs.players[me]
        current_dmg = 1 + self.current_saw_stacked
        target_idx = self._choose_best_target(obs, me, current_dmg)
        opp_p = obs.players[target_idx]

        max_l, min_l, max_b, min_b, p_live, p_blank = self._get_shell_counts(obs)
        nr = obs.next_round

        is_live_certain = 1.0 if (nr == NextRound.LIVE or p_live >= 0.999 or max_b == 0) else 0.0
        is_blank_certain = 1.0 if (nr == NextRound.BLANK or p_blank >= 0.999 or max_l == 0) else 0.0

        alive_count = len([p for p in obs.players if p.health > 0])
        is_lethal = 1.0 if opp_p.health <= current_dmg else 0.0

        return [
            my_p.health / 5.0,
            opp_p.health / 5.0,
            obs.rounds_remaining / 8.0,
            p_live,
            p_blank,
            is_live_certain,
            is_blank_certain,
            my_p.upgrades.juice / 3.0,
            my_p.upgrades.mag_glass / 2.0,
            my_p.upgrades.hand_saw / 3.0,
            my_p.upgrades.pool_floatie / 2.0,
            my_p.upgrades.coffee / 2.0,
            1.0 if opp_p.has_pool_floatie_on else 0.0,
            opp_p.upgrades.mag_glass / 2.0,
            opp_p.upgrades.hand_saw / 2.0,
            self.current_saw_stacked / 3.0,
            alive_count / 4.0,
            is_lethal,
        ]

    def play(self, obs: Obs_PLAY) -> Action_PLAY:
        me = obs.turn
        my_p = obs.players[me]
        my_up = my_p.upgrades
        my_hp = my_p.health

        max_l, min_l, max_b, min_b, p_live, p_blank = self._get_shell_counts(obs)
        current_dmg = 1 + self.current_saw_stacked
        target = self._choose_best_target(obs, me, current_dmg)
        target_hp = obs.players[target].health

        # 1. Feature Extraction: Build 18-D state vector
        s = self.extract_state_vector(obs)
        self.last_state_vec = s

        # 2. Forward Pass: Compute Q-Values using Deep Q-Network
        q_values = self.model.predict_q_values(s)
        self.last_q_values = q_values

        # -------------------------------------------------------------
        # Action Masking: Enforce Invariant Decision Constraints
        # -------------------------------------------------------------
        valid_actions = {}

        # 0: JUICE (Top Priority: Heal whenever injured)
        if my_hp < obs.max_health and my_up.juice > 0:
            valid_actions[0] = q_values[0] + 55.0

        # 1: POOL_FLOATIE (Smart pin: skip lethal target to save floatie for surviving threats)
        if my_up.pool_floatie > 0:
            is_certain_live = (obs.next_round == NextRound.LIVE) or (p_live >= 0.999) or (max_b == 0)
            target_will_die = is_certain_live and (target_hp <= current_dmg)

            for offset in range(1, len(obs.players)):
                cand = (me + offset) % len(obs.players)
                if obs.players[cand].health > 0 and not obs.players[cand].has_pool_floatie_on:
                    if target_will_die and cand == target:
                        continue
                    valid_actions[1] = q_values[1] + 25.0
                    break

        # 2: MAG_GLASS (Vision Dominance: Peek before shooting uncertain chamber)
        if obs.next_round == NextRound.UNKNOWN and my_up.mag_glass > 0 and obs.rounds_remaining > 0:
            if 0.0 < p_live < 1.0:
                valid_actions[2] = q_values[2] + 40.0

        # 3: COFFEE (Eject shell if high blank odds and no Mag Glass)
        if obs.next_round == NextRound.UNKNOWN and my_up.coffee > 0 and obs.rounds_remaining > 1:
            if my_up.mag_glass == 0 and p_blank >= 0.70:
                valid_actions[3] = q_values[3] + 15.0

        # 4: HAND_SAW (Lethal Burst on confirmed Live)
        is_certain_live = (obs.next_round == NextRound.LIVE) or (p_live >= 0.999) or (max_b == 0)
        if is_certain_live and my_up.hand_saw > 0 and target_hp > current_dmg:
            valid_actions[4] = q_values[4] + 35.0

        # 5: SHOOT_SELF (Zero Gamble: ONLY if 100% mathematically proven blank)
        is_certain_blank = (obs.next_round == NextRound.BLANK) or (p_blank >= 0.999) or (max_l == 0)
        if is_certain_blank:
            valid_actions[5] = q_values[5] + 65.0

        # 6: SHOOT_OPPONENT (Terminal offensive action)
        if not is_certain_blank:
            valid_actions[6] = q_values[6]

        # Select action with maximal Q-value from valid actions
        best_action_id = max(valid_actions.keys(), key=lambda a: valid_actions[a])
        self.last_selected_action_name = ACTION_NAMES[best_action_id]

        action = Action_PLAY()
        action.useUpgrade = None
        action.target = None

        if best_action_id == 0:
            action.action = ActionType.USE_UPGRADE
            action.useUpgrade = UpgradeType.JUICE
            return action

        elif best_action_id == 1:
            action.action = ActionType.USE_UPGRADE
            action.useUpgrade = UpgradeType.POOL_FLOATIE
            is_certain_live = (obs.next_round == NextRound.LIVE) or (p_live >= 0.999) or (max_b == 0)
            target_will_die = is_certain_live and (target_hp <= current_dmg)
            for offset in range(1, len(obs.players)):
                cand = (me + offset) % len(obs.players)
                if obs.players[cand].health > 0 and not obs.players[cand].has_pool_floatie_on:
                    if target_will_die and cand == target:
                        continue
                    action.target = cand
                    break
            if action.target is None:
                for offset in range(1, len(obs.players)):
                    cand = (me + offset) % len(obs.players)
                    if obs.players[cand].health > 0 and not obs.players[cand].has_pool_floatie_on:
                        action.target = cand
                        break
            return action

        elif best_action_id == 2:
            action.action = ActionType.USE_UPGRADE
            action.useUpgrade = UpgradeType.MAG_GLASS
            self.current_saw_stacked = 0
            return action

        elif best_action_id == 3:
            action.action = ActionType.USE_UPGRADE
            action.useUpgrade = UpgradeType.COFFEE
            return action

        elif best_action_id == 4:
            action.action = ActionType.USE_UPGRADE
            action.useUpgrade = UpgradeType.HAND_SAW
            self.current_saw_stacked += 1
            return action

        elif best_action_id == 5:
            action.action = ActionType.SHOOT
            action.target = me
            self.current_saw_stacked = 0
            return action

        elif best_action_id == 6:
            action.action = ActionType.SHOOT
            action.target = self._choose_best_target(obs, me, 1 + self.current_saw_stacked)
            self.current_saw_stacked = 0
            return action

        action.action = ActionType.SHOOT
        action.target = self._choose_best_target(obs, me, 1)
        return action

    def pick_upgrade(self, obs: Obs_PICK_UPGRADES) -> Action_PICK_UPGRADES:
        action = Action_PICK_UPGRADES()
        avail = obs.available_upgrades
        me = obs.turn
        my_p = obs.players[me]
        my_hp = my_p.health
        my_juice = my_p.upgrades.juice
        my_saws = my_p.upgrades.hand_saw
        my_mags = my_p.upgrades.mag_glass
        my_float = my_p.upgrades.pool_floatie

        # 1. Survival: If hurt or below minimum juice, ALWAYS grab Juice
        if (my_hp < 5 or my_juice < 2) and getattr(avail, "juice", 0) > 0:
            action.chosen_upgrade = UpgradeType.JUICE
            return action

        # 2. Vision: Ensure we have at least 1 Mag Glass for chamber control
        if my_mags < 2 and getattr(avail, "mag_glass", 0) > 0:
            action.chosen_upgrade = UpgradeType.MAG_GLASS
            return action

        # 3. Lethality: Ensure at least 1 Hand Saw for lethal burst
        if my_saws < 2 and getattr(avail, "hand_saw", 0) > 0:
            action.chosen_upgrade = UpgradeType.HAND_SAW
            return action

        # 4. Control: Ensure at least 1 Pool Floatie for skipping dangerous turns
        if my_float < 1 and getattr(avail, "pool_floatie", 0) > 0:
            action.chosen_upgrade = UpgradeType.POOL_FLOATIE
            return action

        # 5. Surplus Juice hoarding (starve opponents of healing)
        if getattr(avail, "juice", 0) > 0:
            action.chosen_upgrade = UpgradeType.JUICE
            return action

        for up_type, attr in [
            (UpgradeType.JUICE, "juice"),
            (UpgradeType.MAG_GLASS, "mag_glass"),
            (UpgradeType.HAND_SAW, "hand_saw"),
            (UpgradeType.POOL_FLOATIE, "pool_floatie"),
            (UpgradeType.COFFEE, "coffee"),
        ]:
            if getattr(avail, attr, 0) > 0:
                action.chosen_upgrade = up_type
                return action

        action.chosen_upgrade = UpgradeType.JUICE
        return action
