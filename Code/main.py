import pygame
import sys
import pathlib

_PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from Code.Character.Player import Player
from Code.Character.Enemy import *
from Code.Character.Enemies import *
from Code.Settings import *
from Code.Graphics.Groups import AllSprites
from Code.Map.Map import StartRoom, MonsterRoom, TreasureRoom, ShopRoom, BossRoom
from Code.Map.Map import generate_rooms, load_room, draw_minimap
from Code.Map.Room_transition import *
from Code.GameState.Battle_mode import *
from Code.Graphics.Battle_graphic import *

# function to see type of the room (UNCOMMENT: draw_room_name(display_surface, current_room, rooms))
"""def draw_room_name(display_surface, current_room, rooms, font_size=32):
    if current_room in rooms:
        room = rooms[current_room]
        font = pygame.font.Font(None, font_size)

        room_name = room.room_type.capitalize() + " Room"
        text_surf = font.render(room_name, True, (255, 255, 255))

        bg_rect = text_surf.get_rect()
        bg_rect.inflate_ip(20, 10)  # Add padding
        bg_rect.topleft = (20, 20)  # Position in top-left corner

        bg_surface = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(bg_surface, (0, 0, 0, 180), bg_surface.get_rect(), border_radius=8)
        display_surface.blit(bg_surface, bg_rect)

        text_rect = text_surf.get_rect(center=bg_rect.center)
        display_surface.blit(text_surf, text_rect)
"""

if __name__ == "__main__":
    # --- Map load ---
    pygame.init()
    display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Sanctum Corrupted')
    clock = pygame.time.Clock()
    running = True

    all_sprites = AllSprites()
    collision_sprites = pygame.sprite.Group()
    door_sprites = pygame.sprite.Group()
    enemy_sprites = pygame.sprite.Group()

    rooms = {}
    current_room = (0, 0)
    e_pressed_last_frame = False

    room_positions, room_classes = generate_rooms(
        num_rooms=10,
        room_type_weights={
            MonsterRoom: 0.7,
            TreasureRoom: 0.25,
            ShopRoom: 0.05
        }
    )
    for room_pos in room_positions:
        load_room(room_pos, room_classes[room_pos], all_sprites, collision_sprites, door_sprites, rooms)

    # --- Player and enemy declaration
    player = Player((WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), (all_sprites,), collision_sprites, 'Player')

    # enemy = Cat((850, WINDOW_HEIGHT // 2), (all_sprites, enemy_sprites), 'Magic Cat', 100, [], 0, School.MAGICAL)
    # enemy.new_game_starting_package()

    # enemy2 = Cat((250, WINDOW_HEIGHT // 2), (all_sprites, enemy_sprites), 'Tech Cat', 100, [], 0, School.TECHNICAL)
    # enemy2.new_game_starting_package()

    # --- Parameters for tracking game phase and mouse clicks
    battle_initialized = False
    mouse_pressed_last_frame = False

    # --- Game loop ---
    while running:
        dt = clock.tick() / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if player.in_battle:
            # --- Checking mouse and keyboard button press ---
            e_pressed_last_frame = handle_battle_exit(player, e_pressed_last_frame)

            # Track if end turn button was clicked (to avoid also clicking cards)
            end_turn_clicked = False

            # Handle End Turn button FIRST (only in MULTI_CARD_MODE)
            if Battle_mode.MULTI_CARD_MODE:
                mouse_pressed = pygame.mouse.get_pressed()[0]
                if mouse_pressed and not mouse_pressed_last_frame:
                    button_rect = get_end_turn_button_rect()
                    if button_rect.collidepoint(pygame.mouse.get_pos()):
                        end_turn_clicked = True
                handle_end_turn_button(player, enemy, mouse_pressed_last_frame)

            # Then handle card selection (skip if end turn was clicked)
            if not end_turn_clicked:
                mouse_pressed_last_frame = handle_card_selection(player, mouse_pressed_last_frame)
            else:
                mouse_pressed_last_frame = pygame.mouse.get_pressed()[0]

            # --- Background Initialization ---
            if enemy.school == School.MAGICAL:
                bg_file = 'chamber-magical.png'
            elif enemy.school == School.TECHNICAL:
                bg_file = 'chamber-technical.png'
            else:
                bg_file = 'chamber-normal.png'
            draw_battle_background(display_surface, bg_file)

            if not battle_initialized:
                # --- Battle Initialization ---
                Battle_mode.reset_battle_state()

                enemy.start_battle()
                player.start_battle(enemy)

                if Battle_mode.MULTI_CARD_MODE:
                    # Multi-card mode: use turn system
                    player.start_turn()
                else:
                    # Single card mode: draw initial hand, set full mana (no turn system)
                    player.mana = player.max_mana
                    player.current_max_mana = player.max_mana
                    player.draw_cards(10)
                    enemy.mana = enemy.max_mana
                    enemy.current_max_mana = enemy.max_mana
                    enemy.draw_cards(10)

                # --- Reset Battle State ---
                player.card_in_play = None
                enemy.card_in_play = None

                battle_initialized = True

            display_battle_entities(player, enemy, display_surface)

            display_enemy_hand(enemy.hand, display_surface, enemy.card_in_play)
            display_cards_in_hand(player.hand, display_surface)
            display_discard_piles(player, enemy, display_surface)

            # Draw turn indicator and end turn button
            draw_turn_indicator(display_surface, Battle_mode.is_player_turn)
            if Battle_mode.MULTI_CARD_MODE:
                draw_end_turn_button(display_surface, Battle_mode.is_player_turn)

            if Battle_mode.battle_phase != Battle_mode.PHASE_IDLE:
                update_battle_sequence(player, enemy, display_surface)

            if not player.in_battle:
                battle_initialized = False

        else:
            all_sprites.update(dt)

            found_enemy, space_pressed_last_frame = handle_enemy_interaction(enemy_sprites, player)

            if found_enemy:
                enemy = found_enemy

            current_room, e_pressed_last_frame = handle_door_interaction(door_sprites, current_room, player, rooms,
                                                                         e_pressed_last_frame)

            enemy_sprites.empty()

            room_obj = rooms[current_room]
            if isinstance(room_obj, MonsterRoom) and not room_obj.cleared:
                enemy_sprites.add(room_obj.enemy)

            display_surface.fill('black')
            room_center = rooms[current_room].center
            all_sprites.custom_draw(room_center)

            # draw_room_name(display_surface, current_room, rooms)
            draw_minimap(display_surface, rooms, current_room)

        pygame.display.update()

    pygame.quit()