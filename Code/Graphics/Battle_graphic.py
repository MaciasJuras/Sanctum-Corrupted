from Code.Settings import *
import os

def draw_battle_background(display_surface, bg_name, image_cache):
    if bg_name not in image_cache:
        battle_background_path = join('Assets/Images/Battle', bg_name)

        if os.path.exists(battle_background_path):
            bg_image = pygame.image.load(battle_background_path).convert()
            bg_image = pygame.transform.scale(bg_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

            image_cache[bg_name] = bg_image
        else:
            print(f"Error: Background not found at {battle_background_path}")
            surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            display_surface.fill((0, 0, 0))
            image_cache[bg_name] = surface

    display_surface.blit(image_cache[bg_name], (0, 0))