import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction):
        super().__init__()
        self.image = pygame.image.load("sprites/bullet.png")
        self.rect = self.image.get_rect(center=pos)
        self.x = self.rect.centerx
        self.y = self.rect.centery
        self.dx = direction[0]
        self.dy = direction[1]
        self.bullet_speed = .5

    def update(self, time_passed):
        self.x += self.dx * time_passed * self.bullet_speed
        self.y += self.dy * time_passed * self.bullet_speed
        self.rect.x = self.x - self.rect.width / 2
        self.rect.y = self.y - self.rect.width / 2
        pass
