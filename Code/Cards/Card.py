from abc import ABC, abstractmethod
from typing import Dict, List, Callable
import random
from enum import Enum


class EffectTiming(Enum):
    """When effects should be removed"""
    UNTIL_PLAYED = "until_played"
    END_OF_TURN = "end_of_turn"
    END_OF_COMBAT = "end_of_combat"
    PERMANENT = "permanent"


class CardModifier:
    """Represents a temporary effect on a card"""

    def __init__(self,
                 cost_change: int = 0,
                 damage_multiplier: float = 1.0,
                 timing: EffectTiming = EffectTiming.UNTIL_PLAYED,
                 description: str = ""):
        self.cost_change = cost_change
        self.damage_multiplier = damage_multiplier
        self.timing = timing
        self.description = description


class Card(ABC):
    def __init__(self, card_id: int, tier: int = 0):
        self.card_id = card_id
        self.tier = tier
        self.base_mana_cost = self.get_base_cost(tier)
        self.name = self.get_name(tier)
        self.modifiers: List[CardModifier] = []  # Temporary effects
        self.permanent_cost_change = 0  # From events/upgrades

    @property
    def mana_cost(self) -> int:
        """Calculate actual mana cost with all modifiers"""
        total_cost = self.base_mana_cost + self.permanent_cost_change
        for modifier in self.modifiers:
            total_cost += modifier.cost_change
        return max(0, total_cost)

    def add_modifier(self, modifier: CardModifier):
        """Add a temporary effect to this card"""
        self.modifiers.append(modifier)

    def remove_modifiers_by_timing(self, timing: EffectTiming):
        """Remove modifiers that expire at given timing"""
        self.modifiers = [m for m in self.modifiers if m.timing != timing]

    def modify_cost_permanently(self, amount: int):
        """Permanently modify base cost (from events)"""
        self.permanent_cost_change += amount

    @abstractmethod
    def get_base_cost(self, tier: int) -> int:
        pass

    @abstractmethod
    def get_name(self, tier: int) -> str:
        pass

    @abstractmethod
    def effect(self, game_state, tier: int):
        pass

    def play(self, game_state):
        # Remove "until played" modifiers before playing
        self.remove_modifiers_by_timing(EffectTiming.UNTIL_PLAYED)
        self.effect(game_state, self.tier)

    def upgrade(self):
        self.tier += 1
        self.base_mana_cost = self.get_base_cost(self.tier)
        self.name = self.get_name(self.tier)


class Strike(Card):
    def get_base_cost(self, tier: int) -> int:
        if tier >= 2:
            return 1
        return 2

    def get_name(self, tier: int) -> str:
        if tier == 0:
            return "Strike"
        elif tier == 1:
            return "Precise Strike"
        elif tier == 2:
            return "Overwhelming Strike"
        return f"Strike +{tier}"

    def effect(self, game_state, tier: int):
        base_damage = 3
        damage = base_damage + (tier * 3)

        # Apply damage modifiers
        for modifier in self.modifiers:
            damage = int(damage * modifier.damage_multiplier)

        game_state.deal_damage(damage)


class DrawAndDiscount(Card):

    def get_base_cost(self, tier: int) -> int:
        return 1

    def get_name(self, tier: int) -> str:
        return "Bargain Hunter"

    def effect(self, game_state, tier: int):
        num_cards = 3 + tier
        drawn_cards = game_state.draw_cards(num_cards)

        discount_modifier = CardModifier(
            cost_change=-2,
            timing=EffectTiming.UNTIL_PLAYED,
            description="Costs 2 less (until played)"
        )

        for card in drawn_cards:
            card.add_modifier(discount_modifier)


class BattleRage(Card):

    def get_base_cost(self, tier: int) -> int:
        return 1

    def get_name(self, tier: int) -> str:
        return "Battle Rage"

    def effect(self, game_state, tier: int):
        damage_boost = CardModifier(
            damage_multiplier=1.5 + (tier * 0.25),
            timing=EffectTiming.END_OF_TURN,
            description="+50% damage this turn"
        )

        for card in game_state.player.hand:
            card.add_modifier(damage_boost)


class ShieldUp(Card):
    def get_base_cost(self, tier: int) -> int:
        if tier >= 2:
            return 1
        return 2

    def get_name(self, tier: int) -> str:
        if tier == 0:
            return "Shield Up"
        elif tier == 1:
            return "Shield Wall"
        return f"Shield Up +{tier}"

    def effect(self, game_state, tier: int):
        base_defense = 3
        defend = base_defense + (tier * 3)
        game_state.protect(defend)

""" // intended implementation - at least what I had in mind
CARD_REGISTRY: Dict[int, type] = {
    1: Strike,
    2: ShieldUp,
}


def create_card(card_id: int, tier: int = 0) -> Card:
    card_class = CARD_REGISTRY[card_id]
    return card_class(card_id, tier)


def get_random_card_ids(n: int) -> List[int]:
    pool = list(CARD_REGISTRY.keys())
    return random.sample(pool, min(n, len(pool)))
"""