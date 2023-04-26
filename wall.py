import pygame


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, size=40, is_breakable=False):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill('Dark Blue')
        inside = pygame.Rect((1, 1), (39, 39))
        pygame.draw.rect(self.image, "Blue", inside)
        self.rect = self.image.get_rect(topleft=pos)

    def update(self):
        pass
