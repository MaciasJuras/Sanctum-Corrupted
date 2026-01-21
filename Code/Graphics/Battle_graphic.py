from Code.Settings import *
from Code.Cards import Card
from Code.Settings import WINDOW_WIDTH, WINDOW_HEIGHT
from Code.GameState import Battle_mode
import os

TARGET_CARD_WIDTH = 120
CARD_SPACING = -10
CARD_SPACE_FROM_BOTTOM_SCREEN = 0.5

PLAYER_PHASE_DELAY = 1000  # 1 second (faster for multi-card play)
ENEMY_PHASE_DELAY = 1000  # 1 second

# End Turn Button Configuration
END_TURN_BUTTON_WIDTH = 120
END_TURN_BUTTON_HEIGHT = 40


def get_end_turn_button_rect():
    """Returns the rect for the End Turn button."""
    x = WINDOW_WIDTH - END_TURN_BUTTON_WIDTH - 20
    y = WINDOW_HEIGHT // 2
    return pygame.Rect(x, y, END_TURN_BUTTON_WIDTH, END_TURN_BUTTON_HEIGHT)


def draw_end_turn_button(display_surface, is_player_turn):
    """Draws the End Turn button on screen."""
    button_rect = get_end_turn_button_rect()

    # Colors
    if is_player_turn and Battle_mode.battle_phase == Battle_mode.PHASE_IDLE:
        bg_color = (60, 120, 60)  # Green when clickable
        border_color = (80, 160, 80)
        text_color = (255, 255, 255)
    else:
        bg_color = (60, 60, 60)  # Gray when not clickable
        border_color = (80, 80, 80)
        text_color = (150, 150, 150)

    # Draw button background
    pygame.draw.rect(display_surface, bg_color, button_rect, border_radius=8)
    pygame.draw.rect(display_surface, border_color, button_rect, width=2, border_radius=8)

    # Draw button text
    font_path = 'Assets/Font/Jersey10.ttf'
    try:
        font = pygame.font.Font(font_path, 24)
    except:
        font = pygame.font.Font(None, 24)

    text = font.render("End Turn", True, text_color)
    text_rect = text.get_rect(center=button_rect.center)
    display_surface.blit(text, text_rect)


def draw_turn_indicator(display_surface, is_player_turn):
    """Draws whose turn it is."""
    font_path = 'Assets/Font/Jersey10.ttf'
    try:
        font = pygame.font.Font(font_path, 28)
    except:
        font = pygame.font.Font(None, 28)

    if is_player_turn:
        text = "YOUR TURN"
        color = (100, 200, 100)
    else:
        text = "ENEMY TURN"
        color = (200, 100, 100)

    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=(WINDOW_WIDTH // 2, 30))

    # Background
    bg_rect = text_rect.inflate(20, 10)
    bg_surface = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
    pygame.draw.rect(bg_surface, (0, 0, 0, 180), bg_surface.get_rect(), border_radius=8)
    display_surface.blit(bg_surface, bg_rect)

    display_surface.blit(text_surf, text_rect)


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
    Handles the sequence based on MULTI_CARD_MODE:
    - MULTI_CARD_MODE=True: Player plays multiple cards -> End Turn -> Enemy plays multiple cards -> repeat
    - MULTI_CARD_MODE=False: Player plays 1 card -> Enemy plays 1 card -> repeat
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

    # --- PHASE: PLAYER ANIMATION ---
    if Battle_mode.battle_phase == Battle_mode.PHASE_PLAYER_ANIMATION:
        card = player.card_in_play
        if card:
            arrived = animate_move_to(card, target_pos_player, move_speed)
            display_card(card, (card.position.x, card.position.y), display_surface)

            if arrived:
                current_time = pygame.time.get_ticks()

                if Battle_mode.timer_start == 0:
                    Battle_mode.timer_start = current_time
                    battle_ended = Battle_mode.apply_player_effect(player, enemy)
                    if battle_ended:
                        return

                if current_time - Battle_mode.timer_start >= PLAYER_PHASE_DELAY:
                    Battle_mode.timer_start = 0
                    # Move to cleanup for this card
                    Battle_mode.battle_phase = Battle_mode.PHASE_CLEANUP

    # --- PHASE: ENEMY TURN START (draw cards, refill mana) ---
    elif Battle_mode.battle_phase == Battle_mode.PHASE_ENEMY_TURN_START:
        Battle_mode.start_enemy_turn(enemy)
        # battle_phase is set to PHASE_ENEMY_CHOOSE inside start_enemy_turn

    # --- PHASE: ENEMY CHOOSES CARD ---
    elif Battle_mode.battle_phase == Battle_mode.PHASE_ENEMY_CHOOSE:
        enemy_hand_positions = display_enemy_hand(enemy.hand, display_surface)
        has_card = Battle_mode.prepare_enemy_card(enemy, enemy_hand_positions)

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
            # Enemy has no more playable cards
            if Battle_mode.MULTI_CARD_MODE:
                # Multi-card mode: end enemy turn, start player turn
                print("=== Enemy ends turn ===")
                enemy.end_turn()
                Battle_mode.battle_phase = Battle_mode.PHASE_PLAYER_TURN_START
            else:
                # Single card mode: enemy passes, back to player
                print("Enemy has no playable cards. Your turn.")
                Battle_mode.is_player_turn = True
                Battle_mode.battle_phase = Battle_mode.PHASE_IDLE

    # --- PHASE: ENEMY ANIMATION ---
    elif Battle_mode.battle_phase == Battle_mode.PHASE_ENEMY_ANIMATION:
        card = enemy.card_in_play
        if card:
            arrived = animate_move_to(card, target_pos_enemy, move_speed)
            display_card(card, (card.position.x, card.position.y), display_surface)

            if arrived:
                card.graphic = None
                current_time = pygame.time.get_ticks()
                if Battle_mode.timer_start == 0:
                    Battle_mode.timer_start = current_time
                    battle_ended = Battle_mode.apply_enemy_effect(player, enemy)
                    if battle_ended:
                        return

                if current_time - Battle_mode.timer_start >= ENEMY_PHASE_DELAY:
                    Battle_mode.timer_start = 0
                    # Move card to discard
                    Battle_mode.battle_phase = Battle_mode.PHASE_ENEMY_CARD_RESOLVE

    # --- PHASE: ENEMY CARD RESOLVE (discard and maybe play another) ---
    elif Battle_mode.battle_phase == Battle_mode.PHASE_ENEMY_CARD_RESOLVE:
        # Discard enemy's played card
        if enemy.card_in_play:
            enemy.discard_pile.append(enemy.card_in_play)
            enemy.card_in_play = None

        if Battle_mode.MULTI_CARD_MODE:
            # Enemy can play another card
            Battle_mode.battle_phase = Battle_mode.PHASE_ENEMY_CHOOSE
        else:
            # Single card mode: back to player (no turn system, just IDLE)
            Battle_mode.is_player_turn = True
            Battle_mode.battle_phase = Battle_mode.PHASE_IDLE
            print("Enemy finished. Your turn to play a card.")

    # --- PHASE: PLAYER TURN START ---
    elif Battle_mode.battle_phase == Battle_mode.PHASE_PLAYER_TURN_START:
        Battle_mode.start_player_turn(player)
        # battle_phase is set to PHASE_IDLE inside start_player_turn

    # --- PHASE: CLEANUP (Discard Player's card) ---
    elif Battle_mode.battle_phase == Battle_mode.PHASE_CLEANUP:
        finished_p = True

        # Move Player Card to discard
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

        if finished_p:
            if Battle_mode.MULTI_CARD_MODE:
                # Multi-card mode: player can play another card
                Battle_mode.battle_phase = Battle_mode.PHASE_IDLE
                print("Card played. Play another card or click End Turn.")
            else:
                # Single card mode: enemy responds immediately (no turn start)
                Battle_mode.is_player_turn = False
                Battle_mode.battle_phase = Battle_mode.PHASE_ENEMY_CHOOSE


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
    """Draws the top card of the discard piles as card backs in the corners."""
    estimated_card_height = int(TARGET_CARD_WIDTH * 1.4)
    PADDING_X = 20
    PADDING_Y = 180
    card_back_path = 'Assets/Images/Cards/back.png'

    # Player discard pile position (bottom-right)
    player_discard_pos = (WINDOW_WIDTH - TARGET_CARD_WIDTH - PADDING_X,
                          WINDOW_HEIGHT - estimated_card_height - PADDING_Y)
    # Enemy discard pile position (top-left)
    enemy_discard_pos = (PADDING_X, PADDING_Y)

    try:
        back_surf = pygame.image.load(card_back_path).convert_alpha()
        back_surf = pygame.transform.smoothscale(back_surf, (TARGET_CARD_WIDTH, estimated_card_height))
        back_surf_rotated = pygame.transform.rotate(back_surf, 180)
    except:
        return  # Can't load card back, skip drawing

    # Show player discard pile as card back
    if player.discard_pile:
        display_surface.blit(back_surf, player_discard_pos)

    # Show enemy discard pile as rotated card back
    if enemy.discard_pile:
        display_surface.blit(back_surf_rotated, enemy_discard_pos)


def display_battle_entities(player, enemy, display_surface):
    """Positions and draws the player and enemy sprites on the screen."""
    PLAYER_SCALE = 1.2
    player_image_path = 'Assets/Images/Player/Right/0.png'

    try:
        player_battle_surf = pygame.image.load(player_image_path).convert_alpha()
    except:
        player_battle_surf = player.image

    orig_w, orig_h = player_battle_surf.get_size()
    scaled_player_img = pygame.transform.smoothscale(player_battle_surf,
                                                     (int(orig_w * PLAYER_SCALE), int(orig_h * PLAYER_SCALE)))

    battle_player_rect = scaled_player_img.get_rect(center=(60, WINDOW_HEIGHT - 260))
    battle_enemy_rect = enemy.image.get_rect(center=(WINDOW_WIDTH - 60, WINDOW_HEIGHT - 450))

    display_surface.blit(scaled_player_img, battle_player_rect)
    display_surface.blit(enemy.image, battle_enemy_rect)

    # Draw health and mana bars
    display_stat_bars(player, enemy, display_surface)


def display_stat_bars(player, enemy, display_surface):
    """Draws health and mana bars for both player and enemy."""
    # Load font
    font_path = 'Assets/Font/Jersey10.ttf'
    try:
        font = pygame.font.Font(font_path, 24)
        font_small = pygame.font.Font(font_path, 18)
    except:
        font = pygame.font.Font(None, 24)
        font_small = pygame.font.Font(None, 18)

    # Bar dimensions
    BAR_WIDTH = 150
    BAR_HEIGHT = 20
    BAR_SPACING = 8
    BORDER_RADIUS = 5

    # Colors
    HEALTH_COLOR = (220, 50, 50)  # Red
    HEALTH_BG = (80, 20, 20)  # Dark red
    MANA_COLOR = (50, 100, 220)  # Blue
    MANA_BG = (20, 40, 80)  # Dark blue
    BORDER_COLOR = (40, 40, 40)  # Dark gray border
    TEXT_COLOR = (255, 255, 255)  # White text

    # Get current max mana (scales each turn)
    player_max_mana = getattr(player, 'current_max_mana', player.max_mana)
    enemy_max_mana = getattr(enemy, 'current_max_mana', enemy.max_mana)

    # === PLAYER STATS (Bottom-Left) ===
    player_x = 20
    player_y = WINDOW_HEIGHT - 180

    # Player name label
    player_label = font.render(player.name, True, TEXT_COLOR)
    display_surface.blit(player_label, (player_x, player_y - 30))

    # Player Health Bar
    draw_stat_bar(
        display_surface, player_x, player_y,
        BAR_WIDTH, BAR_HEIGHT,
        player.health, player.max_health,
        HEALTH_COLOR, HEALTH_BG, BORDER_COLOR, BORDER_RADIUS
    )
    health_text = font_small.render(f"HP: {player.health}/{player.max_health}", True, TEXT_COLOR)
    display_surface.blit(health_text, (player_x + BAR_WIDTH + 10, player_y + 2))

    # Player Mana Bar
    mana_y = player_y + BAR_HEIGHT + BAR_SPACING
    draw_stat_bar(
        display_surface, player_x, mana_y,
        BAR_WIDTH, BAR_HEIGHT,
        player.mana, player_max_mana,
        MANA_COLOR, MANA_BG, BORDER_COLOR, BORDER_RADIUS
    )
    mana_text = font_small.render(f"MP: {player.mana}/{player_max_mana}", True, TEXT_COLOR)
    display_surface.blit(mana_text, (player_x + BAR_WIDTH + 10, mana_y + 2))

    # === ENEMY STATS (Top-Right) ===
    enemy_x = WINDOW_WIDTH - BAR_WIDTH - 20
    enemy_y = 160

    # Enemy name label
    enemy_label = font.render(enemy.name, True, TEXT_COLOR)
    enemy_label_rect = enemy_label.get_rect(right=WINDOW_WIDTH - 20, top=enemy_y - 30)
    display_surface.blit(enemy_label, enemy_label_rect)

    # Enemy Health Bar
    draw_stat_bar(
        display_surface, enemy_x, enemy_y,
        BAR_WIDTH, BAR_HEIGHT,
        enemy.health, enemy.max_health,
        HEALTH_COLOR, HEALTH_BG, BORDER_COLOR, BORDER_RADIUS
    )
    enemy_health_text = font_small.render(f"HP: {enemy.health}/{enemy.max_health}", True, TEXT_COLOR)
    enemy_health_rect = enemy_health_text.get_rect(right=enemy_x - 10, top=enemy_y + 2)
    display_surface.blit(enemy_health_text, enemy_health_rect)

    # Enemy Mana Bar
    enemy_mana_y = enemy_y + BAR_HEIGHT + BAR_SPACING
    draw_stat_bar(
        display_surface, enemy_x, enemy_mana_y,
        BAR_WIDTH, BAR_HEIGHT,
        enemy.mana, enemy_max_mana,
        MANA_COLOR, MANA_BG, BORDER_COLOR, BORDER_RADIUS
    )
    enemy_mana_text = font_small.render(f"MP: {enemy.mana}/{enemy_max_mana}", True, TEXT_COLOR)
    enemy_mana_rect = enemy_mana_text.get_rect(right=enemy_x - 10, top=enemy_mana_y + 2)
    display_surface.blit(enemy_mana_text, enemy_mana_rect)


def draw_stat_bar(surface, x, y, width, height, current, maximum, fill_color, bg_color, border_color, border_radius):
    """Draws a single stat bar with background, fill, and border."""
    # Background
    bg_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, bg_color, bg_rect, border_radius=border_radius)

    # Fill (proportional to current/max)
    if maximum > 0:
        fill_width = int((current / maximum) * width)
        fill_width = max(0, min(fill_width, width))  # Clamp between 0 and width
        if fill_width > 0:
            fill_rect = pygame.Rect(x, y, fill_width, height)
            pygame.draw.rect(surface, fill_color, fill_rect, border_radius=border_radius)

    # Border
    pygame.draw.rect(surface, border_color, bg_rect, width=2, border_radius=border_radius)