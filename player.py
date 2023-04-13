import pygame, math

from pygame.locals import *

up_kb = [K_w, K_UP]
down_kb = [K_s, K_DOWN]
left_kb = [K_a, K_LEFT]
right_kb = [K_d, K_RIGHT]


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__()

        self.angle = 0
        self.color = color
        self.speed = 1

        self.image = pygame.image.load("sprites/Tank 2.png")
        self.rect = self.image.get_rect(topleft=pos)

    def get_angle(self):
        return self.angle

    def move_player(self):
        movement_x = math.cos(self.angle) * self.speed
        movement_y = math.sin(self.angle) * self.speed
        self.rect.x += movement_x
        self.rect.y += movement_y

    def rotate_player(self):
        pass
        # add rotate function

    def set_velocity(self, x, y):
        self.velocity = [x, y]

    def setSpeedX(self, x):
        self.velocity[0] = x

    def setSpeedY(self, y):
        self.velocity[1] = y

    def getVelocity(self):
        return [self.velocity[0], self.velocity[1]]

    def setAccY(self, y):
        self.velocity[1] = y

    def get_inputs(self):
        keys = pygame.key.get_pressed()
        if keys[K_a]:
            self.image = pygame.transform.rotate(self.image, 1)

    def update(self):
        self.get_inputs()
