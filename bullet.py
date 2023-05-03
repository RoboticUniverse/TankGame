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
        self.collisions_left = 1
        self.collided = 0

    def move_x(self, time_passed, walls):
        self.x += self.dx * time_passed * self.bullet_speed
        self.rect.x = self.x - self.rect.width / 2
        if self.collided < 0:
            for sprite in walls.sprites():
                if sprite.rect.colliderect(self.rect):
                    print("hit x")
                    if self.dx > 0:
                        self.rect.right = sprite.rect.left
                    else:
                        self.rect.left = sprite.rect.right
                    self.dx = -1 * self.dx
                    self.collisions_left -= 1
                    if self.collisions_left < 0:
                        self.kill()
                    self.collided = time_passed * 2
                    break
        else:
            self.collided -= time_passed


    def move_y(self, time_passed, walls):
        self.y += self.dy * time_passed * self.bullet_speed
        self.rect.y = self.y - self.rect.width / 2
        if self.collided < 0:
            for sprite in walls.sprites():
                if sprite.rect.colliderect(self.rect):
                    if self.dy > 0:
                        self.rect.bottom = sprite.rect.top
                    else:
                        self.rect.top = sprite.rect.bottom
                    self.dy = -1 * self.dy
                    self.collisions_left -= 1
                    if self.collisions_left < 0:
                        self.kill()
                    self.collided = time_passed * 2
                    break
        else:
            self.collided -= time_passed

    def update(self, time_passed, walls):
        self.move_x(time_passed, walls)
        self.move_y(time_passed, walls)
