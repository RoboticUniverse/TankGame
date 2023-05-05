import sys

import pygame
from pygame.locals import *


class Button:
    def __init__(self, rect, content="Hello World", num=-1, b_color=(100, 100, 100), t_color=(0, 0, 0), no_background=False):
        self.text = content
        self.num = num
        self.b_c = b_color
        self.t_c = t_color
        self.rect = rect
        self.pr = False
        self.no_back = no_background

    def draw(self, screen):
        if not self.no_back:
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


class Menu:
    def __init__(self, display_surface):
        self.surface = display_surface
        self.menu_buttons = []
        self.menu_buttons.append(Button(Rect(self.surface.get_width() / 2 - 200, self.surface.get_height() / 4 - 50, 400, 100), "FUN TANK GAME", -1, (0, 0, 0), (0, 255, 0)))
        self.menu_buttons[0].set_x(self.surface.get_width() / 2 - self.menu_buttons[0].get_width() / 2)
        self.menu_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 - 100, 100, 50), "Play", 0, (0, 0, 0), (255, 255, 255)))
        self.menu_buttons[1].set_text_size(45)
        self.menu_buttons[1].set_x(self.surface.get_width() / 2 - self.menu_buttons[1].get_width() / 2)
        self.menu_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 - 25, 100, 50), "Settings", 1, (0, 0, 0), (255, 255, 255)))
        self.menu_buttons[2].set_text_size(45)
        self.menu_buttons[2].set_x(self.surface.get_width() / 2 - self.menu_buttons[2].get_width() / 2)
        self.menu_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 50, 100, 50), "Quit :(", 2, (0, 0, 0), (255, 255, 255)))
        self.menu_buttons[3].set_text_size(45)
        self.menu_buttons[3].set_x(self.surface.get_width() / 2 - self.menu_buttons[3].get_width() / 2)
        self.setting_buttons = []
        self.setting_buttons.append(Button(Rect(self.surface.get_width() / 2 - 200, self.surface.get_height() / 4 - 50, 400, 100), "Settings", -1, (0, 0, 0), (0, 255, 0)))
        self.setting_buttons[0].set_x(self.surface.get_width() / 2 - self.setting_buttons[0].get_width() / 2)
        self.setting_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 - 100, 100, 50), "Controls", -1, (0, 0, 0), (255, 255, 255)))
        self.setting_buttons[1].set_text_size(45)
        self.setting_buttons[1].set_x(self.surface.get_width() / 2 - self.setting_buttons[1].get_width() / 2)
        self.setting_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 - 25, 100, 50), "Other", -1, (0, 0, 0), (255, 255, 255)))
        self.setting_buttons[2].set_text_size(45)
        self.setting_buttons[2].set_x(self.surface.get_width() / 2 - self.setting_buttons[2].get_width() / 2)
        self.setting_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 50, 100, 50), "Back", 3, (0, 0, 0), (255, 255, 255)))
        self.setting_buttons[3].set_text_size(45)
        self.setting_buttons[3].set_x(self.surface.get_width() / 2 - self.setting_buttons[3].get_width() / 2)
        self.print_buttons = self.menu_buttons
        self.mouse_down = False
        self.close_menu = False
        self.setting = False

    def action(self, num):
        if num == 0:
            self.close_menu = True
        elif num == 1:
            self.setting = True
            self.print_buttons = self.setting_buttons
        elif num == 2:
            pygame.quit()
            sys.exit()
        elif num == 3:
            self.setting = False
            self.print_buttons = self.menu_buttons
        return False

    def run(self, mouse_clicked):
        self.close_menu = False
        if self.mouse_down != mouse_clicked:
            self.mouse_down = mouse_clicked
            if mouse_clicked:
                for button in self.print_buttons:
                    if button.mouse_over():
                        button.press(True)
            else:
                for button in self.print_buttons:
                    if button.is_pressed() and button.mouse_over():
                        self.action(button.get_num())
                    button.press(False)
        for button in self.print_buttons:
            button.draw(self.surface)
        return self.close_menu
