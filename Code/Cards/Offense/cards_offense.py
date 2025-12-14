from ..Card import Card, School, CardModifier, EffectTiming


class Strike(Card):
    """Basic attack card"""
    def __init__(self, card_id: int, tier: int = 0, school: School = School.NORMAL):
        super().__init__(card_id, tier, school)
    
    def get_base_cost(self, tier: int) -> int:
        if self.school == School.MAGICAL:
            return 1
        elif self.school in [School.NORMAL, School.TECHNICAL]:
            return 2 if tier < 2 else 1
    
    def get_name(self, tier: int) -> str:
        if self.school == School.NORMAL:
            names = {0: "Strike", 1: "Precise Strike", 2: "Overwhelming Strike"}
        elif self.school == School.MAGICAL:
            names = {0: "Arcane Bolt", 1: "Arcane Missile", 2: "Arcane Barrage"}
        else:  # TECHNICAL
            names = {0: "Tactical Strike", 1: "Calculated Strike", 2: "Optimized Strike"}
        return names.get(tier, f"Strike +{tier}")

    def get_effect_value(self, tier: int) -> int:
        if self.school == School.TECHNICAL:
            damage = 4 + (tier * 4)
        else:
            damage = 3 + (tier * 3)
        return damage
    
    def effect(self, game_state, tier: int):
        if self.school == School.TECHNICAL:
            damage = 4 + (tier * 4)
        else:
            damage = 3 + (tier * 3)
        
        for modifier in self.modifiers:
            damage = int(damage * modifier.damage_multiplier)
        game_state[1].deal_damage(damage)

    def get_image_path(self) -> str:
        if self.school == School.NORMAL: return 'Assets/Images/Cards/Damage/card-strike-normal.png'
        if self.school == School.MAGICAL: return 'Assets/Images/Cards/Damage/card-strike-magical.png'
        if self.school == School.TECHNICAL: return 'Assets/Images/Cards/Damage/card-strike-technical.png'
        return ''

class Slash(Card):
    """Multiple weak hits"""
    def __init__(self, card_id: int, tier: int = 0, school: School = School.NORMAL):
        super().__init__(card_id, tier, school)
    
    def get_base_cost(self, tier: int) -> int:
        if self.school == School.MAGICAL:
            return 1
        else:
            return 2
    
    def get_name(self, tier: int) -> str:
        if self.school == School.NORMAL:
            names = {0: "Slash", 1: "Flurry", 2: "Blade Storm"}
        elif self.school == School.MAGICAL:
            names = {0: "Magic Darts", 1: "Magic Volley", 2: "Magic Storm"}
        else:  # TECHNICAL
            names = {0: "Precision Cuts", 1: "Precision Flurry", 2: "Precision Storm"}
        return names.get(tier, f"Slash +{tier}")

    def get_effect_value(self, tier: int) -> int:
        hits = 2 + tier
        if self.school == School.TECHNICAL:
            damage_per_hit = 3
        else:
            damage_per_hit = 2
        return hits * damage_per_hit
    
    def effect(self, game_state, tier: int):
        hits = 2 + tier
        
        if self.school == School.TECHNICAL:
            damage_per_hit = 3
        else:
            damage_per_hit = 2
        
        for _ in range(hits):
            damage = damage_per_hit
            for modifier in self.modifiers:
                damage = int(damage * modifier.damage_multiplier)
            game_state[1].deal_damage(damage)

    def get_image_path(self) -> str:
        if self.school == School.NORMAL: return 'Assets/Images/Cards/Damage/card-kick-normal.png'
        if self.school == School.MAGICAL: return 'Assets/Images/Cards/Damage/card-kick-magical.png'
        if self.school == School.TECHNICAL: return 'Assets/Images/Cards/Damage/card-kick-technical.png'
        return ''


class HeavyStrike(Card):
    """High cost, high damage"""
    def __init__(self, card_id: int, tier: int = 0, school: School = School.NORMAL):
        super().__init__(card_id, tier, school)
    
    def get_base_cost(self, tier: int) -> int:
        if self.school == School.MAGICAL:
            return 2
        else:
            return 3
    
    def get_name(self, tier: int) -> str:
        if self.school == School.NORMAL:
            names = {0: "Heavy Strike", 1: "Crushing Blow", 2: "Devastating Impact"}
        elif self.school == School.MAGICAL:
            names = {0: "Fireball", 1: "Greater Fireball", 2: "Meteor"}
        else:  # TECHNICAL
            names = {0: "Armor Breaker", 1: "Fortress Breaker", 2: "Wall Breaker"}
        return names.get(tier, f"Heavy Strike +{tier}")

    def get_effect_value(self, tier: int) -> int:
        base_damage = 10 + (tier * 5)
        if self.school == School.TECHNICAL:
            base_damage += 2
        return base_damage
    
    def effect(self, game_state, tier: int):
        base_damage = 10 + (tier * 5)
        
        if self.school == School.TECHNICAL:
            base_damage += 2
            damage = base_damage
            for modifier in self.modifiers:
                damage = int(damage * modifier.damage_multiplier)
            game_state[1].deal_damage(damage, ignore_armor=True)
        else:
            damage = base_damage
            for modifier in self.modifiers:
                damage = int(damage * modifier.damage_multiplier)
            game_state[1].deal_damage(damage)

    def get_image_path(self) -> str:
        if self.school == School.NORMAL: return 'Assets/Images/Cards/Damage/card-punch-normal.png'
        if self.school == School.MAGICAL: return 'Assets/Images/Cards/Damage/card-punch-magical.png'
        if self.school == School.TECHNICAL: return 'Assets/Images/Cards/Damage/card-punch-technical.png'
        return ''


class Execute(Card):
    """Bonus damage to wounded enemies"""
    def __init__(self, card_id: int, tier: int = 0, school: School = School.NORMAL):
        super().__init__(card_id, tier, school)
    
    def get_base_cost(self, tier: int) -> int:
        if self.school == School.MAGICAL:
            return 1
        else:
            return 2
    
    def get_name(self, tier: int) -> str:
        if self.school == School.NORMAL:
            names = {0: "Execute", 1: "Executioner's Blade", 2: "Final Strike"}
        elif self.school == School.MAGICAL:
            names = {0: "Soul Rend", 1: "Soul Shatter", 2: "Soul Annihilation"}
        else:  # TECHNICAL
            names = {0: "Lethal Strike", 1: "Assassinate", 2: "Death Blow"}
        return names.get(tier, f"Execute +{tier}")

    def get_effect_value(self, tier: int) -> int:
        base_damage = 5 + (tier * 3)
        if self.school == School.TECHNICAL:
            base_damage += 1
        return base_damage
    
    def effect(self, game_state, tier: int):
        base_damage = 5 + (tier * 3)
        enemy_hp_percent = game_state[1].get_hp_percent()
        
        if self.school == School.TECHNICAL:
            threshold = 0.6
            multiplier = 2.5
            base_damage += 1
        else:
            threshold = 0.5
            multiplier = 2.0
        
        if enemy_hp_percent < threshold:
            base_damage = int(base_damage * multiplier)
        
        damage = base_damage
        for modifier in self.modifiers:
            damage = int(damage * modifier.damage_multiplier)
        game_state[1].deal_damage(damage)

    def get_image_path(self) -> str:
        if self.school == School.NORMAL: return 'Assets/Images/Cards/Damage/card-strike-normal.png'
        if self.school == School.MAGICAL: return 'Assets/Images/Cards/Damage/card-strike-magical.png'
        if self.school == School.TECHNICAL: return 'Assets/Images/Cards/Damage/card-strike-technical.png'
        return ''


class PoisonStrike(Card):
    """Damage over time"""
    def __init__(self, card_id: int, tier: int = 0, school: School = School.NORMAL):
        super().__init__(card_id, tier, school)
    
    def get_base_cost(self, tier: int) -> int:
        return 1
    
    def get_name(self, tier: int) -> str:
        if self.school == School.NORMAL:
            names = {0: "Poison Strike", 1: "Toxic Strike", 2: "Deadly Venom"}
        elif self.school == School.MAGICAL:
            names = {0: "Curse", 1: "Greater Curse", 2: "Doom"}
        else:  # TECHNICAL
            names = {0: "Bio Weapon", 1: "Neurotoxin", 2: "Plague Agent"}
        return names.get(tier, f"Poison Strike +{tier}")

    def get_effect_value(self, tier: int) -> int:
        immediate_damage = 2 + tier
        return immediate_damage
    
    def effect(self, game_state, tier: int):
        immediate_damage = 2 + tier
        
        if self.school == School.TECHNICAL:
            poison_damage = 3 + (tier * 2)
            duration = 3
        else:
            poison_damage = 2 + (tier * 1)
            duration = 3
        
        damage = immediate_damage
        for modifier in self.modifiers:
            damage = int(damage * modifier.damage_multiplier)
        game_state[1].deal_damage(damage)
        game_state[1].apply_poison(poison_damage, duration)

    def get_image_path(self) -> str:
        if self.school == School.NORMAL: return 'Assets/Images/Cards/Damage/card-strike-normal.png'
        if self.school == School.MAGICAL: return 'Assets/Images/Cards/Damage/card-strike-magical.png'
        if self.school == School.TECHNICAL: return 'Assets/Images/Cards/Damage/card-strike-technical.png'
        return ''


class AreaAttack(Card):
    """Damage all enemies"""
    def __init__(self, card_id: int, tier: int = 0, school: School = School.NORMAL):
        super().__init__(card_id, tier, school)
    
    def get_base_cost(self, tier: int) -> int:
        if self.school == School.MAGICAL:
            return 2
        else:
            return 3
    
    def get_name(self, tier: int) -> str:
        if self.school == School.NORMAL:
            names = {0: "Whirlwind", 1: "Cyclone", 2: "Maelstrom"}
        elif self.school == School.MAGICAL:
            names = {0: "Chain Lightning", 1: "Thunder Storm", 2: "Apocalypse"}
        else:  # TECHNICAL
            names = {0: "Grenade", 1: "Cluster Bomb", 2: "Carpet Bombing"}
        return names.get(tier, f"Whirlwind +{tier}")

    def get_effect_value(self, tier: int) -> int:
        if self.school == School.TECHNICAL:
            damage = 6 + (tier * 3)
        else:
            damage = 5 + (tier * 2)
        return damage
    
    def effect(self, game_state, tier: int):
        if self.school == School.TECHNICAL:
            damage = 6 + (tier * 3)
        else:
            damage = 5 + (tier * 2)
        
        for modifier in self.modifiers:
            damage = int(damage * modifier.damage_multiplier)
        game_state[1].deal_damage_aoe(damage)

    def get_image_path(self) -> str:
        if self.school == School.NORMAL: return 'Assets/Images/Cards/Damage/card-strike-normal.png'
        if self.school == School.MAGICAL: return 'Assets/Images/Cards/Damage/card-strike-magical.png'
        if self.school == School.TECHNICAL: return 'Assets/Images/Cards/Damage/card-strike-technical.png'
        return ''
