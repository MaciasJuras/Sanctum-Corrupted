import pygame

def handle_door_interaction(door_sprites, current_room, player, rooms, e_pressed_last_frame):
    keys = pygame.key.get_pressed()
    e_pressed = keys[pygame.K_e]

    if e_pressed and not e_pressed_last_frame:
        for door in door_sprites:
            if door.room != current_room:
                continue

            if door.rect.colliderect(player.rect):
                next_room = (
                    current_room[0] + door.direction[0],
                    current_room[1] + door.direction[1]
                )

                if next_room in rooms:
                    current_room = transition_to_room(door_sprites, current_room, next_room, door.direction, player, rooms)
                    break
    return current_room, e_pressed


def transition_to_room(door_sprites, current_room, next_room, door_direction, player, rooms):
    current_room = next_room
    opposite_direction = (-door_direction[0], -door_direction[1])

    for door in door_sprites:
        if door.room == next_room and door.direction == opposite_direction:
            if opposite_direction == (0, -1):
                player.rect.centerx = door.rect.centerx
                player.rect.y = door.rect.bottom + 20
            elif opposite_direction == (0, 1):
                player.rect.centerx = door.rect.centerx
                player.rect.y = door.rect.top - 20 - player.rect.height
            elif opposite_direction == (1, 0):
                player.rect.x = door.rect.left - 20 - player.rect.width
                player.rect.centery = door.rect.centery
            elif opposite_direction == (-1, 0):
                player.rect.x = door.rect.right + 20
                player.rect.centery = door.rect.centery

            player.hitbox_rect.center = player.rect.center
            break

    return current_room
