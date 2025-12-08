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
    """ Executes the transition to battle mode by repositioning sprites
    to the center of the screen."""

    # 1. Calculate the center points for the battle screen view
    # battle_center_x = WINDOW_WIDTH // 2
    # battle_center_y = WINDOW_HEIGHT // 2
    #
    # # 2. Reposition the Player and Enemy to designated combat spots
    # # These positions are absolute screen coordinates, not world coordinates.
    # # Player is moved slightly left of center
    # player.rect.center = (battle_center_x - 150, battle_center_y)
    # player.position.xy = player.rect.topleft  # Update position vector
    #
    # # Enemy is moved slightly right of center
    # enemy.rect.center = (battle_center_x + 150, battle_center_y)
    # enemy.position.xy = enemy.rect.topleft  # Update position vector

    print(f"BATTLE COMMENCED: {player.name} vs. {enemy.name}!")

    # 3. Initialization (You would add your Battle Manager instantiation here)
    # E.g., self.battle_manager = BattleManager(player, enemy)

    # NOTE: You will need logic in your main loop to handle the world offset/camera
    # when player.in_battle is True, ensuring the battle scene stays fixed on screen.


def handle_battle_exit(player, e_pressed_last_frame):
    keys = pygame.key.get_pressed()
    e_pressed = keys[pygame.K_e]

    if e_pressed and not e_pressed_last_frame:
        print("Exiting battle mode!")
        player.in_battle = False

    return e_pressed