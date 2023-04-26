import pygame
from wall import Wall
from player import *


class Level:
    def __init__(self, display_surface, level_number=1):
        self.surface = display_surface
        self.level_number = level_number
        self.walls = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.create_outline()

    def create_outline(self):
        player_number = 0
        try:
            room = pygame.image.load("sprites/levels/" + str(self.level_number) + ".png")
            for h in range(room.get_height()):
                for w in range(room.get_width()):
                    if room.get_at((w, h)) == (0, 0, 0, 255):
                        self.walls.add(Wall((w * 40 + 20, h * 40 + 20), 40, False))
                    elif room.get_at((w, h)) == (255, 255, 0, 255):
                        self.walls.add(Wall((w * 40 + 20, h * 40 + 20), 40, True))
                    elif room.get_at((w, h)) == (0, 0, 255, 255):
                        self.players.add(Player((w * 40 + 20 + 16, h * 40 + 20 + 16), player_number))
                        player_number += 1
                    # elif room.get_at((w, h)) == (0, 255, 0, 255):
                    #     enemies.append((w, h))
        except FileNotFoundError:
            print("Requested Level " + str(self.level_number) + " Does Not Exist")

    # def __str__(self):
    #     return "X: " + str(self.x) + ", Y: " + str(self.y)

    def run(self, time_passed):
        self.walls.draw(self.surface)
        self.players.update(time_passed, self.walls, self.surface)

