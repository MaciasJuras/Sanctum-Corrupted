from Code.Settings import *
from Code.Graphics.Sprites import *
from pytmx.util_pygame import load_pygame
import random
import os
from os.path import join
import pygame


def draw_minimap(display_surface, rooms, current_room):
    minimap_x = WINDOW_WIDTH - 100
    minimap_y = 20
    dot_size = 4
    spacing = 16

    min_x = min(room[0] for room in rooms)
    min_y = min(room[1] for room in rooms)

    for room_pos in rooms:
        center_x = minimap_x + (room_pos[0] - min_x) * spacing
        center_y = minimap_y + (room_pos[1] - min_y) * spacing

        if room_pos == current_room:
            pygame.draw.circle(display_surface, (255, 255, 255), (center_x, center_y), dot_size + 2)
        else:
            pygame.draw.circle(display_surface, (150, 150, 160), (center_x, center_y), dot_size)


class Room:
    def __init__(self, position, offset, width, height, room_type):
        self.position = position
        self.offset = offset
        self.width = width
        self.height = height
        self.center = (offset[0] + width // 2, offset[1] + height // 2)
        self.room_type = room_type

class StartRoom(Room):
    def __init__(self, position, offset, width, height):
        super().__init__(position, offset, width, height, 'start')

class TreasureRoom(Room):
    def __init__(self, position, offset, width, height):
        super().__init__(position, offset, width, height, 'treasure')


class BossRoom(Room):
    def __init__(self, position, offset, width, height):
        super().__init__(position, offset, width, height, 'boss')


class MonsterRoom(Room):
    def __init__(self, position, offset, width, height):
        super().__init__(position, offset, width, height, 'monster')


class ShopRoom(Room):
    def __init__(self, position, offset, width, height):
        super().__init__(position, offset, width, height, 'shop')


def generate_rooms():
    start_pos = (0, 0)
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    adjacent_positions = random.sample(directions, 2)

    room_positions = [start_pos]

    for direction in adjacent_positions:
        pos = (start_pos[0] + direction[0], start_pos[1] + direction[1])
        room_positions.append(pos)

    distant_pos = (
        start_pos[0] + adjacent_positions[0][0] * 2,
        start_pos[1] + adjacent_positions[0][1] * 2
    )
    room_positions.append(distant_pos)

    room_classes = {start_pos: StartRoom, distant_pos: BossRoom}
    remaining_positions = [pos for pos in room_positions if pos not in room_classes]
    optional_classes = [TreasureRoom, ShopRoom, MonsterRoom]
    random.shuffle(optional_classes)

    for pos in remaining_positions:
        cls = optional_classes.pop() if optional_classes else MonsterRoom
        room_classes[pos] = cls

    return room_positions, room_classes


def load_room(position, room_cls, all_sprites, collision_sprites, door_sprites, rooms):
    room_width = WINDOW_WIDTH
    room_height = WINDOW_HEIGHT
    offset_x = position[0] * room_width
    offset_y = position[1] * room_height

    map_path = join('../Assets/Images/Maps', 'Map9.tmx')
    if os.path.exists(map_path):
        tmx_map = load_pygame(map_path)

        ground_layer = tmx_map.get_layer_by_name('Ground')
        for x, y, image in ground_layer.tiles():
            if image:
                Sprite((x * TILE_SIZE + offset_x, y * TILE_SIZE + offset_y), image, [all_sprites])

        walls_layer = tmx_map.get_layer_by_name('Walls')
        for x, y, image in walls_layer.tiles():
            if image:
               Sprite((x * TILE_SIZE + offset_x, y * TILE_SIZE + offset_y), image, [all_sprites])

        for obj in tmx_map.get_layer_by_name("Collisions"):
            collision_surface = pygame.Surface((obj.width, obj.height))
            CollisionSprite(
                (obj.x + offset_x, obj.y + offset_y),
                collision_surface,
                [collision_sprites]
            )

        room = room_cls(position, (offset_x, offset_y), room_width, room_height)
        rooms[position] = room
        create_doors(room, door_sprites)
        print(f"Loaded {room.room_type} room at {position} (offset: {offset_x}, {offset_y})")


def create_doors(room, door_sprites):
    door_width = 60
    door_height = 60
    offset_x, offset_y = room.offset
    room_width = room.width
    room_height = room.height
    directions = {
        (0, -1): ('up', offset_x + room_width // 2 - door_width // 2, offset_y + 30),
        (1, 0): ('right', offset_x + room_width - 80, offset_y + room_height // 2 - door_height // 2),
        (0, 1): ('down', offset_x + room_width // 2 - door_width // 2, offset_y + room_height - 90),
        (-1, 0): ('left', offset_x + 130, offset_y + room_height // 2 - door_height // 2)
    }

    for direction_vec, (name, x, y) in directions.items():
        size = (door_width, door_height)

        door = Door((x, y), size, direction_vec, [door_sprites])
        door.room = room.position
        door.name = name
