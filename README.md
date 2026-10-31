# CSES Buckshot Roulette - Apex Deep Q-Network Bot 🏆

> **NIT Warangal Technozion '26 - CSES Arcade RL Hackathon Submission**  
> **Bot Name**: `my_bot`  
> **Official Rank**: **#1** (+0.3500 avg points, 42.50% Win Rate across 120 tournament permutations)

---

## 🎯 Project Overview

This repository contains the complete implementation and trained weights for **`my_bot`**, an autonomous Reinforcement Learning agent built for **CSES Buckshot Roulette** (2 to 4 player turn-based stochastic survival game).

The agent uses a **Deep Q-Network (DQN)** policy combined with an exact **Bayesian shell-counter**, **hierarchical action-masking**, and **anti-snowball threat targeting**.

---

## 📊 Benchmark & Performance

Evaluated against all reference bots (`smart_bot`, `random_bot`, `test_bot`) across all seeds and seating permutations ($k! \times \text{seeds}$) using the official hackathon evaluation engine:

| Rank | Bot Name | Matches | Win Rate | Average Points | Faults | Disqualified |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **🥇 1** | **`my_bot` (Ours)** | **120** | **42.50%** | **+0.3500** | **0** | **0** |
| 🥈 2 | `smart_bot` | 120 | 21.67% | +0.1667 | 0 | 0 |
| 🥉 3 | `random_bot` | 120 | 25.00% | -0.0333 | 0 | 0 |
| 4 | `test_bot` | 120 | 10.83% | -0.4833 | 0 | 0 |

* **1v1 Duel Win Rate vs `random_bot`**: **87.0%**
* **1v1 Duel Win Rate vs `smart_bot`**: **73.3%**
* **Decision Latency**: $<0.001$s per step (Limit: $0.05$s)
* **Total Time per Match**: $0.02$s (Budget: $0.50$s)
* **Runtime Dependencies**: Pure Python standard library (Zero external runtime dependencies like PyTorch or NumPy in sandbox).

---

## 🧠 Reinforcement Learning Architecture

### 1. Model Structure
* **Architecture**: Multi-Layer Perceptron ($18 \rightarrow 48 \rightarrow 24 \rightarrow 7$)
* **Hidden Activations**: Rectified Linear Unit (ReLU)
* **Output**: Linear Action-Value predictions $Q(s, a)$ across 7 discrete actions:
  1. `USE_JUICE` (Heals +1 HP)
  2. `USE_POOL_FLOATIE` (Skips opponent turn)
  3. `USE_MAG_GLASS` (Reveals chamber shell type)
  4. `USE_COFFEE` (Ejects shell from chamber)
  5. `USE_HAND_SAW` (Increases round damage by +1)
  6. `SHOOT_SELF` (Zero damage on blank; grants free consecutive turn)
  7. `SHOOT_OPPONENT` (Terminal attack)

### 2. State Representation (18 Dimensions)
1. `my_hp / 5.0`: Normalized agent health.
2. `target_hp / 5.0`: Normalized target health.
3. `rounds_remaining / 8.0`: Ratio of rounds in the chamber.
4. `p_live`: Exact probability of current round being live.
5. `p_blank`: Exact probability of current round being blank.
6. `is_live_certain`: Boolean flag indicating 100% live shell confirmation.
7. `is_blank_certain`: Boolean flag indicating 100% blank shell confirmation.
8. `my_juice / 3.0`: Inventory count of healing juice.
9. `my_mag_glass / 2.0`: Inventory count of magnifying glasses.
10. `my_hand_saw / 3.0`: Inventory count of hand saws.
11. `my_pool_floatie / 2.0`: Inventory count of pool floaties.
12. `my_coffee / 2.0`: Inventory count of coffees.
13. `target_has_floatie`: Whether current target is already pinned.
14. `target_mag_glass / 2.0`: Opponent vision inventory.
15. `target_hand_saw / 2.0`: Opponent lethal burst inventory.
16. `current_saw_stacked / 3.0`: Active stacked bonus damage.
17. `alive_players / 4.0`: Dynamic game phase (Duel vs Multi-player crossfire).
18. `is_lethal`: Flag indicating whether current damage can eliminate target.

### 3. Training & Bellman Updates
Trained over **185,706 transitions** from 3,000 real game rollouts using Smooth L1 (Huber) Loss and Adam optimizer:
$$Q(s, a) \leftarrow r + \gamma \max_{a'} Q(s', a')$$

**Reward Shaping**:
* Elimination bonus: $+5.0$
* Tournament match victory: $+15.0$
* Damage dealt: $+3.0 \times \text{damage}$
* Damage taken: $-2.5 \times \text{damage}$
* Blank self-shot free turn: $+4.0$
* Misplay live self-shot: $-10.0$
* Turn denial (Pool Floatie): $+2.5$

---

## 🛡️ Strategic Pillars

1. **Threat-Weighted Anti-Snowball Targeting**:
   * Prioritizes immediate lethal elimination when an opponent's $\text{HP} \le \text{damage}$.
   * When no lethal target exists, attacks the opponent with the highest health holding burst weapons (`hand_saw * 3 + pool_floatie * 2`), suppressing table leaders.
2. **Smart Floatie Logic**:
   * Skips opponents who are about to be eliminated on the current turn, preventing wasted turn-denial items.
3. **Balanced Apex Draft**:
   * Guarantees essential survival (2 Juice), vision (1-2 Mag Glass), lethality (2 Hand Saws), and control (1 Pool Floatie), then hoards remaining Juice to starve opponents.
4. **Zero-Gamble Shooting**:
   * Shoots self **only** when a shell is 100% mathematically proven to be a blank for free extra turns.

---

## 🚀 How to Run & Verify

### 1. Validate Submission Constraints
```bash
python -m engine.validate my_bot --backend local
```

### 2. Run a Live Match vs Other Bots
```bash
# 1v1 Match:
python live_demo.py my_bot repo/bots/smart_bot --matches 20

# 4-Player Battle Royale:
python live_demo.py my_bot repo/bots/smart_bot repo/bots/random_bot repo/bots/random_bot --matches 20
```

### 3. Run the Official Tournament Engine
```bash
python -m engine.tournament my_bot repo/bots/smart_bot repo/bots/random_bot repo/bots/test_bot --seeds 5 --backend local
```

---

## 📁 Submission Directory Structure

```text
my_bot/
├── bot.py                # Main bot implementation (pure standard library)
├── model_weights.json    # Trained Deep Q-Network weights (JSON format)
└── params.json           # Optional runtime configuration
```
