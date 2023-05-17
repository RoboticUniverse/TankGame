import sys

import pygame
from pygame.locals import *

color = [(0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]

class Button:
    def __init__(self, rect, content="Hello World", num=-1, b_color=(100, 100, 100), t_color=(0, 0, 0), no_background=False, enabled=False, value=0):
        self.text = content
        self.num = num
        self.b_c = b_color
        self.t_c = t_color
        self.rect = rect
        self.pr = False
        self.no_back = no_background
        self.enabled = enabled
        self.value = value

    def draw(self, screen):
        if not self.no_back:
            pygame.draw.rect(screen, self.b_c, self.rect, 0, 3)
        if len(str(self.text)) > 0:
            if self.text == "0" or self.text == "5":
                butt_font = pygame.font.SysFont("lucidasans.ttf", int(self.rect.width))
            else:
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

    def change_color(self):
        if self.b_c == (0, 255, 0):
            self.b_c = (255, 0, 0)
            self.enabled = False
        else:
            self.b_c = (0, 255, 0)
            self.enabled = True

    def change_text_color(self):
        if self.t_c == (255, 255, 255):
            self.t_c = (150, 150, 150)
        else:
            self.t_c = (255, 255, 255)

    def set_back_color(self, col):
        self.b_c = col

    def change_text(self, text):
        self.text = text

    def get_enabled(self):
        return self.enabled

    def press(self, p):
        self.pr = p

    def is_pressed(self):
        return self.pr

    def set_value(self, val):
        self.value = val

    def get_num(self):
        return self.num

    def get_width(self):
        return self.rect.width

    def get_text(self):
        return self.text

    def get_text_color(self):
        return self.t_c

    def get_value(self):
        return self.value


class Menu:
    def __init__(self, display_surface):
        self.surface = display_surface
        self.menu_buttons = []
        self.setting_buttons = []
        self.control_buttons = []
        self.other_buttons = []
        self.print_buttons = []
        self.create_buttons()
        self.mouse_down = False
        self.close_menu = False

    def action(self, num):
        if num == 0:
            self.close_menu = True
        elif num == 1:
            self.print_buttons = self.setting_buttons
        elif num == 2:
            pygame.quit()
            sys.exit()
        elif num == 3:
            self.print_buttons = self.menu_buttons
        elif num == 4:
            self.print_buttons = self.control_buttons
        elif 5 <= num <= 8:
            n = 2
            nu = 2
            for i in range(4):
                if self.control_buttons[n].get_enabled() and i + 5 != num:
                    self.control_buttons[n].change_color()
                if i + 5 == num:
                    nu = n
                n += 11
            self.control_buttons[nu].change_color()
        elif 9 <= num <= 12:
            n = 3
            for i in range(num - 9):
                n += 11
            self.control_buttons[n].change_color()
            for i in range(1, 5):
                self.control_buttons[n+i].change_text_color()
        elif 13 <= num <= 20 or 33 <= num <= 36:
            # 5 16 27 38
            # 7 18 29 40
            if num < 30:
                n = 6
                nu = 13
                change = -5
                if num >= 17:
                    nu = 17
                    change = 5
                for i in range(num - nu):
                    n += 11
                cap = 45
            else:
                n = 3
                change = 5
                if num % 2 == 1:
                    change = -5
                if num > 34:
                    n = 8
                cap = 100
            if (int(self.print_buttons[n].get_text()) > 0 or change > 0) and (int(self.print_buttons[n].get_text()) < cap or change < 0) and self.print_buttons[n].get_text_color() == (255, 255, 255):
                self.print_buttons[n].change_text(str(int(self.print_buttons[n].get_text()) + change))
                # self.control_buttons[n].set_text_size(45)
        elif 21 <= num <= 28:
            n = 10
            nu = 21
            change = -1
            if num >= 25:
                nu = 25
                change = 1
            for i in range(num - nu):
                n += 11
            new_val = self.control_buttons[n].get_value() + change
            if new_val > len(color) - 1:
                new_val = 0
            if new_val < 0:
                new_val = len(color) - 1
            self.control_buttons[n].set_value(new_val)
            self.control_buttons[n].set_back_color(color[new_val])
        elif num == 29:
            self.print_buttons = self.other_buttons
        elif 30 <= num <= 32:
            n = num - 29
            if n > 1:
                n += 3
            self.other_buttons[n].change_color()
            if num % 2 == 0:
                for i in range(1, 4):
                    self.other_buttons[n+i].change_text_color()

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
        if self.close_menu:
            return [self.close_menu, self.control_buttons[2].get_enabled(), self.control_buttons[13].get_enabled(), self.control_buttons[24].get_enabled(), self.control_buttons[35].get_enabled(), self.control_buttons[3].get_enabled(), self.control_buttons[14].get_enabled(), self.control_buttons[25].get_enabled(), self.control_buttons[36].get_enabled(), int(self.control_buttons[6].get_text()), int(self.control_buttons[17].get_text()), int(self.control_buttons[28].get_text()), int(self.control_buttons[39].get_text()), self.control_buttons[10].get_value(), self.control_buttons[21].get_value(), self.control_buttons[32].get_value(), self.control_buttons[43].get_value()]
        fps = int(self.other_buttons[8].get_text())
        if not self.other_buttons[6].get_enabled():
            fps = -1
        volume = int(self.other_buttons[3].get_text())
        if not self.other_buttons[1].get_enabled():
            print("bruh")
            volume = 0
        return [self.close_menu, self.other_buttons[5].get_enabled(), fps, volume]

    def create_buttons(self):
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
        self.setting_buttons.append(Button(Rect(self.surface.get_width() / 2 - 200, self.surface.get_height() / 4 - 50, 400, 100), "Settings", -1, (0, 0, 0), (255, 255, 255)))
        self.setting_buttons[0].set_x(self.surface.get_width() / 2 - self.setting_buttons[0].get_width() / 2)
        self.setting_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 - 100, 100, 50), "Controls", 4, (0, 0, 0), (255, 255, 255)))
        self.setting_buttons[1].set_text_size(45)
        self.setting_buttons[1].set_x(self.surface.get_width() / 2 - self.setting_buttons[1].get_width() / 2)
        self.setting_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 - 25, 100, 50), "Other", 29, (0, 0, 0), (255, 255, 255)))
        self.setting_buttons[2].set_text_size(45)
        self.setting_buttons[2].set_x(self.surface.get_width() / 2 - self.setting_buttons[2].get_width() / 2)
        self.setting_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 50, 100, 50), "Back", 3, (0, 0, 0), (255, 255, 255)))
        self.setting_buttons[3].set_text_size(45)
        self.setting_buttons[3].set_x(self.surface.get_width() / 2 - self.setting_buttons[3].get_width() / 2)
        self.control_buttons = []
        # 0
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 200, self.surface.get_height() / 4 - 125, 400, 100), "Control Settings", -1, (0, 0, 0), (255, 255, 255)))
        self.control_buttons[-1].set_x(self.surface.get_width() / 2 - self.control_buttons[-1].get_width() / 2)
        # Player 1
        # 1
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 - 200, 100, 50), "Player 1", -1, (0, 0, 0), (255, 255, 255)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 - self.control_buttons[-1].get_width() / 2)
        # 2
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 - 125, 100, 50), "Mouse", 5, (255, 0, 0), (255, 255, 255)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 - self.control_buttons[-1].get_width() / 2)
        # 3
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 - 50, 100, 50), "Auto-Turn", 9, (255, 0, 0), (255, 255, 255)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 - self.control_buttons[-1].get_width() / 2)
        # 4
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 25, 100, 50), "Tolerance", -1, (0, 0, 0), (150, 150, 150)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 - self.control_buttons[-1].get_width() / 2)
        # 5
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 100, 100, 50), "<", 13, (0, 0, 0), (150, 150, 150)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 - self.control_buttons[-1].get_width() / 2 - 50)
        # 6
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 100, 100, 50), "20", -1, (0, 0, 0), (150, 150, 150)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 - self.control_buttons[-1].get_width() / 2)
        # 7
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 100, 100, 50), ">", 17, (0, 0, 0), (150, 150, 150)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 - self.control_buttons[-1].get_width() / 2 + 50)
        # 8
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 175, 100, 50), "Color", -1, (0, 0, 0), (255, 255, 255)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 - self.control_buttons[-1].get_width() / 2)
        # 9
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 250, 100, 50), "<", 21, (0, 0, 0), (255, 255, 255)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 - self.control_buttons[-1].get_width() / 2 - 50)
        # 10
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 250, 50, 50), "", -1, (0, 255, 0), (255, 255, 255), False, False, 0))
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 - self.control_buttons[-1].get_width() / 2)
        # 11
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 250, 100, 50), ">", 25, (0, 0, 0), (255, 255, 255)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 - self.control_buttons[-1].get_width() / 2 + 50)
        # Player 2
        # 12
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 - 200, 100, 50), "Player 2", -1, (0, 0, 0), (255, 255, 255)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 * 2 - self.control_buttons[-1].get_width() / 2)
        # 13
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 - 125, 100, 50), "Mouse", 6, (255, 0, 0), (255, 255, 255)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 * 2 - self.control_buttons[-1].get_width() / 2)
        # 14
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 - 50, 100, 50), "Auto-Turn", 10, (255, 0, 0), (255, 255, 255)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 * 2 - self.control_buttons[-1].get_width() / 2)
        # 15
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 25, 100, 50), "Tolerance", -1, (0, 0, 0), (150, 150, 150)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 * 2 - self.control_buttons[-1].get_width() / 2)
        # 16
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 100, 100, 50), "<", 14, (0, 0, 0), (150, 150, 150)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 * 2 - self.control_buttons[-1].get_width() / 2 - 50)
        # 17
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 100, 100, 50), "20", -1, (0, 0, 0), (150, 150, 150)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 * 2 - self.control_buttons[-1].get_width() / 2)
        # 18
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 100, 100, 50), ">", 18, (0, 0, 0), (150, 150, 150)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 * 2 - self.control_buttons[-1].get_width() / 2 + 50)
        # 19
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 175, 100, 50), "Color", -1, (0, 0, 0), (255, 255, 255)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 * 2 - self.control_buttons[-1].get_width() / 2)
        # 20
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 250, 100, 50), "<", 22, (0, 0, 0), (255, 255, 255)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 * 2 - self.control_buttons[-1].get_width() / 2 - 50)
        # 21
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 250, 50, 50), "", -1, (0, 0, 255), (255, 255, 255), False, False, 1))
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 * 2 - self.control_buttons[-1].get_width() / 2)
        # 22
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 250, 100, 50), ">", 26, (0, 0, 0), (255, 255, 255)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 * 2 - self.control_buttons[-1].get_width() / 2 + 50)
        # Player 3
        # 23
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 - 200, 100, 50), "Player 3", -1, (0, 0, 0), (255, 255, 255)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 * 3 - self.control_buttons[-1].get_width() / 2)
        # 24
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 - 125, 100, 50), "Mouse", 7, (255, 0, 0), (255, 255, 255)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 * 3 - self.control_buttons[-1].get_width() / 2)
        # 25
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 - 50, 100, 50), "Auto-Turn", 11, (255, 0, 0), (255, 255, 255)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 * 3 - self.control_buttons[-1].get_width() / 2)
        # 26
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 25, 100, 50), "Tolerance", -1, (0, 0, 0), (150, 150, 150)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 * 3 - self.control_buttons[-1].get_width() / 2)
        # 27
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 100, 100, 50), "<", 15, (0, 0, 0), (150, 150, 150)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 * 3 - self.control_buttons[-1].get_width() / 2 - 50)
        # 28
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 100, 100, 50), "20", -1, (0, 0, 0), (150, 150, 150)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 * 3 - self.control_buttons[-1].get_width() / 2)
        # 29
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 100, 100, 50), ">", 19, (0, 0, 0), (150, 150, 150)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 * 3 - self.control_buttons[-1].get_width() / 2 + 50)
        # 30
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 175, 100, 50), "Color", -1, (0, 0, 0), (255, 255, 255)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 * 3 - self.control_buttons[-1].get_width() / 2)
        # 31
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 250, 100, 50), "<", 23, (0, 0, 0), (255, 255, 255)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 * 3 - self.control_buttons[-1].get_width() / 2 - 50)
        # 32
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 250, 50, 50), "", -1, (255, 255, 0), (255, 255, 255), False, False, 2))
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 * 3 - self.control_buttons[-1].get_width() / 2)
        # 33
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 250, 100, 50), ">", 27, (0, 0, 0), (255, 255, 255)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 * 3 - self.control_buttons[-1].get_width() / 2 + 50)
        # Player 4
        # 34
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 - 200, 100, 50), "Player 4", -1, (0, 0, 0), (255, 255, 255)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 * 4 - self.control_buttons[-1].get_width() / 2)
        # 35
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 - 125, 100, 50), "Mouse", 8, (255, 0, 0), (255, 255, 255)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 * 4 - self.control_buttons[-1].get_width() / 2)
        # 36
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 - 50, 100, 50), "Auto-Turn", 12, (255, 0, 0), (255, 255, 255)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 * 4 - self.control_buttons[-1].get_width() / 2)
        # 37
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 25, 100, 50), "Tolerance", -1, (0, 0, 0), (150, 150, 150)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 * 4 - self.control_buttons[-1].get_width() / 2)
        # 38
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 100, 100, 50), "<", 16, (0, 0, 0), (150, 150, 150)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 * 4 - self.control_buttons[-1].get_width() / 2 - 50)
        # 39
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 100, 100, 50), "20", -1, (0, 0, 0), (150, 150, 150)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 * 4 - self.control_buttons[-1].get_width() / 2)
        # 40
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 100, 100, 50), ">", 20, (0, 0, 0), (150, 150, 150)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 * 4 - self.control_buttons[-1].get_width() / 2 + 50)
        # 41
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 175, 100, 50), "Color", -1, (0, 0, 0), (255, 255, 255)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 * 4 - self.control_buttons[-1].get_width() / 2)
        # 42
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 250, 100, 50), "<", 24, (0, 0, 0), (255, 255, 255)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 * 4 - self.control_buttons[-1].get_width() / 2 - 50)
        # 43
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 250, 50, 50), "", -1, (255, 0, 255), (255, 255, 255), False, False, 3))
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 * 4 - self.control_buttons[-1].get_width() / 2)
        # 44
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 250, 100, 50), ">", 28, (0, 0, 0), (255, 255, 255)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 5 * 4 - self.control_buttons[-1].get_width() / 2 + 50)
        # 45
        self.control_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 350, 100, 50), "Back", 1, (0, 0, 0), (255, 255, 255)))
        self.control_buttons[-1].set_text_size(45)
        self.control_buttons[-1].set_x(self.surface.get_width() / 2 - self.control_buttons[-1].get_width() / 2)
        self.other_buttons = []
        self.other_buttons.append(Button(Rect(self.surface.get_width() / 2 - 200, self.surface.get_height() / 4 - 125, 400, 100), "Other Settings", -1, (0, 0, 0), (255, 255, 255)))
        self.other_buttons[-1].set_x(self.surface.get_width() / 2 - self.other_buttons[-1].get_width() / 2)
        self.other_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 - 175, 100, 50), "Volume", 30, (0, 255, 0), (255, 255, 255), False, True))
        self.other_buttons[-1].set_text_size(45)
        self.other_buttons[-1].set_x(self.surface.get_width() / 2 - self.other_buttons[-1].get_width() / 2)
        self.other_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 - 100, 100, 50), "<", 33, (0, 0, 0), (255, 255, 255)))
        self.other_buttons[-1].set_text_size(45)
        self.other_buttons[-1].set_x(self.surface.get_width() / 2 - self.other_buttons[-1].get_width() / 2 - 50)
        self.other_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 - 100, 100, 50), "100", -1, (0, 0, 0), (255, 255, 255)))
        self.other_buttons[-1].set_text_size(45)
        self.other_buttons[-1].set_x(self.surface.get_width() / 2 - self.other_buttons[-1].get_width() / 2)
        self.other_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 - 100, 100, 50), ">", 34, (0, 0, 0), (255, 255, 255)))
        self.other_buttons[-1].set_text_size(45)
        self.other_buttons[-1].set_x(self.surface.get_width() / 2 - self.other_buttons[-1].get_width() / 2 + 50)
        self.other_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 - 25, 100, 50), "Show FPS", 31, (255, 0, 0), (255, 255, 255)))
        self.other_buttons[-1].set_text_size(45)
        self.other_buttons[-1].set_x(self.surface.get_width() / 2 - self.other_buttons[-1].get_width() / 2)
        self.other_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 50, 100, 50), "FPS Cap", 32, (255, 0, 0), (255, 255, 255)))
        self.other_buttons[-1].set_text_size(45)
        self.other_buttons[-1].set_x(self.surface.get_width() / 2 - self.other_buttons[-1].get_width() / 2)
        self.other_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 125, 100, 50), "<", 35, (0, 0, 0), (150, 150, 150)))
        self.other_buttons[-1].set_text_size(45)
        self.other_buttons[-1].set_x(self.surface.get_width() / 2 - self.other_buttons[-1].get_width() / 2 - 50)
        self.other_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 125, 100, 50), "60", -1, (0, 0, 0), (150, 150, 150)))
        self.other_buttons[-1].set_text_size(45)
        self.other_buttons[-1].set_x(self.surface.get_width() / 2 - self.other_buttons[-1].get_width() / 2)
        self.other_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 125, 100, 50), ">", 36, (0, 0, 0), (150, 150, 150)))
        self.other_buttons[-1].set_text_size(45)
        self.other_buttons[-1].set_x(self.surface.get_width() / 2 - self.other_buttons[-1].get_width() / 2 + 50)
        self.other_buttons.append(Button(Rect(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 275, 100, 50), "Back", 1, (0, 0, 0), (255, 255, 255)))
        self.other_buttons[-1].set_text_size(45)
        self.other_buttons[-1].set_x(self.surface.get_width() / 2 - self.other_buttons[-1].get_width() / 2)
        self.print_buttons = self.menu_buttons
