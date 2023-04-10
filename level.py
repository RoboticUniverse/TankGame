import pygame

# [South, East, North, West]
directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def create_outline(number):
    try:
        room = pygame.image.load("sprites/rooms/" + str(number) + ".png")
        outline = []
        for h in range(room.get_height()):
            for w in range(room.get_width()):
                if room.get_at((w, h)) == (0, 0, 0, 255) or room.get_at((w, h)) == (255, 0, 0, 255):
                    outline.append(pygame.Rect(w, h, 1, 1))
        rtn = ""
        for o in outline:
            rtn += str(o.x) + " " + str(o.y) + ", "
        # print(rtn[:-2])
        return outline
    except FileNotFoundError:
        print("Requested Room " + str(number) + " Does Not Exist")
    return []


# 1 left
# 2 bottom
# 3 right
# 4 top
def get_reds(number, side):
    try:
        room = pygame.image.load("sprites/rooms/" + str(number) + ".png")
        reds = []
        if side == 1 or side == 3:
            for h in range(room.get_height()):
                for w in range(room.get_width()):
                    if side == 3:
                        w = room.get_width() - 1 - w
                    if room.get_at((w, h)) == (255, 0, 0, 255):
                        reds.append((w, h))
                        break
                    if room.get_at((w, h)) != (0, 255, 0, 255):
                        break
        elif side == 2 or side == 4:
            for w in range(room.get_width()):
                for h in range(room.get_height()):
                    if side == 2:
                        h = room.get_height() - 1 - h
                    if room.get_at((w, h)) == (255, 0, 0, 255):
                        reds.append((w, h))
                        break
                    if room.get_at((w, h)) != (0, 255, 0, 255):
                        break
        return reds
    except FileNotFoundError:
        print("Requested Room " + str(number) + " Does Not Exist")
    return []


def get_greens(number):
    try:
        room = pygame.image.load("sprites/rooms/" + str(number) + ".png")
        greens = []
        for w in range(room.get_width()):
            for h in range(room.get_height()):
                if room.get_at((w, h)) == (0, 255, 0, 255):
                    greens.append((w, h))
        return greens
    except FileNotFoundError:
        print("Requested Room " + str(number) + " Does Not Exist")
    return []


class Room:
    def __init__(self, x, y, number=1):
        self.x = x
        self.y = y
        self.number = number
        self.outline = create_outline(number)
        try:
            room = pygame.image.load("sprites/rooms/" + str(number) + ".png")
            self.width = room.get_width()
            self.height = room.get_height()
        except FileNotFoundError:
            print("Requested Room " + str(number) + " Does Not Exist")

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_outline(self):
        return self.outline

    def get_number(self):
        return self.number

    def scale_outline(self, scale, offset_x, offset_y):
        for o in self.outline:
            o.x = o.x * scale + offset_x
            o.y = o.y * scale + offset_y
            o.width *= scale
            o.height *= scale

    def __str__(self):
        return "X: " + str(self.x) + ", Y: " + str(self.y)

