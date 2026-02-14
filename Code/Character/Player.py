from Code.Settings import *
from Code.Character.Character import Character, STARTING_MAX_MANA
from Code.Cards.Card import Card


class Player(pygame.sprite.Sprite, Character):
    def __init__(self, pos, groups, collision_sprites, name, health=60, mana=50, full_deck: list[Card] = None):

        pygame.sprite.Sprite.__init__(self, groups)
        Character.__init__(self, name, health, full_deck if full_deck else [])

        self.frames = {'Left': [], 'Right': [], 'Up': [], 'Down': []}
        self.scale_factor = 0.8
        self.load_images()
        self.state, self.frame_index = 'Down', 0
        self.image = self.frames['Down'][0]
        self.rect = self.image.get_frect(center=pos)
        self.hitbox_rect = self.rect.inflate(-20, -40)

        self.direction = pygame.Vector2()
        self.speed = 500
        self.collision_sprites = collision_sprites

        self.mana = STARTING_MAX_MANA
        self.max_mana = mana
        self.current_max_mana = STARTING_MAX_MANA

        self.in_battle = False
        self.card_in_play = None
        self.animation_step = 0  # 0 = Idle, 1 = Moving to Center, 2 = Effect/Pause, 3 = To Discard
        self.player_turn = True

    def load_images(self):

        file_structure = {
            'Down': ['0.png', '1.png', '2.png'],
            'Up': ['0.png', '1.png', '2.png'],
            'Left': ['0.png', '1.png', '2.png'],
            'Right': ['0.png', '1.png', '2.png']
        }

        for state, files in file_structure.items():
            for file_name in files:
                full_path = join('Assets', 'Images', 'Player', state, file_name)
                surf = pygame.image.load(full_path).convert_alpha()
                width = int(surf.get_width() * self.scale_factor)
                height = int(surf.get_height() * self.scale_factor)
                surf = pygame.transform.scale(surf, (width, height))
                self.frames[state].append(surf)

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.hitbox_rect.top = sprite.rect.bottom

    def animate(self, dt):
        if self.direction.x != 0:
            self.state = 'Right' if self.direction.x > 0 else 'Left'
        if self.direction.y != 0:
            self.state = 'Down' if self.direction.y > 0 else 'Up'

        self.frame_index = self.frame_index + 5 * dt if self.direction else 0
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)

    def end_battle(self, win):
        """Override: Player health does NOT reset after battle to persist across encounters."""
        # Reset mana for next battle
        self.current_max_mana = STARTING_MAX_MANA
        self.mana = 0
        self.turn_number = 0

        # NOTE: Health is NOT reset - player must preserve HP through encounters
        if win:
            print("You win!")
            self.get_new_card(0, 'NORMAL')
        else:
            print("You lost!")

    #COMMENTED FOR TESTING
    # def new_game_starting_package(self, enemy=None):
    #     self.full_deck = []
    #     tier = getattr(enemy, 'tier', 0)
    #     match tier:
    #         case 0:
    #             for _ in range(15):
    #                 self.get_new_card(0, 'NORMAL')
    #         case 1:
    #             for _ in range(15):
    #                 self.get_new_card(0, 'NORMAL')
    #             for _ in range(5):
    #                 self.get_new_card(1, 'NORMAL')
    #         case 2:
    #             for _ in range(10):
    #                 self.get_new_card(0, 'NORMAL')
    #             for _ in range(5):
    #                 self.get_new_card(1, 'NORMAL')
    #             for _ in range(5):
    #                 self.get_new_card(2, 'NORMAL')
