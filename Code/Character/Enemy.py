import random
import pygame

from Code.Character.Character import Character, STARTING_MAX_MANA
from Code.Cards.Card import *

class Enemy(pygame.sprite.Sprite, Character):
        #The Enemy class, inheriting all logic from Character and adding its own AI logic for choosing cards.

    def __init__(self, pos, groups, name, health, full_deck: list[Card], tier, school: School = School.MAGICAL): #there are no NORMAL enemies
        pygame.sprite.Sprite.__init__(self, groups)
        Character.__init__(self, name, health, full_deck if full_deck else [])

        self.card_in_play = None
        self.tier = tier
        self.school = school

        self.max_mana = self.get_max_mana(tier)
        self.mana = STARTING_MAX_MANA
        self.current_max_mana = STARTING_MAX_MANA

        self.image = pygame.Surface((64, 64))  # Placeholder size
        self.image.fill((100, 100, 100))  # Generic gray placeholder

        self.rect = self.image.get_frect(center=pos)
        self.position = pygame.math.Vector2(pos)

    @abstractmethod
    def get_max_health(self, tier: int) -> int:
        pass

    @abstractmethod
    def get_max_mana(self, tier: int) -> int:
        pass

    @abstractmethod
    def get_name(self, tier: int) -> str:
        pass

    def choose_card_to_play(self):
        #AI logic will be implemented here. For now It's just random choice
        playable_cards = [card for card in self.hand if card.mana_cost <= self.mana]
        if not playable_cards:
            print(f"[{self.name}] has no playable cards and ends its turn.")
            return None
        chosen_card = random.choice(playable_cards)
        return chosen_card

    def end_battle(self, win):
        """Enemy health resets since they're fresh each encounter."""
        self.current_max_mana = STARTING_MAX_MANA
        self.mana = 0
        self.turn_number = 0
        self.health = self.max_health  # Enemies reset health

    def new_game_starting_package(self):
        match self.tier:
            case 0:
                for _ in range(15):
                    self.get_new_card(0, self.school.name)
            case 1:
                for _ in range(15):
                    self.get_new_card(0, self.school.name)
                for _ in range(5):
                    self.get_new_card(1, self.school.name)
            case 2:
                for _ in range(10):
                    self.get_new_card(0, self.school.name)
                for _ in range(5):
                    self.get_new_card(1, self.school.name)
                for _ in range(5):
                    self.get_new_card(2, self.school.name)