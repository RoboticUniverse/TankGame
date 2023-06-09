import pygame


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, size=40, is_breakable=False):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill('Black')
        inside = pygame.Rect((1, 1), (39, 39))
        if is_breakable:
            pygame.draw.rect(self.image, (100,100,100), inside)
        else:
            pygame.draw.rect(self.image, (80,80,80), inside)
        self.rect = self.image.get_rect(topleft=pos)
        self.is_breakable = is_breakable

    def update(self):
        pass
