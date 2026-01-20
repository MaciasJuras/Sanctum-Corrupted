from Code.Cards.Card import School
from Code.Character.Enemies import Cat
from Code.Settings import *
from Code.Graphics.Sprites import *
from pytmx.util_pygame import load_pygame
import random
import os
from os.path import join
from collections import deque
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
        self.enemy = None
        self.cleared = False


class ShopRoom(Room):
    def __init__(self, position, offset, width, height):
        super().__init__(position, offset, width, height, 'shop')


def generate_rooms(num_rooms=8, room_type_weights=None):
    if room_type_weights is None:
        room_type_weights = {
            MonsterRoom: 0.6,
            TreasureRoom: 0.25,
            ShopRoom: 0.15
        }

    # --- Safety check ---
    min_rooms = 5  # Start + Boss + Shop + at least one Monster + one Treasure
    if num_rooms < min_rooms:
        raise ValueError(f"num_rooms must be at least {min_rooms}")

    start_pos = (0, 0)
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    # --- Generate connected map ---
    room_positions = [start_pos]
    while len(room_positions) < num_rooms:
        base = random.choice(room_positions)
        dx, dy = random.choice(directions)
        new_pos = (base[0] + dx, base[1] + dy)
        if new_pos not in room_positions:
            room_positions.append(new_pos)

    # --- BFS distance from Start ---
    distances = {start_pos: 0}
    queue = deque([start_pos])
    while queue:
        current = queue.popleft()
        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            if neighbor in room_positions and neighbor not in distances:
                distances[neighbor] = distances[current] + 1
                queue.append(neighbor)

    # --- Boss = farthest from Start ---
    boss_pos = max(distances, key=distances.get)

    # --- Shop = far from Start and Boss ---
    MIN_SHOP_DISTANCE_FROM_START = 3
    MIN_SHOP_DISTANCE_FROM_BOSS = 2

    shop_candidates = [
        pos for pos, d in distances.items()
        if d >= MIN_SHOP_DISTANCE_FROM_START
        and pos != boss_pos
        and abs(pos[0] - boss_pos[0]) + abs(pos[1] - boss_pos[1]) >= MIN_SHOP_DISTANCE_FROM_BOSS
    ]
    if not shop_candidates:
        # fallback if map too small
        shop_candidates = [pos for pos in room_positions if pos != start_pos and pos != boss_pos]

    shop_pos = random.choice(shop_candidates)

    # --- Assign fixed rooms ---
    room_classes = {
        start_pos: StartRoom,
        boss_pos: BossRoom,
        shop_pos: ShopRoom
    }

    # --- Assign room types using weights to all remaining positions ---
    remaining_positions = [pos for pos in room_positions if pos not in room_classes]
    weighted_types = list(room_type_weights.keys())
    weights = list(room_type_weights.values())

    for pos in remaining_positions:
        room_type = random.choices(weighted_types, weights=weights, k=1)[0]
        room_classes[pos] = room_type

    return room_positions, room_classes


def load_room(position, room_cls, all_sprites, collision_sprites, door_sprites, rooms):
    room_width = WINDOW_WIDTH
    room_height = WINDOW_HEIGHT
    offset_x = position[0] * room_width
    offset_y = position[1] * room_height

    map_path = join('Assets/Images/Maps', 'Map9.tmx')
    if os.path.exists(map_path):
        tmx_map = load_pygame(map_path)

        ground_layer = tmx_map.get_layer_by_name('Ground')
        for x, y, image in ground_layer.tiles():
            if image:
                Sprite((x * TILE_SIZE + offset_x, y * TILE_SIZE + offset_y), image, (all_sprites, ))

        walls_layer = tmx_map.get_layer_by_name('Walls')
        for x, y, image in walls_layer.tiles():
            if image:
               Sprite((x * TILE_SIZE + offset_x, y * TILE_SIZE + offset_y), image, (all_sprites, ))

        for obj in tmx_map.get_layer_by_name("Collisions"):
            collision_surface = pygame.Surface((obj.width, obj.height))
            CollisionSprite(
                (obj.x + offset_x, obj.y + offset_y),
                collision_surface,
                (collision_sprites, )
            )

        room = room_cls(position, (offset_x, offset_y), room_width, room_height)
        rooms[position] = room
        create_doors(room, door_sprites)

        if isinstance(room, MonsterRoom):
            enemy = Cat(
                (offset_x + room_width // 2, offset_y + room_height // 2),
                (all_sprites,collision_sprites),
                "Cat",
                100,
                [],
                tier=0,
                school=random.choice([School.MAGICAL, School.TECHNICAL])
            )

            enemy.new_game_starting_package()
            enemy.rect.inflate_ip(-30, -40)

            collision_sprites.add(enemy)
            room.enemy = enemy
            room.cleared = False
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

        door = Door((x, y), size, direction_vec, (door_sprites, ))
        door.room = room.position
        door.name = name
