import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction):
        super().__init__()
        self.image = pygame.image.load("sprites/Turret0.png")
        self.rect = self.image.get_rect(topleft=pos)
        self.dx = direction[0]
        self.dy = direction[1]

    def update(self):
        pass
