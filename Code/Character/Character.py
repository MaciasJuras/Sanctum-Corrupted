import random
from abc import ABC, abstractmethod

from Code.Cards.Card import Card

class Character(ABC):

    #An abstract base class for any combatant in the game.

    def __init__(self, name, health, full_deck: list[Card]):
        self.name = name
        self.health = health
        self.max_health = health

        #Cards
        self.full_deck = full_deck
        self.draw_pile = []
        self.hand = []
        self.discard_pile = []
        self.max_cards = 10

    def start_battle(self):
        self.draw_pile = self.full_deck.copy()
        random.shuffle(self.draw_pile)
        self.hand = []
        self.discard_pile = []
        print(f"{self.name}'prepares for battle")

    def draw_cards(self, number_to_draw):
        for _ in range(number_to_draw):
            if not self.draw_pile:
                if not self.discard_pile:
                    print(f"[{self.name}] is out of cards to draw!")
                    break
                print(f"[{self.name}] shuffles their discard pile.")
                self.draw_pile = self.discard_pile.copy()
                self.discard_pile = []
                random.shuffle(self.draw_pile)
        card = self.draw_pile.pop()
        self.hand.append(card)
        print(f"[{self.name}] drew {card.name}.")

    def play_card(self, card: Card, target):
        card.play(self, [self, target])
        self.hand.remove(card)
        self.discard_pile.append(card)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            print(f"[{self.name}] takes {amount} damage, 0 HP remaining.")
            print(f"[{self.name}] lose")
        else:
            print(f"[{self.name}] takes {amount} damage, {self.health} HP remaining.")

    def heal(self, amount):
        self.health += amount
        if self.health >= self.max_health:
            self.health = self.max_health
        print(f"[{self.name}] heals, {amount} HP remaining.")

    @abstractmethod
    def start_turn(self):
        pass

    @abstractmethod
    def choose_card_to_play(self, target):
        pass

    @abstractmethod
    def end_battle(self):
        pass
