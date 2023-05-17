import math

from level import *
from player import *
from menu import *

width = 1480
height = 1000

BACKGROUND = (100, 100, 100)
FPS = 60
cap_frame_rate = False
show_fps = False
skip_menu = False
volume = 100

in_level = False
mouse_clicked = False


if __name__ == '__main__':
    pygame.init()
    timeClock = pygame.time.Clock()
    fpsClock = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((width, height))
    pygame.display.set_caption('tank game')
    font = pygame.font.Font("freesansbold.ttf", 30)

    pygame.mixer.music.set_volume(.75)
    pygame.mixer.music.stop()
    pygame.mixer.music.load("sprites/menu.mp3")
    pygame.mixer.music.play(-1, 0.0)

    level = Level(DISPLAYSURF, 1)
    menu = Menu(DISPLAYSURF)
    if skip_menu:
        in_level = True
    run_menu = []

    time = 0
    fps_time = 0
    fps_update = 500
    curr_fps = 0

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONUP:
                mouse_clicked = pygame.mouse.get_pressed()[0]
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    level = Level(DISPLAYSURF, 1, run_menu)

        time = timeClock.tick()

        if in_level:
            DISPLAYSURF.fill((174, 140, 10))
            level.run(time)
        else:
            DISPLAYSURF.fill(BACKGROUND)
            run_menu = menu.run(mouse_clicked)
            if run_menu[0]:
                level = Level(DISPLAYSURF, 1, run_menu)
                in_level = True
                pygame.mixer.music.stop()
                pygame.mixer.music.load("sprites/music.mp3")
                pygame.mixer.music.play(-1, 0.0)
            else:
                show_fps = False
                if run_menu[1]:
                    show_fps = True
                cap_frame_rate = False
                if run_menu[2] > 0:
                    cap_frame_rate = True
                    FPS = run_menu[2]
                if volume != run_menu[3]:
                    pygame.mixer.music.set_volume(run_menu[3]/100*.75)
                    volume = run_menu[3]

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
