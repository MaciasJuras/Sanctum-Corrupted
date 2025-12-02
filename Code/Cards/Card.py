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


class School(Enum):
    """Card school types"""
    NORMAL = "normal"
    MAGICAL = "magical"
    TECHNICAL = "technical"


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
    def __init__(self, card_id: int, tier: int = 0, school: School = School.NORMAL):
        self.card_id = card_id
        self.tier = tier
        self.school = school
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
