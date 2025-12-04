from Code.Character.Player import Player
from Code.Settings import *
from Code.Graphics.Groups import AllSprites
from Code.Map.Map import generate_rooms, load_room, draw_minimap
from Code.Map.Room_transition import *
import pygame

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
    pygame.init()
    display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Sanctum Corrupted')
    clock = pygame.time.Clock()
    running = True

    all_sprites = AllSprites()
    collision_sprites = pygame.sprite.Group()
    door_sprites = pygame.sprite.Group()

    rooms = {}
    current_room = (0, 0)
    e_pressed_last_frame = False

    room_positions, room_classes = generate_rooms()
    for room_pos in room_positions:
        load_room(room_pos, room_classes[room_pos], all_sprites, collision_sprites, door_sprites, rooms)

    player = Player((WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), (all_sprites, ), collision_sprites, 'Player')

    while running:
        dt = clock.tick() / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites.update(dt)
        current_room, e_pressed_last_frame = handle_door_interaction(door_sprites, current_room, player, rooms, e_pressed_last_frame)

        display_surface.fill('black')
        room_center = rooms[current_room].center
        all_sprites.custom_draw(room_center)

        #draw_room_name(display_surface, current_room, rooms)
        draw_minimap(display_surface, rooms, current_room)

        pygame.display.update()

    pygame.quit()
