import random

DIRS = {0: (1, 0), 1: (0, 1), 2: (-1, 0), 3: (0, -1)}


class Player:    
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.vision = None

    def move(self, vision):
        self.vision = vision
        return random.randint(0, 5) % 4

    def update_position(self, direction):
        self.x += DIRS[direction][0]
        self.y += DIRS[direction][1]
