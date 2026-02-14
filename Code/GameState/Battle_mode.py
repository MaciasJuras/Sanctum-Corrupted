import pygame

from Code.Graphics.Battle_graphic import *

# =============================================================================
# FEATURE TOGGLE - Set to False to revert to single-card-per-turn behavior
# =============================================================================
MULTI_CARD_MODE = True  # True = play multiple cards per turn, False = one card then enemy responds

# --- Battle State Constants ---
PHASE_IDLE = 0  # Waiting for player input
PHASE_PLAYER_ANIMATION = 1  # Player card moving to center
PHASE_PLAYER_CARD_RESOLVE = 2  # Player card effect resolving
PHASE_ENEMY_TURN_START = 3  # Enemy turn begins (draw cards, refill mana)
PHASE_ENEMY_CHOOSE = 4  # Enemy picks a card to play
PHASE_ENEMY_ANIMATION = 5  # Enemy card moving to center
PHASE_ENEMY_CARD_RESOLVE = 6  # Enemy card effect resolving
PHASE_CLEANUP = 7  # Cards moving to discard piles
PHASE_PLAYER_TURN_START = 8  # Player turn begins

battle_phase = PHASE_IDLE
timer_start = 0  # To manipulate time in battle

# Track whose turn it is
is_player_turn = True

# Track cards played this turn for cleanup
player_cards_to_discard = []
enemy_cards_to_discard = []


def handle_enemy_interaction(enemy_sprites, player):
    """ Checks for SPACE key press and direct collision with an enemy
        to initiate a battle."""
    keys = pygame.key.get_pressed()
    space_pressed = keys[pygame.K_SPACE]

    if space_pressed and not player.in_battle:
        colliding_enemy = pygame.sprite.spritecollideany(player, enemy_sprites)

        if colliding_enemy:
            player.in_battle = True
            return colliding_enemy, True

    return None, space_pressed


def handle_battle_exit(player, e_pressed_last_frame):
    keys = pygame.key.get_pressed()
    e_pressed = keys[pygame.K_e]

    if e_pressed and not e_pressed_last_frame:
        print("Exiting battle mode!")
        player.in_battle = False
        player.end_battle(False)

    return e_pressed


def handle_card_selection(player, mouse_pressed_last_frame):
    """
    Detects if the player clicked on a card in their hand.
    Returns the new state of the mouse button (to prevent multi-clicks).
    """
    global battle_phase, is_player_turn
    mouse_pressed = pygame.mouse.get_pressed()[0]

    # Only allow card selection during player's turn in IDLE phase
    if not is_player_turn:
        return mouse_pressed

    if mouse_pressed and not mouse_pressed_last_frame and battle_phase == PHASE_IDLE:
        mouse_pos = pygame.mouse.get_pos()

        for card in player.hand:
            # Check collision with the card's visual rect
            if card.position and card.position.collidepoint(mouse_pos):
                if player.mana < card.mana_cost:
                    print(f"Not enough Mana! Cost: {card.mana_cost}, Have: {player.mana}")
                    return mouse_pressed

                print(f"Clicked on: {card.name}")

                if card in player.hand:
                    player.mana -= card.mana_cost
                    player.hand.remove(card)
                    print(f"Player mana = {player.mana}")

                player.card_in_play = card
                battle_phase = PHASE_PLAYER_ANIMATION
                break

    return mouse_pressed


def handle_end_turn_button(player, enemy, mouse_pressed_last_frame):
    """
    Handles clicking the End Turn button.
    Returns the new mouse state.
    """
    global battle_phase, is_player_turn
    mouse_pressed = pygame.mouse.get_pressed()[0]

    # Only check during player's idle phase
    if not is_player_turn or battle_phase != PHASE_IDLE:
        return mouse_pressed

    if mouse_pressed and not mouse_pressed_last_frame:
        mouse_pos = pygame.mouse.get_pos()
        button_rect = get_end_turn_button_rect()

        if button_rect.collidepoint(mouse_pos):
            print("=== Player ends turn ===")
            # Discard remaining hand
            player.end_turn()

            # Switch to enemy turn
            is_player_turn = False
            battle_phase = PHASE_ENEMY_TURN_START

    return mouse_pressed


def start_player_turn(player):
    """Initialize player's turn - draw cards, refill mana."""
    global battle_phase, is_player_turn
    is_player_turn = True
    player.start_turn()
    battle_phase = PHASE_IDLE
    print(f"[{player.name}] Health: {player.health}/{player.max_health}")


def start_enemy_turn(enemy):
    """Initialize enemy's turn - draw cards, refill mana."""
    global battle_phase
    enemy.start_turn()
    battle_phase = PHASE_ENEMY_CHOOSE
    print(f"[{enemy.name}] Health: {enemy.health}/{enemy.max_health}")


# --- BATTLE LOGIC ---

def apply_player_effect(player, enemy):
    """Called when player card hits the center."""
    global battle_phase, player_cards_to_discard
    if player.card_in_play:
        print(f"Player effect: {player.card_in_play.name}")
        player.card_in_play.play([player, enemy])

        if enemy.health <= 0:
            player.end_battle(True)
            player.in_battle = False
            enemy.kill()
            battle_phase = PHASE_IDLE
            return True  # Battle ended

        # Track card for discard
        player_cards_to_discard.append(player.card_in_play)

        # In single card mode, draw 1 card after playing
        if not MULTI_CARD_MODE:
            player.draw_cards(1)

    return False  # Battle continues


def prepare_enemy_card(enemy, player, enemy_hand_positions):
    enemy_card = enemy.choose_card_to_play(player)

    if enemy_card:
        if enemy_card in enemy.hand:
            enemy.hand.remove(enemy_card)
            enemy.mana -= enemy_card.mana_cost
            print(f"Enemy mana = {enemy.mana}")

        if enemy_hand_positions and enemy_card in enemy_hand_positions:
            start_x, start_y = enemy_hand_positions[enemy_card]
        else:
            start_x, start_y = (WINDOW_WIDTH // 2, 0)

        enemy.card_in_play = enemy_card
        enemy.card_in_play.position = pygame.Rect(start_x, start_y, TARGET_CARD_WIDTH, int(TARGET_CARD_WIDTH * 1.4))

        return True
    return False


def apply_enemy_effect(player, enemy):
    """Called when enemy card hits the center."""
    global battle_phase, enemy_cards_to_discard
    if enemy.card_in_play:
        print(f"Enemy effect: {enemy.card_in_play.name}")
        enemy.card_in_play.play([enemy, player])

        if player.health <= 0:
            player.end_battle(False)
            player.in_battle = False
            battle_phase = PHASE_IDLE
            return True  # Battle ended

        # Track card for discard
        enemy_cards_to_discard.append(enemy.card_in_play)

        # In single card mode, enemy draws 1 card after playing
        if not MULTI_CARD_MODE:
            enemy.draw_cards(1)

    return False  # Battle continues


def reset_battle_state():
    """Reset battle state for a new battle."""
    global battle_phase, is_player_turn, player_cards_to_discard, enemy_cards_to_discard, timer_start
    battle_phase = PHASE_IDLE
    is_player_turn = True
    player_cards_to_discard = []
    enemy_cards_to_discard = []
    timer_start = 0