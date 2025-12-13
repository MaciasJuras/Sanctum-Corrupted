import pygame

# --- Battle State Constants ---
PHASE_IDLE = 0
PHASE_PLAYER_ANIMATION = 1    # Player card moving to center
PHASE_ENEMY_CHOOSE = 2   # Logic step: Enemy picks card
PHASE_ENEMY_ANIMATION = 3     # Enemy card moving to center
PHASE_CLEANUP = 4        # Both cards moving to discard piles

battle_phase = PHASE_IDLE
timer_start = 0     # To manipulate time in battle

def handle_enemy_interaction(enemy_sprites, player):
    """ Checks for SPACE key press and direct collision with an enemy
        to initiate a battle."""
    keys = pygame.key.get_pressed()
    space_pressed = keys[pygame.K_SPACE]

    if space_pressed and not player.in_battle:
        colliding_enemy = pygame.sprite.spritecollideany(player, enemy_sprites)

        if colliding_enemy:
            player.in_battle = True
            return colliding_enemy, True

    return None, space_pressed


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
    global battle_phase
    mouse_pressed = pygame.mouse.get_pressed()[0]

    if mouse_pressed and not mouse_pressed_last_frame and battle_phase == PHASE_IDLE:
        mouse_pos = pygame.mouse.get_pos()

        for card in player.hand:
            # Check collision with the card's visual rect
            if card.position and card.position.collidepoint(mouse_pos):
                print(f"Clicked on: {card.name}")

                if card in player.hand:
                    player.hand.remove(card)

                player.card_in_play = card
                battle_phase = PHASE_PLAYER_ANIMATION
                break

    return mouse_pressed


# --- BATTLE LOGIC (Called by Graphics/Battle_graphic) ---

def apply_player_effect(player, enemy):
    """Called when player card hits the center."""
    if player.card_in_play:
        print(f"Player effect: {player.card_in_play.name}")
        player.card_in_play.play([player, enemy])

        if enemy.health <= 0:
            print("ENEMY DEFEATED!")
            #win logic here in future


def prepare_enemy_turn(enemy):
    """Called after player effect. Enemy picks a card."""
    enemy_card = enemy.choose_card_to_play()

    if enemy_card:
        if enemy_card in enemy.hand:
            enemy.hand.remove(enemy_card)

        enemy.card_in_play = enemy_card

        # Set starting position for animation (e.g., from the Enemy's body)
        # We need a temporary rect for the card if it doesn't have one
        if not hasattr(enemy_card, 'position') or enemy_card.position is None:
            enemy_card.position = pygame.Rect(enemy.rect.centerx, enemy.rect.centery, 0, 0)
        else:
            enemy_card.position.x = enemy.rect.centerx
            enemy_card.position.y = enemy.rect.centery

        return True  # Enemy played a card
    return False  # Enemy passed turn


def apply_enemy_effect(player, enemy):
    """Called when enemy card hits the center."""
    if enemy.card_in_play:
        print(f"Enemy effect: {enemy.card_in_play.name}")
        enemy.card_in_play.play([enemy, player])

        if player.health <= 0:
            print("PLAYER DEFEATED!")