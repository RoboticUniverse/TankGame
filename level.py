import pygame
from wall import Wall
from player import *


class Level:
    def __init__(self, display_surface, number=1):
        self.surface = display_surface
        self.number = number
        self.walls = pygame.sprite.Group()
        self.create_outline()
        self.players = pygame.sprite.Group()
        self.players.add(Player((2, 2), (255, 0, 0)))

    def create_outline(self):
        try:
            room = pygame.image.load("sprites/levels/" + str(self.number) + ".png")
            for h in range(room.get_height()):
                for w in range(room.get_width()):
                    if room.get_at((w, h)) == (0, 0, 0, 255):
                        self.walls.add(Wall((w * 40 + 20, h * 40 + 20), 40, False))
                    elif room.get_at((w, h)) == (255, 0, 0, 255):
                        self.walls.add(Wall((w * 40 + 20, h * 40 + 20), 40, True))
                    # elif room.get_at((w, h)) == (0, 255, 0, 255):
                    #     enemies.append((w, h))
        except FileNotFoundError:
            print("Requested Room " + str(self.number) + " Does Not Exist")

    def get_walls(self):
        return self.walls

    def get_number(self):
        return self.number

    # def __str__(self):
    #     return "X: " + str(self.x) + ", Y: " + str(self.y)

    def run(self):
        self.walls.draw(self.surface)
        self.players.update()
        self.players.draw(self.surface)

