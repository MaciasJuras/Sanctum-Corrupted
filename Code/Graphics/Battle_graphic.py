from Code.Settings import *
from Code.Cards import Card
from Code.Settings import WINDOW_WIDTH, WINDOW_HEIGHT
from Code.GameState import Battle_mode
import os

TARGET_CARD_WIDTH = 120
CARD_SPACING = -10
CARD_SPACE_FROM_BOTTOM_SCREEN = 0.5

def draw_battle_background(display_surface, bg_name):
    battle_background_path = join('Assets/Images/Battle', bg_name)

    if os.path.exists(battle_background_path):
        bg_image = pygame.image.load(battle_background_path).convert()
        bg_image = pygame.transform.scale(bg_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        display_surface.blit(bg_image, (0, 0))
    else:
        print(f"Error: Background not found at {battle_background_path}")
        display_surface.fill((0, 0, 0))


def display_card(card, position, display_surface):
    if card.graphic is None:
        card_image = card.generate_card_image()
        if card_image:
            mode = card_image.mode
            size = card_image.size
            data = card_image.tobytes()

            original_surface = pygame.image.fromstring(data, size, mode)
            original_width, original_height = original_surface.get_size()

            ratio = original_height / original_width
            target_height = int(TARGET_CARD_WIDTH * ratio)
            card.graphic = pygame.transform.smoothscale(original_surface, (TARGET_CARD_WIDTH, target_height))

        else:
            print(f"Failed to generate image for card: {card.name}")

    if card.graphic:
        display_surface.blit(card.graphic, position)

def display_cards_in_hand(hand: list[Card], display_surface):
    total_width = len(hand) * (TARGET_CARD_WIDTH + CARD_SPACING) - CARD_SPACING
    start_x = (display_surface.get_width() - total_width) // 2

    estimated_height = int(TARGET_CARD_WIDTH * 1.4)
    y = display_surface.get_height() - estimated_height - CARD_SPACE_FROM_BOTTOM_SCREEN

    for i, card in enumerate(hand):
        x = start_x + (i * (TARGET_CARD_WIDTH + CARD_SPACING))
        card.position = pygame.Rect(x, y, TARGET_CARD_WIDTH, estimated_height)
        display_card(card, (x, y), display_surface)


def update_battle_sequence(player, enemy, display_surface):
    """
    Main Battle Animation Loop.
    Handles the sequence: Player Move -> Effect -> Enemy Move -> Effect -> Cleanup
    """

    # Positions of cards in a center
    estimated_card_height = int(TARGET_CARD_WIDTH * 1.4)
    center_y = (WINDOW_HEIGHT // 2) - (estimated_card_height // 2)
    target_pos_player = ((WINDOW_WIDTH // 2) - 80, center_y)
    target_pos_enemy = ((WINDOW_WIDTH // 2) + 20, center_y)

    move_speed = 25
    cleanup_speed = 35

    # --- PHASE 1: PLAYER ANIMATION ---
    if Battle_mode.battle_phase == Battle_mode.PHASE_PLAYER_ANIMATION:
        card = player.card_in_play
        if card:
            arrived = animate_move_to(card, target_pos_player, move_speed)
            display_card(card, (card.position.x, card.position.y), display_surface)

            if arrived:
                Battle_mode.apply_player_effect(player, enemy)
                Battle_mode.battle_phase = Battle_mode.PHASE_ENEMY_CHOOSE

    # --- PHASE 2: ENEMY CHOOSES CARD ---
    elif Battle_mode.battle_phase == Battle_mode.PHASE_ENEMY_CHOOSE:
        # Render player card waiting in center      ??? już jest wyświetlone
        if player.card_in_play:
            display_card(player.card_in_play, (player.card_in_play.position.x, player.card_in_play.position.y),
                         display_surface)

        has_card = Battle_mode.prepare_enemy_turn(enemy)

        if has_card:
            Battle_mode.battle_phase = Battle_mode.PHASE_ENEMY_ANIMATION
        else:
            # Enemy didn't play card
            Battle_mode.battle_phase = Battle_mode.PHASE_CLEANUP

    # --- PHASE 3: ENEMY ANIMATION ---
    elif Battle_mode.battle_phase == Battle_mode.PHASE_ENEMY_ANIMATION:
        # Keep drawing player card static
        if player.card_in_play:     #??? już jest wyświetlone
            display_card(player.card_in_play, (player.card_in_play.position.x, player.card_in_play.position.y),
                         display_surface)

        card = enemy.card_in_play
        if card:
            arrived = animate_move_to(card, target_pos_enemy, move_speed)
            display_card(card, (card.position.x, card.position.y), display_surface)

            if arrived:
                Battle_mode.apply_enemy_effect(player, enemy)
                Battle_mode.battle_phase = Battle_mode.PHASE_CLEANUP

    # --- PHASE 4: CLEANUP (Discard Animation) ---
    elif Battle_mode.battle_phase == Battle_mode.PHASE_CLEANUP:

        finished_p = True
        finished_e = True

        # Move Player Card to bottom-left
        if player.card_in_play:
            finished_p = animate_move_to(player.card_in_play, (100, WINDOW_HEIGHT + 200), cleanup_speed)
            display_card(player.card_in_play, (player.card_in_play.position.x, player.card_in_play.position.y),
                         display_surface)

            if finished_p:
                player.discard_pile.append(player.card_in_play)
                player.card_in_play = None

        # Move Enemy Card to top-right (Discard)
        if enemy.card_in_play:
            finished_e = animate_move_to(enemy.card_in_play, (WINDOW_WIDTH - 100, -200), cleanup_speed)
            display_card(enemy.card_in_play, (enemy.card_in_play.position.x, enemy.card_in_play.position.y),
                         display_surface)

            if finished_e:
                enemy.discard_pile.append(enemy.card_in_play)
                enemy.card_in_play = None

        if finished_p and finished_e:
            Battle_mode.battle_phase = Battle_mode.PHASE_IDLE
            print("Turn complete. Waiting for player input.")


def animate_move_to(card, target, speed):
    """Helper to move card rect toward target (x,y). Returns True if arrived."""
    tx, ty = target

    # if card position is missing
    if not hasattr(card, 'position') or card.position is None:
        card.position = pygame.Rect(0, 0, TARGET_CARD_WIDTH, int(TARGET_CARD_WIDTH * 1.4))

    cx, cy = card.position.x, card.position.y

    dist_x = tx - cx
    dist_y = ty - cy

    # Check if close enough to snap
    if abs(dist_x) < speed and abs(dist_y) < speed:
        card.position.x = tx
        card.position.y = ty
        return True

    import math
    dist = math.hypot(dist_x, dist_y)
    if dist != 0:
        card.position.x += (dist_x / dist) * speed
        card.position.y += (dist_y / dist) * speed

    return False