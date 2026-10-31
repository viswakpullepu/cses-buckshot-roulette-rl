
from schemas import Action_PLAY, Action_PICK_UPGRADES, ActionType, UpgradeType, NextRound, Obs_PLAY, Obs_PICK_UPGRADES

class Bot:
    def init(self, params=None):
        self.current_saw_stacked = 0

    def _get_shell_counts(self, obs: Obs_PLAY):
        r = obs.rounds_remaining
        if r <= 0: return 0, 0, 0, 0, 0.0, 0.0
        if obs.next_round == NextRound.LIVE: return 1, 1, 0, 0, 1.0, 0.0
        if obs.next_round == NextRound.BLANK: return 0, 0, 1, 1, 0.0, 1.0

        known_lives_removed = obs.lives_shot + obs.ejections.lives_ejected
        known_blanks_removed = obs.blanks_shot + obs.ejections.blanks_ejected
        unknown_ejected = obs.ejections.unknowns_ejected

        max_lives_rem = max(0, obs.lives_init - known_lives_removed)
        max_blanks_rem = max(0, obs.blanks_init - known_blanks_removed)
        min_lives_rem = max(0, max_lives_rem - unknown_ejected)
        min_blanks_rem = max(0, max_blanks_rem - unknown_ejected)

        if max_blanks_rem == 0 or min_lives_rem == r: return r, r, 0, 0, 1.0, 0.0
        if max_lives_rem == 0 or min_blanks_rem == r: return 0, 0, r, r, 0.0, 1.0

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
        if not living: return me
        lethal = [i for i in living if obs.players[i].health <= damage]
        if lethal:
            lethal.sort(key=lambda idx: obs.players[idx].upgrades.hand_saw * 3 + obs.players[idx].upgrades.pool_floatie * 2, reverse=True)
            return lethal[0]
        living.sort(key=lambda idx: (obs.players[idx].health, idx))
        return living[0]

    def play(self, obs: Obs_PLAY) -> Action_PLAY:
        me = obs.turn
        my_p = obs.players[me]
        my_up = my_p.upgrades
        my_hp = my_p.health

        action = Action_PLAY()
        action.useUpgrade = None
        action.target = None

        max_l, min_l, max_b, min_b, p_live, p_blank = self._get_shell_counts(obs)

        # 1. HEAL
        if my_hp < obs.max_health and my_up.juice > 0:
            action.action = ActionType.USE_UPGRADE
            action.useUpgrade = UpgradeType.JUICE
            return action

        # 2. POOL FLOATIE
        if my_up.pool_floatie > 0:
            player_count = len(obs.players)
            for offset in range(1, player_count):
                cand = (me + offset) % player_count
                if obs.players[cand].health > 0 and not obs.players[cand].has_pool_floatie_on:
                    action.action = ActionType.USE_UPGRADE
                    action.useUpgrade = UpgradeType.POOL_FLOATIE
                    action.target = cand
                    return action

        # 3. MAG GLASS
        if obs.next_round == NextRound.UNKNOWN and my_up.mag_glass > 0 and obs.rounds_remaining > 0:
            if 0.0 < p_live < 1.0:
                action.action = ActionType.USE_UPGRADE
                action.useUpgrade = UpgradeType.MAG_GLASS
                self.current_saw_stacked = 0
                return action

        # 4. COFFEE
        if obs.next_round == NextRound.UNKNOWN and my_up.coffee > 0 and obs.rounds_remaining > 1:
            if my_up.mag_glass == 0 and p_blank >= 0.75:
                action.action = ActionType.USE_UPGRADE
                action.useUpgrade = UpgradeType.COFFEE
                return action

        # 5. HAND SAW
        is_certain_live = (obs.next_round == NextRound.LIVE) or (p_live >= 0.999)
        if is_certain_live and my_up.hand_saw > 0:
            current_dmg = 1 + self.current_saw_stacked
            target = self._choose_best_target(obs, me, current_dmg)
            target_hp = obs.players[target].health
            if target_hp > current_dmg:
                action.action = ActionType.USE_UPGRADE
                action.useUpgrade = UpgradeType.HAND_SAW
                self.current_saw_stacked += 1
                return action

        # 6. SHOOT
        action.action = ActionType.SHOOT
        current_dmg = 1 + self.current_saw_stacked
        self.current_saw_stacked = 0

        # Self shoot threshold
        if (obs.next_round == NextRound.BLANK) or (p_blank >= 0.7) or (max_l == 0):
            action.target = me
            return action

        action.target = self._choose_best_target(obs, me, current_dmg)
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

        # Draft logic
        
        if (my_hp < 5 or my_juice < 2) and getattr(avail, "juice", 0) > 0:
            action.chosen_upgrade = UpgradeType.JUICE
            return action
        if my_mags < 2 and getattr(avail, "mag_glass", 0) > 0:
            action.chosen_upgrade = UpgradeType.MAG_GLASS
            return action
        if my_saws < 3 and getattr(avail, "hand_saw", 0) > 0:
            action.chosen_upgrade = UpgradeType.HAND_SAW
            return action
        if getattr(avail, "pool_floatie", 0) > 0:
            action.chosen_upgrade = UpgradeType.POOL_FLOATIE
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
