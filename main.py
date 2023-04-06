import math
import sys
import pygame
from pygame.locals import *

up_kb = [K_w, K_UP]
down_kb = [K_s, K_DOWN]
left_kb = [K_a, K_LEFT]
right_kb = [K_d, K_RIGHT]

ratio = [16, 9]

BACKGROUND = (100, 100, 100)
FPS = 60
cap_frame_rate = False
show_fps = True


if __name__ == '__main__':
    pygame.init()
    timeClock = pygame.time.Clock()
    fpsClock = pygame.time.Clock()
    info = pygame.display.Info()
    width = info.current_w
    height = info.current_h
    for i in range(10):
        width -= ratio[0]
        height -= ratio[1]
    DISPLAYSURF = pygame.display.set_mode((width, height))
    pygame.display.set_caption('tank game')
    font = pygame.font.Font("freesansbold.ttf", 30)

    time = 0
    fps_time = 0
    fps_update = 500
    curr_fps = 0

    while True:
        DISPLAYSURF.fill(BACKGROUND)
        if show_fps:
            fps_time += time
            if fps_time >= fps_update:
                curr_fps = fpsClock.get_fps()
                fps_time = fps_time % fps_update
            fps_text = font.render("FPS: " + str(math.floor(curr_fps)), False, (255, 255, 255))
            DISPLAYSURF.blit(fps_text, (5, 5))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        time = timeClock.tick()

        pygame.display.update()
        if cap_frame_rate:
            fpsClock.tick(FPS)
        else:
            fpsClock.tick()