from ..Card import Card, School, CardModifier, EffectTiming


class ShieldUp(Card):
    """Basic defense card"""
    def __init__(self, card_id: int, tier: int = 0, school: School = School.NORMAL):
        super().__init__(card_id, tier, school)
    
    def get_base_cost(self, tier: int) -> int:
        if self.school == School.MAGICAL:
            return 1
        elif tier >= 2:
            return 1
        else:
            return 2
    
    def get_name(self, tier: int) -> str:
        if self.school == School.NORMAL:
            names = {0: "Shield Up", 1: "Shield Wall", 2: "Fortress"}
        elif self.school == School.MAGICAL:
            names = {0: "Magic Barrier", 1: "Arcane Shield", 2: "Mystic Fortress"}
        else:  # TECHNICAL
            names = {0: "Deploy Shield", 1: "Energy Barrier", 2: "Force Field"}
        return names.get(tier, f"Shield Up +{tier}")

    def get_effect_value(self, tier: int) -> int:
        if self.school == School.TECHNICAL:
            defense = 4 + (tier * 4)
        else:
            defense = 3 + (tier * 3)
        return defense

    def effect(self, game_state, tier: int):
        if self.school == School.TECHNICAL:
            defense = 4 + (tier * 4)
        else:
            defense = 3 + (tier * 3)
        
        game_state[0].add_block(defense)

    def get_image_path(self) -> str:
        if self.school == School.NORMAL: return 'Assets/Images/Cards/Defense/card-block-normal.png'
        if self.school == School.MAGICAL: return 'Assets/Images/Cards/Defense/card-block-magical.png'
        if self.school == School.TECHNICAL: return 'Assets/Images/Cards/Defense/card-block-technical.png'
        return ''


class Dodge(Card):
    """Avoid next attack"""
    def __init__(self, card_id: int, tier: int = 0, school: School = School.NORMAL):
        super().__init__(card_id, tier, school)
    
    def get_base_cost(self, tier: int) -> int:
        if self.school == School.MAGICAL:
            return 0 if tier >= 1 else 1
        else:
            return 1
    
    def get_name(self, tier: int) -> str:
        if self.school == School.NORMAL:
            names = {0: "Dodge", 1: "Evasion", 2: "Phase Shift"}
        elif self.school == School.MAGICAL:
            names = {0: "Blink", 1: "Teleport", 2: "Dimension Door"}
        else:  # TECHNICAL
            names = {0: "Sidestep", 1: "Quick Dash", 2: "Burst Movement"}
        return names.get(tier, f"Dodge +{tier}")

    def get_effect_value(self, tier: int) -> int:
        return 1 + tier
    
    def effect(self, game_state, tier: int):
        if self.school == School.TECHNICAL:
            game_state[0].add_dodge(1 + tier)
            game_state[0].add_block(2 + tier)
        else:
            game_state[0].add_dodge(1 + tier)

    def get_image_path(self) -> str:
        if self.school == School.NORMAL: return 'Assets/Images/Cards/Defense/card-dodge-normal.png'
        if self.school == School.MAGICAL: return 'Assets/Images/Cards/Defense/card-dodge-magical.png'
        if self.school == School.TECHNICAL: return 'Assets/Images/Cards/Defense/card-dodge-technical.png'
        return ''


class ArmorUp(Card):
    """Permanent damage reduction"""
    def __init__(self, card_id: int, tier: int = 0, school: School = School.NORMAL):
        super().__init__(card_id, tier, school)
    
    def get_base_cost(self, tier: int) -> int:
        if self.school == School.MAGICAL:
            return 1
        else:
            return 2
    
    def get_name(self, tier: int) -> str:
        if self.school == School.NORMAL:
            names = {0: "Armor Up", 1: "Fortify", 2: "Iron Skin"}
        elif self.school == School.MAGICAL:
            names = {0: "Stoneskin", 1: "Greater Stoneskin", 2: "Diamond Skin"}
        else:  # TECHNICAL
            names = {0: "Plating", 1: "Reinforced Plating", 2: "Reactive Armor"}
        return names.get(tier, f"Armor Up +{tier}")

    def get_effect_value(self, tier: int) -> int:
        if self.school == School.TECHNICAL:
            armor = 2 + (tier * 2)
        else:
            armor = 1 + (tier * 1)
        return armor
    
    def effect(self, game_state, tier: int):
        if self.school == School.TECHNICAL:
            armor = 2 + (tier * 2)
        else:
            armor = 1 + (tier * 1)
        
        game_state[0].add_armor(armor)

    def get_image_path(self) -> str:
        if self.school == School.NORMAL: return 'Assets/Images/Cards/Defense/card-block-normal.png'
        if self.school == School.MAGICAL: return 'Assets/Images/Cards/Defense/card-block-magical.png'
        if self.school == School.TECHNICAL: return 'Assets/Images/Cards/Defense/card-block-technical.png'
        return ''


class CounterAttack(Card):
    """Damage enemy when hit"""
    def __init__(self, card_id: int, tier: int = 0, school: School = School.NORMAL):
        super().__init__(card_id, tier, school)
    
    def get_base_cost(self, tier: int) -> int:
        if self.school == School.MAGICAL:
            return 1
        else:
            return 2
    
    def get_name(self, tier: int) -> str:
        if self.school == School.NORMAL:
            names = {0: "Counter Attack", 1: "Riposte", 2: "Perfect Counter"}
        elif self.school == School.MAGICAL:
            names = {0: "Thorn Shield", 1: "Reflection", 2: "Mirror Image"}
        else:  # TECHNICAL
            names = {0: "Auto-Turret", 1: "Defense System", 2: "Retaliation Protocol"}
        return names.get(tier, f"Counter Attack +{tier}")

    def get_effect_value(self, tier: int) -> int:
        if self.school == School.TECHNICAL:
            damage = 4 + (tier * 3)
        else:
            damage = 3 + (tier * 2)
        return damage
    
    def effect(self, game_state, tier: int):
        if self.school == School.TECHNICAL:
            damage = 4 + (tier * 3)
            stacks = 2
        else:
            damage = 3 + (tier * 2)
            stacks = 1
        
        game_state[0].add_thorns(damage, stacks)

    def get_image_path(self) -> str:
        if self.school == School.NORMAL: return 'Assets/Images/Cards/Defense/card-block-normal.png'
        if self.school == School.MAGICAL: return 'Assets/Images/Cards/Defense/card-block-magical.png'
        if self.school == School.TECHNICAL: return 'Assets/Images/Cards/Defense/card-block-technical.png'
        return ''


class Regeneration(Card):
    """Heal over time"""
    def __init__(self, card_id: int, tier: int = 0, school: School = School.NORMAL):
        super().__init__(card_id, tier, school)
    
    def get_base_cost(self, tier: int) -> int:
        return 1
    
    def get_name(self, tier: int) -> str:
        if self.school == School.NORMAL:
            names = {0: "Bandages", 1: "First Aid", 2: "Full recovery"}
        elif self.school == School.MAGICAL:
            names = {0: "Runic Wrap", 1: "Spirit Thread", 2: "Blessed Cloth"}
        else:  # TECHNICAL
            names = {0: "Med Kit", 1: "Auto-Repair", 2: "Systemic Repair"}
        return names.get(tier, f"Regeneration +{tier}")

    def get_effect_value(self, tier: int) -> int:
        if self.school == School.TECHNICAL:
            heal_per_turn = 3 + (tier * 2)
        else:
            heal_per_turn = 2 + (tier * 1)
        return heal_per_turn
    
    def effect(self, game_state, tier: int):
        if self.school == School.TECHNICAL:
            heal_per_turn = 3 + (tier * 2)
            duration = 3 + tier
        else:
            heal_per_turn = 2 + (tier * 1)
            duration = 3
        
        game_state[0].add_regeneration(heal_per_turn, duration)

    def get_image_path(self) -> str:
        if self.school == School.NORMAL: return 'Assets/Images/Cards/Heal/card-bandages-normal.png'
        if self.school == School.MAGICAL: return 'Assets/Images/Cards/Heal/card-bandages-magical.png'
        if self.school == School.TECHNICAL: return 'Assets/Images/Cards/Heal/card-bandages-technical.png'
        return ''


class Heal(Card):
    """Immediate healing"""
    def __init__(self, card_id: int, tier: int = 0, school: School = School.NORMAL):
        super().__init__(card_id, tier, school)
    
    def get_base_cost(self, tier: int) -> int:
        if self.school == School.MAGICAL:
            return 1
        else:
            return 2
    
    def get_name(self, tier: int) -> str:
        if self.school == School.NORMAL:
            names = {0: "Health Potion", 1: "Revitalizing Brew", 2: "Panacea"}
        elif self.school == School.MAGICAL:
            names = {0: "Healing Charm", 1: "Restorative Brew", 2: "Elixir of Life"}
        else:  # TECHNICAL
            names = {0: "Quick Synth", 1: "Gene Reconstructor", 2: "Emergency Protocol"}
        return names.get(tier, f"Bandage +{tier}")

    def get_effect_value(self, tier: int) -> int:
        if self.school == School.TECHNICAL:
            heal = 6 + (tier * 4)
        else:
            heal = 5 + (tier * 3)

        return heal
    
    def effect(self, game_state, tier: int):
        if self.school == School.TECHNICAL:
            heal = 6 + (tier * 4)
        else:
            heal = 5 + (tier * 3)
        
        game_state[0].heal(heal)

    def get_image_path(self) -> str:
        if self.school == School.NORMAL: return 'Assets/Images/Cards/Heal/card-heal-normal.png'
        if self.school == School.MAGICAL: return 'Assets/Images/Cards/Heal/card-heal-magical.png'
        if self.school == School.TECHNICAL: return 'Assets/Images/Cards/Heal/card-heal-technical.png'
        return ''


class Parry(Card):
    """Block and counter"""
    def __init__(self, card_id: int, tier: int = 0, school: School = School.NORMAL):
        super().__init__(card_id, tier, school)
    
    def get_base_cost(self, tier: int) -> int:
        if self.school == School.MAGICAL:
            return 1
        else:
            return 2
    
    def get_name(self, tier: int) -> str:
        if self.school == School.NORMAL:
            names = {0: "Parry", 1: "Perfect Parry", 2: "Master's Parry"}
        elif self.school == School.MAGICAL:
            names = {0: "Spell Shield", 1: "Counterspell", 2: "Absorption"}
        else:  # TECHNICAL
            names = {0: "Deflect", 1: "Active Defense", 2: "Adaptive Shield"}
        return names.get(tier, f"Parry +{tier}")

    def get_effect_value(self, tier: int) -> int:
        if self.school == School.TECHNICAL:
            block = 4 + (tier * 2)
        else:
            block = 3 + (tier * 2)
        return block
    
    def effect(self, game_state, tier: int):
        if self.school == School.TECHNICAL:
            block = 4 + (tier * 2)
            damage = 3 + (tier * 2)
        else:
            block = 3 + (tier * 2)
            damage = 2 + (tier * 1)
        
        game_state[0].add_block(block)
        game_state[0].add_next_attack_counter(damage)

    def get_image_path(self) -> str:
        if self.school == School.NORMAL: return 'Assets/Images/Cards/Defense/card-block-normal.png'
        if self.school == School.MAGICAL: return 'Assets/Images/Cards/Defense/card-block-magical.png'
        if self.school == School.TECHNICAL: return 'Assets/Images/Cards/Defense/card-block-technical.png'
        return ''