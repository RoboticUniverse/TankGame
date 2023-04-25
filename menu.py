import sys

import pygame
from pygame.locals import *


class Button:
    def __init__(self, rect, content="Hello World", num=-1, b_color=(100, 100, 100), t_color=(0, 0, 0)):
        self.text = content
        self.num = num
        self.b_c = b_color
        self.t_c = t_color
        self.rect = rect
        self.pr = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.b_c, self.rect, 0, 3)
        butt_font = pygame.font.SysFont("lucidasans.ttf", int(self.rect.width / len(str(self.text)) * 2))
        butt_text = butt_font.render(self.text, True, self.t_c)
        screen.blit(butt_text, (self.rect.x + (self.rect.width - butt_text.get_width()) / 2, self.rect.y + (self.rect.height - butt_text.get_height()) / 2))

    def mouse_over(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            return True
        return False

    def set_text_size(self, size):
        self.rect.width = int(size / 2 * len(str(self.text)))

    def set_x(self, x_val):
        self.rect.x = x_val

    def press(self, p):
        self.pr = p

    def is_pressed(self):
        return self.pr

    def get_num(self):
        return self.num

    def get_width(self):
        return self.rect.width


def action(num):
    if num == 0:
        return True
    elif num == 1:
        # settings
        pass
    elif num == 2:
        pygame.quit()
        sys.exit()
    return False


class Menu:
    def __init__(self, display_surface):
        self.surface = display_surface
        self.menu_buttons = []
        self.menu_buttons.append(Button(Rect(self.surface.get_width() / 2 - 200, self.surface.get_height() / 4 - 50, 400, 100), "FUN TANK GAME", -1, (100, 100, 100), (0, 255, 0)))
        self.menu_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 - 100, 100, 50), "Play", 0, (0, 0, 0), (255, 255, 255)))
        self.menu_buttons[1].set_text_size(45)
        self.menu_buttons[1].set_x(self.surface.get_width() / 2 - self.menu_buttons[1].get_width() / 2)
        self.menu_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 - 25, 100, 50), "Settings", 1, (0, 0, 0), (255, 255, 255)))
        self.menu_buttons[2].set_text_size(45)
        self.menu_buttons[2].set_x(self.surface.get_width() / 2 - self.menu_buttons[2].get_width() / 2)
        self.menu_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 50, 100, 50), "Quit :(", 2, (0, 0, 0), (255, 255, 255)))
        self.menu_buttons[3].set_text_size(45)
        self.menu_buttons[3].set_x(self.surface.get_width() / 2 - self.menu_buttons[3].get_width() / 2)
        self.mouse_down = False

    def run(self, mouse_clicked):
        close_menu = False
        if self.mouse_down != mouse_clicked:
            self.mouse_down = mouse_clicked
            if mouse_clicked:
                for button in self.menu_buttons:
                    if button.mouse_over():
                        button.press(True)
            else:
                for button in self.menu_buttons:
                    if button.is_pressed() and button.mouse_over():
                        close_menu = action(button.get_num())
                    button.press(False)
        for button in self.menu_buttons:
            button.draw(self.surface)
        return close_menu
