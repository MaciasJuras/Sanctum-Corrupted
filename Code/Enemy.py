import random

from Code.Character import Character
from Code.Cards import Card

class Enemy(Character):
        #The Enemy class, inheriting all logic from Character and adding its own AI logic for choosing cards.

    def __init__(self, name, health, mana, full_deck: list[Card]):
        super().__init__(name, health, full_deck)
        self.mana = mana
        self.max_mana = mana

    def start_turn(self):
        print(f"\n--- {self.name}'s Turn ---")
        self.draw_cards(self.max_cards - len(self.hand))
        print(f"[{self.name}] Health: {self.health}/{self.max_health}")

    def choose_card_to_play(self, target: Character):
        #AI logic will be implemented here. For now It's just random choice
        playable_cards = [card for card in self.hand if card.cost <= self.mana]
        if not playable_cards:
            print(f"[{self.name}] has no playable cards and ends its turn.")
            return False
        chosen_card = random.choice(playable_cards)
        self.mana -= chosen_card.cost
        self.play_card(chosen_card, target)
        return True