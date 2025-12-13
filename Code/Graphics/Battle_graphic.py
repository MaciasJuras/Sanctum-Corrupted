from Code.Settings import *
from Code.Cards import Card
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
        card_image = card.generate_card_image()
        if card_image:
            mode = card_image.mode
            size = card_image.size
            data = card_image.tobytes()

            original_surface = pygame.image.fromstring(data, size, mode)
            original_width, original_height = original_surface.get_size()

            ratio = original_height / original_width
            target_height = int(TARGET_CARD_WIDTH * ratio)
            card_surface = pygame.transform.smoothscale(original_surface, (TARGET_CARD_WIDTH, target_height))

            display_surface.blit(card_surface, position)

        else:
            print(f"Failed to generate image for card: {card.name}")

def display_cards_in_hand(hand: list[Card], display_surface):
    total_width = len(hand) * (TARGET_CARD_WIDTH + CARD_SPACING) - CARD_SPACING
    start_x = (display_surface.get_width() - total_width) // 2

    estimated_height = int(TARGET_CARD_WIDTH * 1.4)
    y = display_surface.get_height() - estimated_height - CARD_SPACE_FROM_BOTTOM_SCREEN

    for i, card in enumerate(hand):
        x = start_x + (i * (TARGET_CARD_WIDTH + CARD_SPACING))
        display_card(card, (x, y), display_surface)