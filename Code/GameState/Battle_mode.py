import pygame

def handle_enemy_interaction(enemy_sprites, player):
    """ Checks for SPACE key press and direct collision with an enemy
        to initiate a battle."""
    keys = pygame.key.get_pressed()
    space_pressed = keys[pygame.K_SPACE]

    if space_pressed and not player.in_battle:
        colliding_enemy = pygame.sprite.spritecollideany(player, enemy_sprites)

        if colliding_enemy:
            start_battle_mode(player, colliding_enemy)
            player.in_battle = True

    return player.in_battle, space_pressed


def start_battle_mode(player, enemy):
    """ Executes the transition to battle mode."""
    print(f"BATTLE COMMENCED: {player.name} vs. {enemy.name}!") #black screen defined in main for nor

def handle_battle_exit(player, e_pressed_last_frame):
    keys = pygame.key.get_pressed()
    e_pressed = keys[pygame.K_e]

    if e_pressed and not e_pressed_last_frame:
        print("Exiting battle mode!")
        player.in_battle = False

    return e_pressed