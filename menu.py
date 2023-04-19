import pygame
from pygame.locals import *


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


class Menu:
    def __init__(self, display_surface):
        self.surface = display_surface
        self.menu_buttons = []
        self.menu_buttons.append(Button(Rect(self.surface.get_width() / 2 - 200, self.surface.get_height() / 4 - 50, 400, 100), "FUN TANK GAME", (100, 100, 100), (0, 255, 0)))
        self.menu_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 - 25, 100, 50), "Play", (0, 0, 0), (255, 255, 255)))

    def run(self):
        for button in self.menu_buttons:
            button.draw(self.surface)
