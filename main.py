import math
import sys
import pygame
import random
from pygame.locals import *
from level import *
from player import *

width = 1480
height = 1000

BACKGROUND = (100, 100, 100)
FPS = 120
cap_frame_rate = False
show_fps = True
skip_menu = False

in_level = False
menu_buttons = []


class Button:
    def __init__(self, rect, content="Hello World", b_color=(100, 100, 100), t_color=(0, 0, 0)):
        self.x = rect.x
        self.y = rect.y
        self.width = rect.width
        self.height = rect.height
        self.text = content
        self.b_c = b_color
        self.t_c = t_color
        self.rect = rect
        self.pr = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.b_c, self.rect, 0, 3)
        butt_font = pygame.font.SysFont("lucidasans.ttf", int(self.width / len(str(self.text)) * 2))
        butt_text = butt_font.render(self.text, True, self.t_c)
        screen.blit(butt_text, (self.x + (self.width - butt_text.get_width()) / 2, self.y + (self.height - butt_text.get_height()) / 2))

    def mouse_over(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            return True
        return False

    def set_text_size(self, size):
        self.width = int(size / 2 * len(str(self.text)))
        self.rect = Rect(self.x, self.y, self.width, self.height)

    def set_x(self, x_val):
        self.x = x_val
        self.rect = Rect(x_val, self.rect.y, self.rect.width, self.rect.height)

    def press(self, p):
        self.pr = p

    def is_pressed(self):
        return self.pr


def display_menu():
    for button in menu_buttons:
        button.draw(DISPLAYSURF)


if __name__ == '__main__':
    pygame.init()
    timeClock = pygame.time.Clock()
    fpsClock = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((width, height))
    pygame.display.set_caption('tank game')
    font = pygame.font.Font("freesansbold.ttf", 30)

    level = Level(DISPLAYSURF, 1)
    menu_buttons.append(Button(Rect(DISPLAYSURF.get_width() / 2 - 200, DISPLAYSURF.get_height() / 4 - 50, 400, 100), "FUN TANK GAME", (100, 100, 100), (0, 255, 0)))
    menu_buttons.append(Button(Rect(DISPLAYSURF.get_width() / 2 - 50, DISPLAYSURF.get_height() / 2 - 25, 100, 50), "Play", (0, 0, 0), (255, 255, 255)))
    if skip_menu:
        in_level = True

    time = 0
    fps_time = 0
    fps_update = 500
    curr_fps = 0

    while True:
        DISPLAYSURF.fill(BACKGROUND)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                level = Level(DISPLAYSURF, 1)
                in_level = True

        time = timeClock.tick()

        if in_level:
            level.run(time)
        else:
            display_menu()
        # pygame.draw.circle(DISPLAYSURF, (255, 0, 0), (100, 100), 2.5)

        if show_fps:
            fps_time += time
            if fps_time >= fps_update:
                curr_fps = fpsClock.get_fps()
                fps_time = fps_time % fps_update
            fps_text = font.render("FPS: " + str(math.floor(curr_fps)), False, (255, 255, 255))
            DISPLAYSURF.blit(fps_text, (5, 5))

        pygame.display.update()
        if cap_frame_rate:
            fpsClock.tick(FPS)
        else:
            fpsClock.tick()
