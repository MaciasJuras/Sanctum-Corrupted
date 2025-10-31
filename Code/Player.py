"""
from . import Character
from . import Card

class Player(Character):

    #The Player class, inheriting all logic from Character and adding player-specific controls and attributes (like mana).

    def __init__(self, name, health, mana, full_deck: list[Card]):
        super().__init__(name, health, full_deck)
        self.mana = mana
        self.max_mana = mana

    def start_turn(self):
        print(f"\n--- {self.name}'s Turn ---")
        self.draw_cards(self.max_cards - len(self.hand))
        self.show_hand()

    def show_hand(self):
        #Prints the player's current hand to the console for now - need to be changed when we will have assets
        print(f"{self.name}'s Hand:")
        if not self.hand:
            print("  (No cards in hand)")
            return

        for i, card in enumerate(self.hand):
            print(f"  {i + 1}: {card.name} (Cost: {card.cost}) - {card.description}")

    def choose_card_to_play(self, target: Character):
        #Uses console input for now - need to be changed when we will have assets
        playable_cards = [card for card in self.hand if card.cost <= self.mana]
        if not playable_cards:
            print("You don't have enough mana to play any card. Your turn ends")
            return False

        while True:
            try:
                choice = input(f"Choose a card from the hand (1-indexed) or '0' to end turn: ")
                if choice == '0':
                    print(f"{self.name} ends their turn.")
                    return False

                chosen_index = int(choice)-1

                if 0 <= chosen_index < len(self.hand):
                    chosen_card = self.hand[chosen_index]

                    if  chosen_card.cost > self.mana:
                        print(f"Not enough mana to play {chosen_card}")
                        continue

                    self.mana -= chosen_card.cost
                    print(f"{self.name} spends {chosen_card.cost} mana. ({self.mana} remaining)")
                    self.play_card(chosen_card, target)
                    return True
                else:
                    print("Invalid choice. Please pick a number from your hand.")

            except ValueError:
                print("Invalid input. Please enter a number.")

    def end_battle(self):
        self.mana = self.max_mana
        #add getting reward at the end of won battle
"""