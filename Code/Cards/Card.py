from abc import ABC, abstractmethod
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, List, Callable
import random
import os
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
        self.position = None    #position of a card in a screen
        self.graphic = None

    @abstractmethod
    def get_image_path(self) -> str:
        pass

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
    def get_effect_value(self, tier: int) -> int:
        pass

    @abstractmethod
    def effect(self, game_state, tier: int):
        pass

    def play(self, game_state):
        # Remove "until played" modifiers before playing
        self.effect(game_state, self.tier)
        self.remove_modifiers_by_timing(EffectTiming.UNTIL_PLAYED)

    def upgrade(self):
        self.tier += 1
        self.base_mana_cost = self.get_base_cost(self.tier)
        self.name = self.get_name(self.tier)

    def draw_text_centered(self, draw: ImageDraw.ImageDraw, text: str, center_x: int, center_y: int, font):
        """Draws text centered on a target (X, Y) point."""

        color = (255, 255, 255, 255)

        left, top, right, bottom = draw.textbbox((0, 0), text, font)

        start_x = center_x - ((right - left) / 2)
        start_y = center_y - ((bottom - top) / 2)

        draw.text((start_x, start_y), text, font=font, fill=color)

    def generate_card_image(self):
        """
        Generates a card image from a Card object instance.
        """
        font = 'Assets/Font/Jersey10.ttf'

        NAME_FONT_SIZE = 40
        MANA_FONT_SIZE = 40
        VALUE_FONT_SIZE = 40

        template_path = self.get_image_path()

        if not os.path.exists(template_path):
            print(f"Error: Template file not found at '{template_path}'.")
            return None

        img = None
        try:
            img = Image.open(template_path).convert("RGBA")
            draw = ImageDraw.Draw(img)

            try:
                name_font = ImageFont.truetype(font, NAME_FONT_SIZE)
                mana_font = ImageFont.truetype(font, MANA_FONT_SIZE)
                value_font = ImageFont.truetype(font, VALUE_FONT_SIZE)
            except IOError:
                try:
                    font_name = "arial.ttf"
                    print(f"Jersey10.ttf not found. Switching to {font_name}")
                    name_font = ImageFont.truetype(font_name, NAME_FONT_SIZE)
                    mana_font = ImageFont.truetype(font_name, MANA_FONT_SIZE)
                    value_font = ImageFont.truetype(font_name, VALUE_FONT_SIZE)
                except IOError:
                    print(f"Warning: No fonts found. Using default font.")
                    name_font = ImageFont.load_default()
                    mana_font = ImageFont.load_default()
                    value_font = ImageFont.load_default()

            # Reduce name size slightly if the text is very long
            if len(self.get_name(self.tier)) > 10:
                name_font = ImageFont.truetype(font, int(NAME_FONT_SIZE * 0.8))

            self.draw_text_centered(draw, str(self.get_base_cost(self.tier)), 30, 30, mana_font)
            self.draw_text_centered(draw, self.get_name(self.tier), 143, 38, name_font)
            self.draw_text_centered(draw, str(self.get_effect_value(self.tier)), 246, 313, value_font)
        except Exception as e:
            print(f"An unexpected error occurred during image generation: {e}")

        return img