import pygame, math

from pygame.locals import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__()

        self.angle = 0
        self.color = color
        self.speed = 1

        self.image = pygame.image.load("Tank 2.png")
        self.rect = self.image.get_rect(topleft=pos)

    def getAngle(self):
        return self.angle
    def movePlayer(self):
        movement_x = math.cos(self.angle) * self.speed
        movement_y = math.sin(self.angle) * self.speed
        self.rect.x += movement_x
        self.rect.y += movement_y

    def rotatePlayer(self):
        pass
        # add rotate function
    def setVelocity(self, x, y):
        self.velocity = [x, y]
    def setSpeedX(self, x):
        self.velocity[0] = x
    def setSpeedY(self, y):
        self.velocity[1] = y
    def getVelocity(self):
        return [self.velocity[0], self.velocity[1]]
    def setAccY(self, y):
        self.velocity[1] = y

    def getImputs(self):
        keys = pygame.key.get_pressed()



    def update(self, DISPLAYSURF):
        self.getImputs()
