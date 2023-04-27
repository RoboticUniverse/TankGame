import pygame, math

from pygame.locals import *
from bullet import *

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
        self.shot_speed = 1000
        self.shoot_cooldown = self.shot_speed
        self.keyboard = True
        self.autoaim = False
        self.autoturn = True

        self.picture = pygame.image.load("sprites/Tank" + str(player_number) + ".png")
        self.sprites = [[], [], [], []]
        for row in range(4):
            for col in range(4):
                self.sprites[row].append(self.picture.subsurface((row * 64, col * 64), (64, 64)))
        self.left_tread = 0
        self.right_tread = 0
        self.animation_speed = 50
        self.animation_cooldown = self.animation_speed

        self.image = self.sprites[self.right_tread][self.left_tread]
        self.rect = self.image.get_rect(center=pos)
        self.hitbox_addition = 0
        self.rect.width += self.hitbox_addition
        self.rect.height += self.hitbox_addition
        self.x = self.rect.centerx
        self.y = self.rect.centery

        self.turret = pygame.image.load("sprites/Turret0.png")
        self.turret_image = pygame.image.load("sprites/Turret0.png")
        self.bullets = []

    def update_animation_buffer(self, time_passed):
        self.animation_cooldown += time_passed
        if self.animation_cooldown > self.animation_speed:
            self.animation_cooldown = 0

    def get_inputs(self, time_passed):
        keys = pygame.key.get_pressed()
        if not self.autoturn:
            if keys[key_sets[self.player_number]["left"]] and not keys[key_sets[self.player_number]["right"]]:
                self.angle += self.turn_speed * time_passed
                if self.animation_cooldown == 0:
                    self.decrease_left_tread()
                    self.increase_right_tread()
                self.image = pygame.transform.rotate(self.sprites[self.left_tread][self.right_tread], int(self.angle))
            elif keys[key_sets[self.player_number]["right"]] and not keys[key_sets[self.player_number]["left"]]:
                self.angle -= self.turn_speed * time_passed
                if self.animation_cooldown == 0:
                    self.increase_right_tread()
                    self.decrease_left_tread()
                self.image = pygame.transform.rotate(self.sprites[self.left_tread][self.right_tread], int(self.angle))
            elif keys[key_sets[self.player_number]["up"]] and not keys[key_sets[self.player_number]["down"]]:
                self.move_player(time_passed, 1)
                if self.animation_cooldown == 0:
                    self.increase_right_tread()
                    self.increase_left_tread()
                self.image = pygame.transform.rotate(self.sprites[self.left_tread][self.right_tread], int(self.angle))
            elif keys[key_sets[self.player_number]["down"]] and not keys[key_sets[self.player_number]["up"]]:
                self.move_player(time_passed, -1)
                if self.animation_cooldown == 0:
                    self.decrease_right_tread()
                    self.decrease_left_tread()
                self.image = pygame.transform.rotate(self.sprites[self.left_tread][self.right_tread], int(self.angle))
        else:
            if keys[key_sets[self.player_number]["up"]]:
                if keys[key_sets[self.player_number]["right"]]:
                    self.move_player_combined(45, time_passed)
                elif keys[key_sets[self.player_number]["left"]]:
                    self.move_player_combined(135, time_passed)
                else:
                    self.move_player_combined(90, time_passed)
            elif keys[key_sets[self.player_number]["right"]]:
                if keys[key_sets[self.player_number]["down"]]:
                    self.move_player_combined(315, time_passed)
                else:
                    self.move_player_combined(0, time_passed)
            elif keys[key_sets[self.player_number]["down"]]:
                if keys[key_sets[self.player_number]["left"]]:
                    self.move_player_combined(225, time_passed)
                else:
                    self.move_player_combined(270, time_passed)
            elif keys[key_sets[self.player_number]["left"]]:
                self.move_player_combined(180, time_passed)

        pos = pygame.mouse.get_pos()
        if self.autoaim:
            self.turret = pygame.transform.rotate(self.turret_image, int(self.angle))
        else:
            v1 = pygame.math.Vector2(1, 0)
            v2 = pygame.math.Vector2(pos[0] - self.x, self.y - pos[1])
            self.turret_angle = v1.angle_to(v2)
            self.turret = pygame.transform.rotate(self.turret_image, int(self.turret_angle))
        self.shoot_cooldown += time_passed
        if keys[key_sets[self.player_number]["shoot"]] and self.shoot_cooldown >= self.shot_speed:
            print("shoot")
            self.bullets.append(Bullet((self.x, self.y), (1, 0)))
            self.shoot_cooldown = 0

    def move_player_combined(self, direction, time_passed):
        # reset the angle to between 0 and 360
        self.angle = self.angle % 360
        if self.angle < 0:
            self.angle = self.angle - 360
        # target angle is put to between 0 and 360
        end_angle = abs(direction % 360)
        # if target matches current, move the player
        if self.angle == abs(end_angle % 360):
            if self.animation_cooldown == 0:
                self.increase_right_tread()
                self.increase_left_tread()
                self.image = pygame.transform.rotate(self.sprites[self.left_tread][self.right_tread], int(self.angle))
            self.move_player(time_passed, 1)

        else:
            if end_angle == 0:
                if self.angle > 180:
                    self.angle += self.turn_speed * time_passed
                    if self.animation_cooldown == 0:
                        self.increase_left_tread()
                        self.decrease_right_tread()
                    if self.angle % 360 < 180:
                        self.angle = end_angle
                else:
                    self.angle -= self.turn_speed * time_passed
                    if self.animation_cooldown == 0:
                        self.increase_right_tread()
                        self.decrease_left_tread()
                    if self.angle % 360 > 180:
                        self.angle = 0

            elif end_angle - self.angle <= 180 and (end_angle - self.angle > 0 or end_angle - self.angle < -180):
                self.angle += self.turn_speed * time_passed
                if self.animation_cooldown == 0:
                    self.increase_left_tread()
                    self.decrease_right_tread()
                if self.angle % 360 > end_angle and self.angle - end_angle < 10:
                    self.angle = end_angle
            else:
                self.angle -= self.turn_speed * time_passed
                if self.animation_cooldown == 0:
                    self.increase_right_tread()
                    self.decrease_left_tread()
                if self.angle % 360 < end_angle and end_angle - self.angle < 10:
                    self.angle = end_angle
            self.image = pygame.transform.rotate(self.sprites[self.left_tread][self.right_tread], int(self.angle))
            self.rect.x = self.x - (self.rect.width/2)
            self.rect.y = self.y - (self.rect.width/2)

    def move_player(self, time_passed, direction):
        movement_x = math.cos(self.angle * math.pi / 180) * self.speed * time_passed
        movement_y = math.sin(self.angle * math.pi / 180) * -1 * self.speed * time_passed
        self.x += movement_x * direction
        self.y += movement_y * direction
        self.rect.x = self.x - self.rect.width/2
        self.rect.y = self.y - self.rect.width/2

    def increase_left_tread(self):
        self.left_tread += 1
        if self.left_tread > 3:
            self.left_tread = 0

    def increase_right_tread(self):
        self.right_tread += 1
        if self.right_tread > 3:
            self.right_tread = 0

    def decrease_left_tread(self):
        self.left_tread -= 1
        if self.left_tread < 0:
            self.left_tread = 3

    def decrease_right_tread(self):
        self.right_tread -= 1
        if self.right_tread < 0:
            self.right_tread = 3


    def check_wall_collisions(self, walls):
        for sprite in walls.sprites():
            if sprite.rect.colliderect(self.rect):
                left_over_lap = sprite.rect.right - self.rect.left
                right_over_lap = self.rect.right - sprite.rect.left
                top_over_lap = sprite.rect.bottom - self.rect.top
                bottom_over_lap = self.rect.bottom - sprite.rect.top
                lap_list = [left_over_lap, right_over_lap, top_over_lap, bottom_over_lap]
                lap_list.sort()
                if lap_list[0] == lap_list[1]:
                    continue

                if lap_list[0] is left_over_lap:
                    self.rect.left = sprite.rect.right
                    self.x = self.rect.centerx
                elif lap_list[0] is right_over_lap:
                    self.rect.right = sprite.rect.left
                    self.x = self.rect.centerx
                elif lap_list[0] is top_over_lap:
                    self.rect.top = sprite.rect.bottom
                    self.y = self.rect.centery
                else:
                    self.rect.bottom = sprite.rect.top
                    self.y = self.rect.centery

    def blit(self, surface):
        surface.blit(self.image, (self.x - int(self.image.get_width() / 2), self.y - int(self.image.get_height() / 2)))
        surface.blit(self.turret, (self.x - int(self.turret.get_width() / 2), self.y - int(self.turret.get_height() / 2)))
        if False:
            pygame.draw.rect(surface, (255, 0, 0), self.rect)
            pygame.draw.circle(surface, "Pink", (self.x, self.y), 3)

    def blit_bullets(self, surface):
        for b in self.bullets:
            surface.blit(b.image, (self.x, self.y))

    def update(self, time_passed, walls, surface):
        self.update_animation_buffer(time_passed)
        self.get_inputs(time_passed)
        self.check_wall_collisions(walls)
        self.blit(surface)
        self.blit_bullets(surface)
