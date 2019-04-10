import random

DIRS = {0: (1, 0), 1: (0, 1), 2: (-1, 0), 3: (0, -1)}


class Player:    
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def move(self, vision):
        return random.randint(0, 3)

    def update_position(self, dir):
        self.x += DIRS[dir][0]
        self.y += DIRS[dir][1]        
