from Code.Settings import *
from Code.Character import Character
from Code.Cards import Card


class Player(pygame.sprite.Sprite, Character):
    def __init__(self, pos ,groups, collision_sprites, name, health = 100, mana = 50, full_deck: list[Card] = None):

        pygame.sprite.Sprite.__init__(self, groups)
        Character.__init__(self, name, health, full_deck if full_deck else [])

        self.scale_factor = 0.8
        self.load_images()
        self.state, self.frame_index = 'Down', 0
        self.image = self.frames['Down'][0]
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-20, -40)

        self.direction = pygame.Vector2()
        self.speed = 500
        self.collision_sprites = collision_sprites

        self.mana = mana
        self.max_mana = mana
        self.in_battle = False

    def load_images(self):
        self.frames = {'Left': [], 'Right': [], 'Up': [], 'Down': []}

        file_structure = {
            'Down': ['0.png', '1.png', '2.png'],
            'Up': ['0.png', '1.png', '2.png'],
            'Left': ['0.png', '1.png', '2.png'],
            'Right': ['0.png', '1.png', '2.png']
        }

        for state, files in file_structure.items():
            for file_name in files:
                full_path = join('..','Assets', 'Images', 'Player', state, file_name)
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



    def start_turn(self):
        print(f"\n--- {self.name}'s Turn ---")
        self.draw_cards(self.max_cards - len(self.hand))
        self.show_hand()

    def show_hand(self):

        print(f"{self.name}'s Hand:")
        if not self.hand:
            print("  (No cards in hand)")
            return

        for i, card in enumerate(self.hand):
            print(f"  {i + 1}: {card.name} (Cost: {card.cost}) - {card.description}")

    def choose_card_to_play(self, target: Character):
        #Uses console input for now - need to be changed when we will have assets
        playable_cards = [card for card in self.hand if card.cost <= self.mana]
        if not playable_cards:
            print("You don't have enough mana to play any card. Your turn ends")
            return False
        while True:
            try:
                choice = input(f"Choose a card from the hand (1-indexed) or '0' to end turn: ")
                if choice == '0':
                    print(f"{self.name} ends their turn.")
                    return False
                chosen_index = int(choice)-1
                if 0 <= chosen_index < len(self.hand):
                    chosen_card = self.hand[chosen_index]
                    if  chosen_card.cost > self.mana:
                        print(f"Not enough mana to play {chosen_card}")
                        continue
                    self.mana -= chosen_card.cost
                    print(f"{self.name} spends {chosen_card.cost} mana. ({self.mana} remaining)")
                    self.play_card(chosen_card, target)
                    return True
                else:
                    print("Invalid choice. Please pick a number from your hand.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def end_battle(self):
        self.mana = self.max_mana

