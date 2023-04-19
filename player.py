import pygame, math

from pygame.locals import *

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
        self.speed = .2
        self.turn_speed = 1
        self.keyboard = True
        self.autoaim = True
        self.autoturn = False

        self.image = pygame.image.load("sprites/Tank0.png")
        self.rect = self.image.get_rect(center=pos)
        self.x = pos[0]
        self.y = pos[1]

        self.picture = pygame.image.load("sprites/Tank0.png")

    def getAngle(self):
        return self.angle

    def movePlayerCombined(self, direction, time_passed):
        startAngle = self.angle % 360
        endAngle = direction % 360
        print(self.angle)
        if startAngle == endAngle:
            movement_x = math.cos(self.angle) * self.speed
            movement_y = math.sin(self.angle) * self.speed
            self.rect.x += movement_x
            self.rect.y += movement_y
        else:
            if endAngle - startAngle <= 180:
                self.angle += 1
            else:
                self.angle += self.turn_speed * time_passed
            self.image = pygame.transform.rotate(self.picture, int(self.angle))
            self.rect.x = self.x - int(self.image.get_width() / 2)
            self.rect.y = self.y - int(self.image.get_height() / 2)


    def movePlayer(self, time_passed, direction):
        movement_x = math.cos(self.angle * math.pi / 180) * self.speed * time_passed
        movement_y = math.sin(self.angle * math.pi / 180) * -1 * self.speed * time_passed
        self.x += movement_x * direction
        self.y += movement_y * direction
        self.rect.x = self.x - int(self.image.get_width() / 2)
        self.rect.y = self.y - int(self.image.get_height() / 2)

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

    def get_inputs(self, time_passed):
        keys = pygame.key.get_pressed()
        if not self.autoturn:
            if keys[key_sets[self.player_number]["left"]] and not keys[key_sets[self.player_number]["right"]]:
                self.angle += self.turn_speed * time_passed
                self.image = pygame.transform.rotate(self.picture, int(self.angle))
                self.rect.x = self.x - int(self.image.get_width() / 2)
                self.rect.y = self.y - int(self.image.get_height() / 2)
            elif keys[key_sets[self.player_number]["right"]] and not keys[key_sets[self.player_number]["left"]]:
                self.angle -= self.turn_speed * time_passed
                self.image = pygame.transform.rotate(self.picture, int(self.angle))
                self.rect.x = self.x - int(self.image.get_width() / 2)
                self.rect.y = self.y - int(self.image.get_height() / 2)
            elif keys[key_sets[self.player_number]["up"]] and not keys[key_sets[self.player_number]["down"]]:
                self.movePlayer(time_passed, 1)
            elif keys[key_sets[self.player_number]["down"]] and not keys[key_sets[self.player_number]["up"]]:
                self.movePlayer(time_passed, -1)
                print('move player')
        else:
            if keys[key_sets[self.player_number]["up"]]:
                self.movePlayerCombined(90, time_passed)
            elif keys[key_sets[self.player_number]["right"]]:
                self.movePlayerCombined(0, time_passed)
            elif keys[key_sets[self.player_number]["left"]]:
                self.movePlayerCombined(180, time_passed)
            elif keys[key_sets[self.player_number]["down"]]:
                self.movePlayerCombined(270, time_passed)

    def update(self, time_passed):
        self.get_inputs(time_passed)
