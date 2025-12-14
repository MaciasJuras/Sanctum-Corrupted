import random
import pygame

from Code.Character.Character import Character
from Code.Cards.Card import Card

class Enemy(pygame.sprite.Sprite, Character):
        #The Enemy class, inheriting all logic from Character and adding its own AI logic for choosing cards.

    def __init__(self, pos, groups, name, health, mana, full_deck: list[Card]):
        pygame.sprite.Sprite.__init__(self, groups)
        Character.__init__(self, name, health, full_deck if full_deck else [])
        self.mana = mana
        self.max_mana = mana
        self.card_in_play = None

        self.image = pygame.Surface((64, 64))  # Placeholder size
        self.image.fill((100, 100, 100))  # Generic gray placeholder

        self.rect = self.image.get_frect(center=pos)
        self.position = pygame.math.Vector2(pos)

    def start_turn(self):
        print(f"\n--- {self.name}'s Turn ---")
        self.draw_cards(self.max_cards - len(self.hand))
        print(f"[{self.name}] Health: {self.health}/{self.max_health}")

    def choose_card_to_play(self):
        #AI logic will be implemented here. For now It's just random choice
        playable_cards = [card for card in self.hand if card.mana_cost <= self.mana]
        if not playable_cards:
            print(f"[{self.name}] has no playable cards and ends its turn.")
            return None
        chosen_card = random.choice(playable_cards)
        return chosen_card

    def end_battle(self):
        pass

class MagicRat(Enemy):
        def __init__(self, pos, groups, name, health, mana, full_deck: list[Card]):
            super().__init__(pos, groups, name, health, mana, full_deck)
            self.mana = mana
            image_path = "Assets/Images/Enemies/magic-rat.png"

            try:
                self.image = pygame.image.load(image_path).convert_alpha()
            except pygame.error:
                # Fallback if image path is bad
                self.image = pygame.Surface((64, 64))
                self.image.fill((0, 0, 255))

            self.rect = self.image.get_frect(center=pos)


class TechRat(Enemy):
    def __init__(self, pos, groups, name, health, mana, full_deck: list[Card]):
        super().__init__(pos, groups, name, health, mana, full_deck)
        self.mana = mana
        image_path = "Assets/Images/Enemies/tech-rat.png"

        try:
            self.image = pygame.image.load(image_path).convert_alpha()
        except pygame.error:
            # Fallback if image path is bad
            self.image = pygame.Surface((64, 64))
            self.image.fill((0, 0, 255))

        self.rect = self.image.get_frect(center=pos)