from Code.Settings import *


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos , surf , groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos ,surf , groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class Door(pygame.sprite.Sprite):
    def __init__(self, pos, size, direction, groups):
        super().__init__(groups)
        self.image = pygame.Surface(size).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_frect(topleft=pos)
        self.direction = direction

