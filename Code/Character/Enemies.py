import random
import pygame

from Code.Character.Enemy import Enemy
from Code.Cards.Card import *

class Rat(Enemy):
    def __init__(self, pos, groups, name, health, full_deck: list[Card], tier, school: School = School.MAGICAL):
        super().__init__(pos, groups, name, health, full_deck, tier, school)

        if self.school == School.MAGICAL:
            image_path = "Assets/Images/Enemies/magic-rat.png"
        else:  # TECHNICAL
            image_path = "Assets/Images/Enemies/tech-rat.png"

        try:
            self.image = pygame.image.load(image_path).convert_alpha()
        except pygame.error:
            # Fallback if image path is bad
            self.image = pygame.Surface((64, 64))
            self.image.fill((0, 0, 255))

        self.rect = self.image.get_frect(center=pos)

    def get_max_health(self, tier: int) -> int:
        if self.school == School.TECHNICAL:
            health = 5 + (tier * 2)
        else:
            health = 7 + (tier * 3)
        return health

    def get_max_mana(self, tier: int) -> int:
        if self.school == School.MAGICAL:
            max_mana = 5 + (tier * 2)
        else:
            max_mana = 7 + (tier * 3)
        return max_mana

    def get_name(self, tier: int) -> str:
        if self.school == School.MAGICAL:
            names = {0: "Magic Rat", 1: "MR", 2: "VMR"}
        else:  # TECHNICAL
            names = {0: "Tech Rat", 1: "TR", 2: "TMR"}
        return names.get(tier, f"Rat {tier}")


class Cat(Enemy):
    def __init__(self, pos, groups, name, health, full_deck: list[Card], tier, school: School = School.MAGICAL):
        super().__init__(pos, groups, name, health, full_deck, tier, school)

        if self.school == School.MAGICAL:
            image_path = "Assets/Images/Enemies/magic-cat.png"
        else:  # TECHNICAL
            image_path = "Assets/Images/Enemies/tech-cat.png"

        try:
            self.image = pygame.image.load(image_path).convert_alpha()
        except pygame.error:
            # Fallback if image path is bad
            self.image = pygame.Surface((64, 64))
            self.image.fill((0, 0, 255))

        self.rect = self.image.get_frect(center=pos)

    def get_max_health(self, tier: int) -> int:
        if self.school == School.TECHNICAL:
            health = 7 + (tier * 2)
        else:
            health = 9 + (tier * 3)
        return health

    def get_max_mana(self, tier: int) -> int:
        if self.school == School.MAGICAL:
            max_mana = 7 + (tier * 2)
        else:
            max_mana = 9 + (tier * 3)
        return max_mana

    def get_name(self, tier: int) -> str:
        if self.school == School.MAGICAL:
            names = {0: "Magic Cat", 1: "MR", 2: "VMR"}
        else:  # TECHNICAL
            names = {0: "Tech Cat", 1: "TR", 2: "TMR"}
        return names.get(tier, f"Cat {tier}")
