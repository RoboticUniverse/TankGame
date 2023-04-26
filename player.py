import pygame, math
import numpy as np

from pygame.locals import *
from numpy import array

up_kb = [K_w, K_UP]
down_kb = [K_s, K_DOWN]
left_kb = [K_a, K_LEFT]
right_kb = [K_d, K_RIGHT]



key_sets = [{'up': K_w, 'down': K_s, 'left': K_a, 'right': K_d, 'shoot': K_LSHIFT, 'ability': K_LCTRL},
            {'up': K_p, 'down': K_SEMICOLON, 'left': K_l, 'right': K_QUOTE, 'shoot': K_COMMA, 'ability': K_m},
            {'up': K_t, 'down': K_g, 'left': K_f, 'right': K_h, 'shoot': K_c, 'ability': K_x},
            {'up': K_UP, 'down': K_DOWN, 'left': K_LEFT, 'right': K_RIGHT, 'shoot': K_RCTRL, 'ability': K_MENU},
            ]


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, player_number):
        super().__init__()

        self.player_number = player_number
        self.angle = 0
        self.turret_angle = 0
        self.speed = .2
        self.turn_speed = .2
        self.keyboard = True
        self.autoaim = False
        self.autoturn = False

        self.picture = pygame.image.load("sprites/Tank" + str(player_number) + ".png")
        self.sprites = [[], [], [], []]
        for row in range(4):
            for col in range(4):
                self.sprites[row].append(self.picture.subsurface((row * 64, col * 64), (64, 64)))
        self.left_tread = 0
        self.right_tread = 0

        self.image = self.sprites[self.right_tread][self.left_tread]
        self.rect = self.image.get_rect(topleft=pos)
        self.x = pos[0]
        self.y = pos[1]

        self.turret = pygame.image.load("sprites/Turret0.png")
        self.turret_image = pygame.image.load("sprites/Turret0.png")


    def getAngle(self):
        return self.angle
    def getX(self):
        return self.x
    def getY(self):
        return self.y

    def movePlayerCombined(self, direction, time_passed):
        # reset the angle to between 0 and 360
        self.angle = self.angle % 360
        if self.angle < 0:
            self.angle = self.angle - 360
        print(self.angle)
        # target angle is put to between 0 and 360
        endAngle = abs(direction % 360)
        # if target matches currrent, move the player
        if self.angle == abs(endAngle % 360):
            self.movePlayer(time_passed, 1)
        # rotate the player in the direction of the target
        else:
            if endAngle == 0:
                if self.angle > 180:
                    self.angle += self.turn_speed * time_passed
                    if self.angle % 360 < 180:
                        self.angle = endAngle
                else:
                    self.angle -= self.turn_speed * time_passed
                    if self.angle % 360 > 180:
                        self.angle = 0

            elif endAngle - self.angle <= 180 and (endAngle - self.angle > 0 or endAngle - self.angle < -180):
                self.angle += self.turn_speed * time_passed
                if self.angle % 360 > endAngle and self.angle - endAngle < 10:
                    self.angle = endAngle
            else:
                self.angle -= self.turn_speed * time_passed
                if self.angle % 360 < endAngle and endAngle - self.angle < 10:
                    self.angle = endAngle
            self.image = pygame.transform.rotate(self.sprites[self.left_tread][self.right_tread], int(self.angle))
            self.rect.x = self.x - int(self.image.get_width() / 2)
            self.rect.y = self.y - int(self.image.get_height() / 2)


    def movePlayer(self, time_passed, direction):
        movement_x = math.cos(self.angle * math.pi / 180) * self.speed * time_passed
        movement_y = math.sin(self.angle * math.pi / 180) * -1 * self.speed * time_passed
        self.x += movement_x * direction
        self.y += movement_y * direction
        self.rect.x = self.x
        self.rect.y = self.y

    def blit(self, surface):
        surface.blit(self.image, (self.rect.x - int(self.image.get_width() / 2), self.rect.y - int(self.image.get_height() / 2)))
        surface.blit(self.turret, (self.rect.x - int(self.turret.get_width() / 2), self.rect.y - int(self.turret.get_height() / 2)))

    def enemyAI(self, player):
        pass


    def get_inputs(self, time_passed):
        keys = pygame.key.get_pressed()
        if not self.autoturn:
            if keys[key_sets[self.player_number]["left"]] and not keys[key_sets[self.player_number]["right"]]:
                self.angle += self.turn_speed * time_passed
                self.image = pygame.transform.rotate(self.sprites[self.left_tread][self.right_tread], int(self.angle))
                self.rect.x = self.x - int(self.image.get_width() / 2)
                self.rect.y = self.y - int(self.image.get_height() / 2)
            elif keys[key_sets[self.player_number]["right"]] and not keys[key_sets[self.player_number]["left"]]:
                self.angle -= self.turn_speed * time_passed
                self.image = pygame.transform.rotate(self.sprites[self.left_tread][self.right_tread], int(self.angle))
                self.rect.x = self.x - int(self.image.get_width() / 2)
                self.rect.y = self.y - int(self.image.get_height() / 2)
            elif keys[key_sets[self.player_number]["up"]] and not keys[key_sets[self.player_number]["down"]]:
                self.movePlayer(time_passed, 1)
            elif keys[key_sets[self.player_number]["down"]] and not keys[key_sets[self.player_number]["up"]]:
                self.movePlayer(time_passed, -1)
                print('move player')
        else:
            if keys[key_sets[self.player_number]["up"]]:
                if keys[key_sets[self.player_number]["right"]]:
                    self.movePlayerCombined(45, time_passed)
                elif keys[key_sets[self.player_number]["left"]]:
                    self.movePlayerCombined(135, time_passed)
                else:
                    self.movePlayerCombined(90, time_passed)
            elif keys[key_sets[self.player_number]["right"]]:
                if keys[key_sets[self.player_number]["down"]]:
                    self.movePlayerCombined(315, time_passed)
                else:
                    self.movePlayerCombined(0, time_passed)
            elif keys[key_sets[self.player_number]["down"]]:
                if keys[key_sets[self.player_number]["left"]]:
                    self.movePlayerCombined(225, time_passed)
                else:
                    self.movePlayerCombined(270, time_passed)
            elif keys[key_sets[self.player_number]["left"]]:
                self.movePlayerCombined(180, time_passed)
                self.movePlayerCombined(270, time_passed)
        pos = pygame.mouse.get_pos()
        if self.autoaim:
            self.turret = pygame.transform.rotate(self.turret_image, int(self.angle))
        else:
            self.turret = pygame.transform.rotate(self.turret_image, int(self.turret_angle))

    def update(self, time_passed):
        self.get_inputs(time_passed)
