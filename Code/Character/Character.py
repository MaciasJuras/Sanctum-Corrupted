import random
from abc import ABC, abstractmethod
from Code.Cards.Card import *
from Code.Cards.card_registry import *
from Code.Cards.card_ids import *

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

    def get_new_card(self, tier, school_name):
        school_enum = School[school_name]
        card = create_card(get_random_card_ids(1)[0],tier,school_enum)
        self.full_deck.append(card)

    def new_game_starting_package(self):
        for _ in range(10):
            self.get_new_card(0, 'NORMAL')

    def start_battle(self):
        self.draw_pile = self.full_deck.copy()
        random.shuffle(self.draw_pile)
        self.hand = []
        self.discard_pile = []
        print(f"{self.name}'prepares for battle")

    def draw_cards(self, amount: int):
        for _ in range(amount):
            if not self.draw_pile:
                if not self.discard_pile:
                    print(f"[{self.name}] is out of cards to draw!")
                    break
                print(f"[{self.name}] shuffles their discard pile.")
                self.draw_pile = self.discard_pile.copy()
                self.discard_pile = []
                random.shuffle(self.draw_pile)
            if self.draw_pile:
                card = self.draw_pile.pop()
                self.hand.append(card)
                print(f"[{self.name}] drew {card.name}.")
            else:
                print("ERROR while drawing cards.")

    def play_card(self, card: Card, target):
        card.play([self, target])
        if card in self.hand:
            self.hand.remove(card)
            self.discard_pile.append(card)
        else:
            print(f"ERROR: {card.name} was played, but it was not in the hand (Possible double-trigger in animation loop).")

    @abstractmethod
    def start_turn(self):
        pass

    @abstractmethod
    def end_battle(self):
        pass

    # --- Combat / Damage Cards effects ---
    def deal_damage(self, damage: int, ignore_armor: bool = False):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            print(f"[{self.name}] takes {damage} damage, 0 HP remaining.")
            print(f"[{self.name}] lose")
        else:
            print(f"[{self.name}] takes {damage} damage, {self.health} HP remaining.")
        print(f"{self.name} took {damage} damage (Ignore Armor: {ignore_armor})")
        pass

    def deal_damage_aoe(self, damage: int):
        """
        Called by AreaAttack.
        Should likely iterate over the character's team or the opposing team.
        """
        print(f"AOE damage of {damage} triggered relative to {self.name}")
        pass

    def get_hp_percent(self) -> float:
        """Used by Execute to check threshold"""
        return 1.0  # Returns 100% by default for now

    # --- Status Effect Cards effects ---

    def apply_poison(self, damage: int, duration: int):
        print(f"Applied poison: {damage} dmg for {duration} turns")
        pass

    def add_next_attack_counter(self, damage: int):
        """Used by Parry"""
        print(f"Next attack will counter for {damage}")
        pass

    def heal(self, amount):
        self.health += amount
        if self.health >= self.max_health:
            self.health = self.max_health
        print(f"[{self.name}] heals, {amount} HP remaining.")

    # --- Deck / Hand Manipulation Cards effects ---

    def draw_cards_special(self, amount: int) -> list:
        """
        Used by DrawCards and DrawAndDiscount.
        Calls the standard draw_cards logic and captures the specific cards added.
        """
        start_count = len(self.hand)
        self.draw_cards(amount)
        drawn_cards = self.hand[start_count:]
        return drawn_cards

    def discard_from_hand(self, amount: int) -> list:
        """
        Used by DiscardForPower and Cycle.
        MUST return a list of discarded cards to prevent crashes.
        """
        print(f"Discarding {amount} cards")
        return []

    def duplicate_card(self, copies: int):
        """Used by Duplicate"""
        print(f"Duplicating a card {copies} times")
        pass

    def upgrade_card_in_hand(self, amount: int):
        """Used by UpgradeCard"""
        print(f"Upgrading a card {amount} times")
        pass

    def exhaust_card(self, card):
        """Used by ExhaustForEffect"""
        print(f"Exhausting card: {card}")
        pass

    def scry(self, look_ahead: int, discard_count: int):
        """Used by Scry"""
        print(f"Scrying top {look_ahead} cards, discarding {discard_count}")
        pass