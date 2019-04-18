import random

DIRS = {0: (1, 0), 1: (0, 1), 2: (-1, 0), 3: (0, -1)}


class Player:    
    def __init__(self, name, pid, x, y):
        self.name = name
        self.player_id = pid - 1
        self.x = x
        self.y = y
        self.vision = None
        self.prev_dir = None
        self.steps = 0

    def move(self, vision):
        self.vision = vision
        if random.randint(0, 10) == 0:
            self.prev_dir = None
        if self.prev_dir is None:
            direction = random.randint(0, 3) % 4
        else:
            direction = self.prev_dir
        self.prev_dir = direction
        self.steps += 1
        return direction

    def update_position(self, direction):
        self.x += DIRS[direction][0]
        self.y += DIRS[direction][1]
