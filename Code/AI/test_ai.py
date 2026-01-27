import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from Code.Character.enemy_ai import EnemyAI
from Code.Character.Enemies import Cat
from Code.Character.Player import Player
from Code.Cards.Card import School


def test_ai_integration():
    print("Testing AI Integration...")

    import pygame
    pygame.init()
    pygame.display.set_mode((1, 1))

    player = Player((0, 0), [], [], 'Test Player', health=60, mana=50)
    enemy = Cat((0, 0), [], 'Test Cat', 100, [], tier=0, school=School.MAGICAL)
    enemy.new_game_starting_package()

    player.start_battle(enemy)
    enemy.start_battle()
    enemy.start_turn()

    print(f"Player: {player.health} HP, {player.mana} mana")
    print(f"Enemy: {enemy.health} HP, {enemy.mana} mana")
    print(f"Enemy hand: {[card.name for card in enemy.hand]}")

    ai = EnemyAI()
    action = ai.choose_action(enemy, player)
    card = ai.get_card_from_action(action, enemy)

    if card:
        print(f"AI chose: {card.name} (Cost: {card.mana_cost})")
    else:
        print("AI chose to pass")

    print("AI integration test passed!")

    pygame.quit()


if __name__ == "__main__":
    test_ai_integration()