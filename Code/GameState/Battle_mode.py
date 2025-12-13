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
        player.end_battle()

    return e_pressed


def handle_card_selection(player, mouse_pressed_last_frame):
    """
    Detects if the player clicked on a card in their hand.
    Returns the new state of the mouse button (to prevent multi-clicks).
    """
    mouse_pressed = pygame.mouse.get_pressed()[0]

    if mouse_pressed and not mouse_pressed_last_frame:
        mouse_pos = pygame.mouse.get_pos()

        if player.card_in_play is None:
            for card in player.hand:
                if card.position and card.position.collidepoint(mouse_pos):
                    print(f"Clicked on: {card.name}")
                    player.hand.remove(card)
                    player.card_in_play = card
                    player.animation_step = 1
                    break

    return mouse_pressed