from Code.Settings import *
from Code.Cards import Card
from Code.Settings import WINDOW_WIDTH, WINDOW_HEIGHT
from Code.GameState import Battle_mode
import os

TARGET_CARD_WIDTH = 120
CARD_SPACING = -10
CARD_SPACE_FROM_BOTTOM_SCREEN = 0.5

PLAYER_PHASE_DELAY = 2000 # 2 seconds
ENEMY_PHASE_DELAY = 2000  # 2 seconds

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

def display_enemy_hand(hand: list[Card], display_surface, enemy_card_in_play=None):
    """Draws the enemy's hand at the top of the screen using the back image."""
    if not hand:
        return

    total_width = len(hand) * (TARGET_CARD_WIDTH + CARD_SPACING) - CARD_SPACING
    start_x = (display_surface.get_width() - total_width) // 2
    y = -10

    estimated_height = int(TARGET_CARD_WIDTH * 1.4)
    card_back_path = 'Assets/Images/Cards/back.png'

    card_positions = {}
    TRANSPARENCY_VALUE = 130

    try:
        back_surf = pygame.image.load(card_back_path).convert_alpha()
        back_surf = pygame.transform.smoothscale(back_surf, (TARGET_CARD_WIDTH, estimated_height))

        back_surf.set_alpha(TRANSPARENCY_VALUE)
        back_surf = pygame.transform.rotate(back_surf, 180)

        for i, card in enumerate(hand):
            x = start_x + (i * (TARGET_CARD_WIDTH + CARD_SPACING))
            card_positions[card] = (x, y)

            if card != enemy_card_in_play:
                display_surface.blit(back_surf, (x, y))

    except Exception as e:
        print(f"Error displaying enemy hand: {e}")

    return card_positions

def update_battle_sequence(player, enemy, display_surface):
    """
    Main Battle Animation Loop.
    Handles the sequence: Player Move -> Effect -> Enemy Move -> Effect -> Cleanup
    """

    # Positions of cards in a center
    estimated_card_height = int(TARGET_CARD_WIDTH * 1.4)
    center_y = (WINDOW_HEIGHT // 2) - (estimated_card_height // 2)
    target_pos_player = ((WINDOW_WIDTH // 2) - 120, center_y)
    target_pos_enemy = ((WINDOW_WIDTH // 2) + 40, center_y)

    # Positions of discard cards
    PADDING_X = 20
    PADDING_Y = 180
    player_discard_target = (WINDOW_WIDTH - TARGET_CARD_WIDTH - PADDING_X,
                             WINDOW_HEIGHT - estimated_card_height - PADDING_Y)
    enemy_discard_target = (PADDING_X, PADDING_Y)
    card_back_path = 'Assets/Images/Cards/back.png'

    move_speed = 25
    cleanup_speed = 35

    # --- PHASE 1: PLAYER ANIMATION ---
    if Battle_mode.battle_phase == Battle_mode.PHASE_PLAYER_ANIMATION:
        card = player.card_in_play
        if card:
            arrived = animate_move_to(card, target_pos_player, move_speed)
            display_card(card, (card.position.x, card.position.y), display_surface)

            if arrived:
                current_time = pygame.time.get_ticks()

                if Battle_mode.timer_start == 0:
                    Battle_mode.timer_start = current_time
                    Battle_mode.apply_player_effect(player, enemy)

                if current_time - Battle_mode.timer_start >= PLAYER_PHASE_DELAY:
                    Battle_mode.battle_phase = Battle_mode.PHASE_ENEMY_CHOOSE
                    Battle_mode.timer_start = 0

    # --- PHASE 2: ENEMY CHOOSES CARD ---
    elif Battle_mode.battle_phase == Battle_mode.PHASE_ENEMY_CHOOSE:
        enemy_hand_positions = display_enemy_hand(enemy.hand, display_surface)
        has_card = Battle_mode.prepare_enemy_turn(enemy, enemy_hand_positions)

        if has_card:
            try:
                back_surf = pygame.image.load(card_back_path).convert_alpha()
                rotated_surf = pygame.transform.rotate(back_surf, 180)
                enemy.card_in_play.graphic = pygame.transform.smoothscale(rotated_surf,
                                                                          (TARGET_CARD_WIDTH, estimated_card_height))
            except:
                pass
            Battle_mode.battle_phase = Battle_mode.PHASE_ENEMY_ANIMATION
        else:
            # Enemy didn't play card
            Battle_mode.battle_phase = Battle_mode.PHASE_CLEANUP

    # --- PHASE 3: ENEMY ANIMATION ---
    elif Battle_mode.battle_phase == Battle_mode.PHASE_ENEMY_ANIMATION:
        if player.card_in_play:
            display_card(player.card_in_play, (player.card_in_play.position.x, player.card_in_play.position.y),
                         display_surface)

        card = enemy.card_in_play
        if card:
            arrived = animate_move_to(card, target_pos_enemy, move_speed)
            display_card(card, (card.position.x, card.position.y), display_surface)

            if arrived:
                card.graphic = None
                current_time = pygame.time.get_ticks()
                if Battle_mode.timer_start == 0:
                    Battle_mode.timer_start = current_time
                    Battle_mode.apply_enemy_effect(player, enemy)
                if current_time - Battle_mode.timer_start >= ENEMY_PHASE_DELAY:
                    Battle_mode.battle_phase = Battle_mode.PHASE_CLEANUP
                    Battle_mode.timer_start = 0

    # --- PHASE 4: CLEANUP (Discard Animation) ---
    elif Battle_mode.battle_phase == Battle_mode.PHASE_CLEANUP:

        finished_p = True
        finished_e = True

        # Move Player Card to bottom-right
        if player.card_in_play:
            finished_p = animate_move_to(player.card_in_play, player_discard_target, cleanup_speed)
            display_card(player.card_in_play, (player.card_in_play.position.x, player.card_in_play.position.y),
                         display_surface)

            if finished_p:
                try:
                    discard_surf = pygame.image.load(card_back_path).convert_alpha()
                    player.card_in_play.graphic = pygame.transform.smoothscale(discard_surf, (TARGET_CARD_WIDTH,
                                                                                              estimated_card_height))
                except:
                    print("Discard image not found, keeping original graphic.")

                player.discard_pile.append(player.card_in_play)
                player.card_in_play = None

        # Move Enemy Card to top-left (Discard)
        if enemy.card_in_play:
            finished_e = animate_move_to(enemy.card_in_play, enemy_discard_target, cleanup_speed)
            display_card(enemy.card_in_play, (enemy.card_in_play.position.x, enemy.card_in_play.position.y),
                         display_surface)
            if finished_e:
                try:
                    discard_surf = pygame.image.load(card_back_path).convert_alpha()
                    rotated_surf = pygame.transform.rotate(discard_surf, 180)
                    enemy.card_in_play.graphic = pygame.transform.smoothscale(rotated_surf, (TARGET_CARD_WIDTH,
                                                                                              estimated_card_height))
                except:
                    print("Discard image not found, keeping original graphic.")

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

def display_discard_piles(player, enemy, display_surface):
    """Draws the top card of the discard piles in the corners."""
    if player.discard_pile:
        last_card = player.discard_pile[-1]
        display_card(last_card, (last_card.position.x, last_card.position.y), display_surface)

    if enemy.discard_pile:
        last_card = enemy.discard_pile[-1]
        display_card(last_card, (last_card.position.x, last_card.position.y), display_surface)

def display_battle_entities(player, enemy, display_surface):
    """Positions and draws the player and enemy sprites on the screen."""
    PLAYER_SCALE = 1.2
    player_image_path = 'Assets/Images/Player/Right/0.png'

    try:
        player_battle_surf = pygame.image.load(player_image_path).convert_alpha()
    except:
        player_battle_surf = player.image

    orig_w, orig_h = player_battle_surf.get_size()
    scaled_player_img = pygame.transform.smoothscale(player_battle_surf,(int(orig_w * PLAYER_SCALE), int(orig_h * PLAYER_SCALE)))

    battle_player_rect = scaled_player_img.get_rect(center=(60, WINDOW_HEIGHT - 260))
    battle_enemy_rect = enemy.image.get_rect(center=(WINDOW_WIDTH - 60, WINDOW_HEIGHT - 450))

    display_surface.blit(scaled_player_img, battle_player_rect)
    display_surface.blit(enemy.image, battle_enemy_rect)