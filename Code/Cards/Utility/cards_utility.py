from ..Card import Card, School, CardModifier, EffectTiming


class DrawCards(Card):
    """Simple card draw"""
    image_paths = {
        School.NORMAL: '',
        School.MAGICAL: '',
        School.TECHNICAL: '',
    }
    
    def __init__(self, card_id: int, tier: int = 0, school: School = School.NORMAL):
        super().__init__(card_id, tier, school)
    
    def get_base_cost(self, tier: int) -> int:
        if self.school == School.MAGICAL:
            return 0
        else:
            return 1
    
    def get_name(self, tier: int) -> str:
        if self.school == School.NORMAL:
            names = {0: "Draw Cards", 1: "Deep Study", 2: "Master's Insight"}
        elif self.school == School.MAGICAL:
            names = {0: "Divination", 1: "Scrying", 2: "Omniscience"}
        else:  # TECHNICAL
            names = {0: "Scan", 1: "Data Mining", 2: "Full Analysis"}
        return names.get(tier, f"Draw Cards +{tier}")

    def get_effect_value(self, tier: int) -> int:
        if self.school == School.TECHNICAL:
            num_cards = 3 + tier
        else:
            num_cards = 2 + tier
        return num_cards
    
    def effect(self, game_state, tier: int):
        if self.school == School.TECHNICAL:
            num_cards = 3 + tier
        else:
            num_cards = 2 + tier
        
        game_state[0].draw_cards(num_cards)


class DrawAndDiscount(Card):
    """Draw cards with cost reduction"""
    image_paths = {
        School.NORMAL: '',
        School.MAGICAL: '',
        School.TECHNICAL: '',
    }
    
    def __init__(self, card_id: int, tier: int = 0, school: School = School.NORMAL):
        super().__init__(card_id, tier, school)
    
    def get_base_cost(self, tier: int) -> int:
        return 1
    
    def get_name(self, tier: int) -> str:
        if self.school == School.NORMAL:
            names = {0: "Bargain Hunter", 1: "Opportunist", 2: "Master Trader"}
        elif self.school == School.MAGICAL:
            names = {0: "Mana Infusion", 1: "Arcane Efficiency", 2: "Spell Mastery"}
        else:  # TECHNICAL
            names = {0: "Optimization", 1: "System Override", 2: "Maximum Efficiency"}
        return names.get(tier, f"Bargain Hunter +{tier}")

    def get_effect_value(self, tier: int) -> int:
        num_cards = 3 + tier
        return num_cards
    
    def effect(self, game_state, tier: int):
        if self.school == School.TECHNICAL:
            num_cards = 3 + tier
            discount = -3
        else:
            num_cards = 3 + tier
            discount = -2
        
        drawn_cards = game_state[0].draw_cards(num_cards)
        
        discount_modifier = CardModifier(
            cost_change=discount,
            timing=EffectTiming.UNTIL_PLAYED,
            description=f"Costs {abs(discount)} less (until played)"
        )
        
        for card in drawn_cards:
            card.add_modifier(discount_modifier)


class BattleRage(Card):
    """Damage boost for hand"""
    image_paths = {
        School.NORMAL: '',
        School.MAGICAL: '',
        School.TECHNICAL: '',
    }
    
    def __init__(self, card_id: int, tier: int = 0, school: School = School.NORMAL):
        super().__init__(card_id, tier, school)
    
    def get_base_cost(self, tier: int) -> int:
        if self.school == School.MAGICAL:
            return 0
        else:
            return 1
    
    def get_name(self, tier: int) -> str:
        if self.school == School.NORMAL:
            names = {0: "Battle Rage", 1: "Fury", 2: "Berserk"}
        elif self.school == School.MAGICAL:
            names = {0: "Empower", 1: "Greater Empower", 2: "Divine Power"}
        else:  # TECHNICAL
            names = {0: "Targeting System", 1: "Weapon Calibration", 2: "Overcharge"}
        return names.get(tier, f"Battle Rage +{tier}")

    def get_effect_value(self, tier: int) -> int:
        if self.school == School.TECHNICAL:
            multiplier = 1.75 + (tier * 0.25)
        else:
            multiplier = 1.5 + (tier * 0.25)
        return int((multiplier - 1) * 100)
    
    def effect(self, game_state, tier: int):
        if self.school == School.TECHNICAL:
            multiplier = 1.75 + (tier * 0.25)
        else:
            multiplier = 1.5 + (tier * 0.25)
        
        damage_boost = CardModifier(
            damage_multiplier=multiplier,
            timing=EffectTiming.END_OF_TURN,
            description=f"+{int((multiplier-1)*100)}% damage this turn"
        )
        
        for card in game_state[0].hand:
            card.add_modifier(damage_boost)


class ManaGain(Card):
    """Gain extra mana"""
    image_paths = {
        School.NORMAL: '',
        School.MAGICAL: '',
        School.TECHNICAL: '',
    }
    
    def __init__(self, card_id: int, tier: int = 0, school: School = School.NORMAL):
        super().__init__(card_id, tier, school)
    
    def get_base_cost(self, tier: int) -> int:
        return 0
    
    def get_name(self, tier: int) -> str:
        if self.school == School.NORMAL:
            names = {0: "Second Wind", 1: "Adrenaline Rush", 2: "Limitless Energy"}
        elif self.school == School.MAGICAL:
            names = {0: "Mana Crystal", 1: "Mana Gem", 2: "Mana Core"}
        else:  # TECHNICAL
            names = {0: "Energy Cell", 1: "Power Core", 2: "Fusion Reactor"}
        return names.get(tier, f"Mana Gain +{tier}")

    def get_effect_value(self, tier: int) -> int:
        if self.school == School.TECHNICAL:
            mana = 3 + tier
        else:
            mana = 2 + tier
        return mana
    
    def effect(self, game_state, tier: int):
        if self.school == School.TECHNICAL:
            mana = 3 + tier
        else:
            mana = 2 + tier
        
        game_state[0].add_mana(mana)


class DiscardForPower(Card):
    """Discard cards for benefits"""
    image_paths = {
        School.NORMAL: '',
        School.MAGICAL: '',
        School.TECHNICAL: '',
    }
    
    def __init__(self, card_id: int, tier: int = 0, school: School = School.NORMAL):
        super().__init__(card_id, tier, school)
    
    def get_base_cost(self, tier: int) -> int:
        if self.school == School.MAGICAL:
            return 0
        else:
            return 1
    
    def get_name(self, tier: int) -> str:
        if self.school == School.NORMAL:
            names = {0: "Desperate Measures", 1: "All In", 2: "Last Stand"}
        elif self.school == School.MAGICAL:
            names = {0: "Sacrifice", 1: "Blood Magic", 2: "Soul Sacrifice"}
        else:  # TECHNICAL
            names = {0: "Emergency Power", 1: "Core Dump", 2: "System Purge"}
        return names.get(tier, f"Desperate Measures +{tier}")

    def get_effect_value(self, tier: int) -> int:
        # Returns base damage for 2 discarded cards
        if self.school == School.TECHNICAL:
            damage = 5 * 2 + (tier * 3)
        else:
            damage = 4 * 2 + (tier * 2)
        return damage
    
    def effect(self, game_state, tier: int):
        num_to_discard = 2
        discarded = game_state[0].discard_from_hand(num_to_discard)
        
        if self.school == School.TECHNICAL:
            damage = 5 * len(discarded) + (tier * 3)
            block = 3 * len(discarded)
            game_state[0].add_block(block)
        else:
            damage = 4 * len(discarded) + (tier * 2)
        
        game_state[1].deal_damage(damage)


class Cycle(Card):
    """Discard and redraw"""
    image_paths = {
        School.NORMAL: '',
        School.MAGICAL: '',
        School.TECHNICAL: '',
    }
    
    def __init__(self, card_id: int, tier: int = 0, school: School = School.NORMAL):
        super().__init__(card_id, tier, school)
    
    def get_base_cost(self, tier: int) -> int:
        return 0
    
    def get_name(self, tier: int) -> str:
        if self.school == School.NORMAL:
            names = {0: "Cycle", 1: "Refresh", 2: "Perfect Flow"}
        elif self.school == School.MAGICAL:
            names = {0: "Transmute", 1: "Metamorphosis", 2: "Reality Shift"}
        else:  # TECHNICAL
            names = {0: "Reboot", 1: "System Refresh", 2: "Hot Swap"}
        return names.get(tier, f"Cycle +{tier}")

    def get_effect_value(self, tier: int) -> int:
        return 2 + tier
    
    def effect(self, game_state, tier: int):
        num_cards = 2 + tier
        
        if self.school == School.TECHNICAL:
            game_state[0].draw_cards(num_cards)
            game_state[0].discard_from_hand(num_cards)
        else:
            game_state[0].discard_from_hand(num_cards)
            game_state[0].draw_cards(num_cards)


class Duplicate(Card):
    """Copy a card in hand"""
    image_paths = {
        School.NORMAL: '',
        School.MAGICAL: '',
        School.TECHNICAL: '',
    }
    
    def __init__(self, card_id: int, tier: int = 0, school: School = School.NORMAL):
        super().__init__(card_id, tier, school)
    
    def get_base_cost(self, tier: int) -> int:
        if self.school == School.MAGICAL:
            return 1 if tier < 2 else 0
        else:
            return 2 if tier < 1 else 1
    
    def get_name(self, tier: int) -> str:
        if self.school == School.NORMAL:
            names = {0: "Duplicate", 1: "Echo", 2: "Multiplication"}
        elif self.school == School.MAGICAL:
            names = {0: "Conjure Copy", 1: "Mirror Spell", 2: "Mass Duplication"}
        else:  # TECHNICAL
            names = {0: "Clone", 1: "Replicate", 2: "Mass Production"}
        return names.get(tier, f"Duplicate +{tier}")

    def get_effect_value(self, tier: int) -> int:
        if self.school == School.TECHNICAL:
            copies = 2 + tier
        else:
            copies = 1 + tier
        return copies
    
    def effect(self, game_state, tier: int):
        if self.school == School.TECHNICAL:
            copies = 2 + tier
        else:
            copies = 1 + tier
        
        game_state[0].duplicate_card(copies)


class UpgradeCard(Card):
    """Upgrade a card in hand"""
    image_paths = {
        School.NORMAL: '',
        School.MAGICAL: '',
        School.TECHNICAL: '',
    }
    
    def __init__(self, card_id: int, tier: int = 0, school: School = School.NORMAL):
        super().__init__(card_id, tier, school)
    
    def get_base_cost(self, tier: int) -> int:
        if self.school == School.MAGICAL:
            return 1
        else:
            return 2
    
    def get_name(self, tier: int) -> str:
        if self.school == School.NORMAL:
            names = {0: "Hone", 1: "Master", 2: "Perfection"}
        elif self.school == School.MAGICAL:
            names = {0: "Enchant", 1: "Greater Enchant", 2: "Ultimate Enchant"}
        else:  # TECHNICAL
            names = {0: "Upgrade", 1: "Modify", 2: "Optimize"}
        return names.get(tier, f"Hone +{tier}")

    def get_effect_value(self, tier: int) -> int:
        if self.school == School.TECHNICAL:
            num_upgrades = 2 + tier
        else:
            num_upgrades = 1 + tier
        return num_upgrades
    
    def effect(self, game_state, tier: int):
        if self.school == School.TECHNICAL:
            num_upgrades = 2 + tier
        else:
            num_upgrades = 1 + tier
        
        game_state[0].upgrade_card_in_hand(num_upgrades)


class CostReduction(Card):
    """Reduce cost of cards in hand"""
    image_paths = {
        School.NORMAL: '',
        School.MAGICAL: '',
        School.TECHNICAL: '',
    }
    
    def __init__(self, card_id: int, tier: int = 0, school: School = School.NORMAL):
        super().__init__(card_id, tier, school)
    
    def get_base_cost(self, tier: int) -> int:
        if self.school == School.MAGICAL:
            return 0
        else:
            return 1
    
    def get_name(self, tier: int) -> str:
        if self.school == School.NORMAL:
            names = {0: "Quick Thinking", 1: "Momentum", 2: "Flow State"}
        elif self.school == School.MAGICAL:
            names = {0: "Inspiration", 1: "Enlightenment", 2: "Transcendence"}
        else:  # TECHNICAL
            names = {0: "Efficiency Mode", 1: "Turbo Boost", 2: "Overclock"}
        return names.get(tier, f"Quick Thinking +{tier}")

    def get_effect_value(self, tier: int) -> int:
        if self.school == School.TECHNICAL:
            cost_reduction = 2 + tier
        else:
            cost_reduction = 1 + tier
        return cost_reduction
    
    def effect(self, game_state, tier: int):
        if self.school == School.TECHNICAL:
            cost_reduction = -2 - tier
        else:
            cost_reduction = -1 - tier
        
        cost_modifier = CardModifier(
            cost_change=cost_reduction,
            timing=EffectTiming.END_OF_TURN,
            description=f"Costs {abs(cost_reduction)} less this turn"
        )
        
        for card in game_state[0].hand:
            card.add_modifier(cost_modifier)


class ExhaustForEffect(Card):
    """Remove card for powerful effect"""
    image_paths = {
        School.NORMAL: '',
        School.MAGICAL: '',
        School.TECHNICAL: '',
    }
    
    def __init__(self, card_id: int, tier: int = 0, school: School = School.NORMAL):
        super().__init__(card_id, tier, school)
    
    def get_base_cost(self, tier: int) -> int:
        if self.school == School.MAGICAL:
            return 0
        else:
            return 1
    
    def get_name(self, tier: int) -> str:
        if self.school == School.NORMAL:
            names = {0: "Last Resort", 1: "Burning Bright", 2: "Supernova"}
        elif self.school == School.MAGICAL:
            names = {0: "Ritual", 1: "Grand Ritual", 2: "Ultimate Sacrifice"}
        else:  # TECHNICAL
            names = {0: "Self Destruct", 1: "Overload", 2: "Meltdown"}
        return names.get(tier, f"Last Resort +{tier}")

    def get_effect_value(self, tier: int) -> int:
        if self.school == School.TECHNICAL:
            damage = 8 + (tier * 5)
        else:
            damage = 6 + (tier * 4)
        return damage
    
    def effect(self, game_state, tier: int):
        if self.school == School.TECHNICAL:
            damage = 8 + (tier * 5)
            block = 4 + (tier * 3)
            game_state[0].add_block(block)
        else:
            damage = 6 + (tier * 4)
        
        game_state[1].deal_damage(damage)
        game_state[0].exhaust_card(self)


class Scry(Card):
    """Look at and manipulate deck"""
    image_paths = {
        School.NORMAL: '',
        School.MAGICAL: '',
        School.TECHNICAL: '',
    }
    
    def __init__(self, card_id: int, tier: int = 0, school: School = School.NORMAL):
        super().__init__(card_id, tier, school)
    
    def get_base_cost(self, tier: int) -> int:
        return 0
    
    def get_name(self, tier: int) -> str:
        if self.school == School.NORMAL:
            names = {0: "Scout Ahead", 1: "Reconnaissance", 2: "Perfect Information"}
        elif self.school == School.MAGICAL:
            names = {0: "Scry", 1: "Foresight", 2: "Prophecy"}
        else:  # TECHNICAL
            names = {0: "Deck Analysis", 1: "Deep Scan", 2: "Probability Engine"}
        return names.get(tier, f"Scout Ahead +{tier}")

    def get_effect_value(self, tier: int) -> int:
        if self.school == School.TECHNICAL:
            look_ahead = 4 + tier
        else:
            look_ahead = 3 + tier
        return look_ahead
    
    def effect(self, game_state, tier: int):
        if self.school == School.TECHNICAL:
            look_ahead = 4 + tier
            discard_count = 2 + tier
        else:
            look_ahead = 3 + tier
            discard_count = 1 + tier
        
        game_state[0].scry(look_ahead, discard_count)
