import random
from abc import ABC, abstractmethod
from Code.Cards.Card import *
from Code.Cards.card_registry import *
from Code.Cards.card_ids import *

# === BATTLE CONFIGURATION ===
CARDS_PER_TURN = 5  # Cards drawn at start of each turn
MAX_MANA_CAP = 5  # Maximum mana cap
STARTING_MAX_MANA = 1  # Max mana on turn 1


class Character(ABC):

    # An abstract base class for any combatant in the game.

    def __init__(self, name, health, full_deck: list[Card]):
        self.name = name
        self.health = health
        self.max_health = health

        # Cards
        self.full_deck = full_deck
        self.draw_pile = []
        self.hand = []
        self.discard_pile = []
        self.max_cards = 10

        # Mana system - will be initialized in start_battle
        self.mana = 0
        self.max_mana = 0
        self.current_max_mana = STARTING_MAX_MANA  # Grows each turn
        self.turn_number = 0

        # Defensive stats
        self.block = 0  # Temporary shield, absorbs damage before health, resets each turn
        self.dodge = 0  # Number of attacks that can be completely avoided
        self.dodge_triggered = False  # Flag for UI to show "Dodged!" text

        # Status effects
        self.regeneration = []  # List of (heal_amount, remaining_turns)
        self.thorns = []  # List of (damage, remaining_stacks)

    def get_new_card(self, tier, school_name):
        school_enum = School[school_name]
        card = create_card(get_random_card_ids(1)[0], tier, school_enum)
        self.full_deck.append(card)

    def new_game_starting_package(self):
        pass
        # for _ in range(15):
        #     self.get_new_card(0, 'NORMAL')

    def start_battle(self):
        for card in self.full_deck:
            card.graphic = None
            card.position = None
        self.draw_pile = self.full_deck.copy()
        random.shuffle(self.draw_pile)
        self.hand = []
        self.discard_pile = []
        self.turn_number = 0
        self.current_max_mana = STARTING_MAX_MANA
        self.mana = 0

        # Reset defensive stats for new battle
        self.block = 0
        self.dodge = 0
        self.dodge_triggered = False
        self.regeneration = []
        self.thorns = []

        print(f"{self.name} prepares for battle")

    def draw_cards(self, amount: int):
        for _ in range(amount):
            if len(self.hand) >= self.max_cards:
                print(f"[{self.name}] Hand is full ({self.max_cards})! Cannot draw more.")
                break
            if not self.draw_pile:
                if not self.discard_pile:
                    print(f"[{self.name}] is out of cards to draw!")
                    break
                print(f"[{self.name}] shuffles their discard pile.")
                for card in self.discard_pile:
                    card.graphic = None
                    card.position = None
                self.draw_pile = self.discard_pile.copy()
                self.discard_pile = []
                random.shuffle(self.draw_pile)
            if self.draw_pile:
                card = self.draw_pile.pop()
                self.hand.append(card)
                print(f"[{self.name}] drew {card.name} (Tier {card.tier}).")
            else:
                print("ERROR while drawing cards.")

    def play_card(self, card: Card, target):
        card.play([self, target])
        if card in self.hand:
            self.hand.remove(card)
            self.discard_pile.append(card)
        else:
            print(
                f"ERROR: {card.name} was played, but it was not in the hand (Possible double-trigger in animation loop).")

    def start_turn(self):
        """Called at the start of each turn. Increases mana cap, refills mana, draws cards."""
        self.turn_number += 1

        # Increase max mana (up to cap)
        if self.current_max_mana < MAX_MANA_CAP:
            self.current_max_mana = min(self.turn_number, MAX_MANA_CAP)

        # Refill mana to current max
        self.mana = self.current_max_mana

        print(f"\n--- {self.name}'s Turn {self.turn_number} ---")
        print(f"[{self.name}] Mana: {self.mana}/{self.current_max_mana}")

        # Reset block at the start of turn (temporary shield)
        if self.block > 0:
            print(f"[{self.name}] Block fades: {self.block} -> 0")
            self.block = 0

        # Apply regeneration effects
        self._apply_regeneration()

        # Draw cards for this turn
        self.draw_cards(CARDS_PER_TURN)

    def _apply_regeneration(self):
        """Apply all active regeneration effects and decrement their duration."""
        if not self.regeneration:
            return

        total_heal = 0
        remaining_regen = []

        for heal_amount, duration in self.regeneration:
            total_heal += heal_amount
            if duration > 1:
                remaining_regen.append((heal_amount, duration - 1))

        self.regeneration = remaining_regen

        if total_heal > 0:
            self.heal(total_heal)
            print(f"[{self.name}] Regeneration heals for {total_heal}!")

    def end_turn(self):
        """Called at the end of each turn. Discards entire hand."""
        # Move all cards from hand to discard pile, clearing their visual state
        for card in self.hand:
            card.position = None  # Clear position so it doesn't draw in old location
            card.graphic = None  # Clear graphic so it regenerates if needed
            self.discard_pile.append(card)
        self.hand = []
        print(f"[{self.name}] discards hand. End of turn.")

    def end_battle(self, win):
        self.mana = self.max_mana
        self.health = self.max_health
        if win:
            print("You win!")
            self.get_new_card(0, 'NORMAL')
        else:
            print("You lost!")

    # --- Combat / Damage Cards effects ---
    def deal_damage(self, damage: int, ignore_armor: bool = False):
        """
        Takes damage, applying defensive mechanics in order:
        1. Dodge - 20% chance to completely avoid the attack (consumed when triggered)
        2. Block - absorbs damage before health (temporary shield, resets each turn)
        3. Health - remaining damage hits HP
        """
        # Check for dodge (20% chance to avoid if active)
        if self.dodge > 0:
            if random.random() < 0.2:  # 20% chance
                self.dodge = 0  # Consume dodge when it triggers
                self.dodge_triggered = True  # Flag for UI to show "Dodged!" text
                print(f"[{self.name}] dodged the attack! (20% chance triggered)")
                return  # Attack completely avoided

        # Apply block (temporary shield)
        if self.block > 0:
            if self.block >= damage:
                self.block -= damage
                print(f"[{self.name}] block absorbs all damage! ({self.block} block remaining)")
                return  # All damage blocked
            else:
                damage -= self.block
                print(f"[{self.name}] block absorbs {self.block} damage, {damage} goes through")
                self.block = 0

        # Apply remaining damage to health
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            print(f"[{self.name}] takes {damage} damage, 0 HP remaining.")
            print(f"[{self.name}] has been defeated!")
        else:
            print(f"[{self.name}] takes {damage} damage, {self.health} HP remaining.")

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
        print(f"[{self.name}] heals for {amount} HP. ({self.health}/{self.max_health})")

    def add_mana(self, amount: int):
        """Used by ManaGain card"""
        if hasattr(self, 'mana'):
            self.mana += amount
            if self.mana > self.current_max_mana:
                self.mana = self.current_max_mana
            print(f"[{self.name}] recovered {amount} Mana. ({self.mana}/{self.current_max_mana})")

    def add_block(self, amount: int):
        """Used by ShieldUp, Parry, Dodge, etc."""
        self.block += amount
        print(f"[{self.name}] gained {amount} Block. (Total: {self.block})")

    def add_dodge(self, amount: int):
        """Used by Dodge - max 1 instance, gives 20% chance to avoid damage"""
        if self.dodge == 0:
            self.dodge = 1
            print(f"[{self.name}] gained Dodge! (20% chance to avoid attacks)")
        else:
            print(f"[{self.name}] already has Dodge active.")

    def add_armor(self, amount: int):
        """Used by ArmorUp"""
        print(f"[{self.name}] gained {amount} Armor.")
        pass

    def add_thorns(self, damage: int, stacks: int):
        """Used by CounterAttack"""
        self.thorns.append((damage, stacks))
        print(f"[{self.name}] gained {damage} Thorns ({stacks} stacks).")

    def add_regeneration(self, heal_amount: int, duration: int):
        """Used by Regeneration"""
        self.regeneration.append((heal_amount, duration))
        print(f"[{self.name}] gained Regeneration: {heal_amount} HP for {duration} turns.")

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