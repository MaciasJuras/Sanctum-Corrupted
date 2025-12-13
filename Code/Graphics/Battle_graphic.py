from Code.Settings import *
from Code.Cards import Card
from Code.Settings import WINDOW_WIDTH, WINDOW_HEIGHT
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

def update_card_animation(player, enemy, display_surface):
    """
    Called every frame in the main loop if player.card_in_play is not None.
    Handles movement, waiting, and effects.
    """
    card = player.card_in_play
    if not card:
        return

    target_x = (WINDOW_WIDTH // 2) - (card.position.width // 2)
    target_y = (WINDOW_HEIGHT // 2) - (card.position.height // 2)

    # --- STEP 1: MOVE TO CENTER ---
    if player.animation_step == 1:
        move_speed = 25

        if card.position.x < target_x: card.position.x += move_speed
        if card.position.x > target_x: card.position.x -= move_speed
        if card.position.y < target_y: card.position.y += move_speed
        if card.position.y > target_y: card.position.y -= move_speed

        if abs(card.position.x - target_x) < move_speed and abs(card.position.y - target_y) < move_speed:
            card.position.x = target_x
            card.position.y = target_y
            player.animation_step = 2

    # --- STEP 2: PAUSE & EXECUTE EFFECT ---
    elif player.animation_step == 2:

        #card.play([player, enemy])
        player.animation_step = 3
        pass

    # --- STEP 3: MOVE TO DISCARD PILE ---
    elif player.animation_step == 3:
        move_speed = 10
        card.position.x += move_speed
        card.position.y += move_speed

        # If off screen, finish
        if card.position.x > WINDOW_WIDTH:
            player.discard_pile.append(card)
            player.card_in_play = None
            player.animation_step = 0
            print("Animation finished, waiting for input.")

    display_card(card, (card.position.x, card.position.y), display_surface)