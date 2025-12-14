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
from Code.Map.Map import generate_rooms, load_room, draw_minimap
from Code.Map.Room_transition import *
from Code.GameState.Battle_mode import *
from Code.Graphics.Battle_graphic import *




""" #function to see type of the room (UNCOMMENT: draw_room_name(display_surface, current_room, rooms))
def draw_room_name(display_surface, current_room, rooms, font_size=32):
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
#--- Map load ---
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

    room_positions, room_classes = generate_rooms()
    for room_pos in room_positions:
        load_room(room_pos, room_classes[room_pos], all_sprites, collision_sprites, door_sprites, rooms)

#--- Player and enemy declaration
    player = Player((WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), (all_sprites, ), collision_sprites, 'Player')
    player.new_game_starting_package()

    enemy = Rat((850, WINDOW_HEIGHT // 2), (all_sprites, enemy_sprites), 'Magic Rat', 100, [], 0, School.MAGICAL)
    enemy.new_game_starting_package()

    enemy2 = Rat((250, WINDOW_HEIGHT // 2), (all_sprites, enemy_sprites), 'Tech Rat', 100, [], 0, School.TECHNICAL)
    enemy2.new_game_starting_package()

#--- Parameters for tracking game phase and mouse clicks
    battle_initialized = False
    mouse_pressed_last_frame = False

#--- Game loop ---
    while running:
        dt = clock.tick() / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if player.in_battle:
            # --- Checking mouse and keyboard button press ---
            e_pressed_last_frame = handle_battle_exit(player, e_pressed_last_frame)
            mouse_pressed_last_frame = handle_card_selection(player, mouse_pressed_last_frame)

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
                enemy.start_battle()
                enemy.draw_cards(10)

                player.start_battle()
                player.start_turn()

                # --- Reset Battle State ---
                Battle_mode.battle_phase = Battle_mode.PHASE_IDLE
                player.card_in_play = None
                enemy.card_in_play = None

                battle_initialized = True

            display_cards_in_hand(player.hand, display_surface)

            if Battle_mode.battle_phase != Battle_mode.PHASE_IDLE:
                update_battle_sequence(player, enemy, display_surface)

            if not player.in_battle:
                battle_initialized = False

        else:
            all_sprites.update(dt)

            found_enemy, space_pressed_last_frame = handle_enemy_interaction(enemy_sprites, player)

            if found_enemy:
                enemy = found_enemy

            current_room, e_pressed_last_frame = handle_door_interaction(door_sprites,  current_room,  player,  rooms,  e_pressed_last_frame)

            display_surface.fill('black')
            room_center = rooms[current_room].center
            all_sprites.custom_draw(room_center)

            # draw_room_name(display_surface, current_room, rooms)
            draw_minimap(display_surface, rooms, current_room)

        pygame.display.update()

    pygame.quit()