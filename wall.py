import pygame


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, size=40, is_breakable=False):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill('Blue')
        self.rect = self.image.get_rect(topleft=pos)

    def update(self):
        pass
