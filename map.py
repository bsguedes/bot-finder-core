import random

SIZE = 500
TOP_LEVEL = 100
SEED = None
WATER_LEVEL = 5
REDUCTION_RATE = 50
TREE_RANGE_MIN, TREE_RANGE_MAX = 60, 70


class Map:
    def __init__(self):
        random.seed = SEED
        self.board = [[0]*SIZE for _ in range(SIZE)]

    def generate(self):
        sx = int(SIZE / 2)
        sy = int(SIZE / 2)
        queue = set()
        queue.add((sx, sy, TOP_LEVEL))
        while len(queue) > 0:
            (x, y, l) = queue.pop()
            if not self.board[x][y] == 0:
                continue
            self.board[x][y] = self.red(l)
            if x > 0:
                queue.add((x - 1, y, self.board[x][y]))
            if x < SIZE - 1:
                queue.add((x + 1, y, self.board[x][y]))
            if y > 0:
                queue.add((x, y - 1, self.board[x][y]))
            if y < SIZE - 1:
                queue.add((x, y + 1, self.board[x][y]))

    def red(self, v):
        return v * ((REDUCTION_RATE - 1) / REDUCTION_RATE + random.random() / REDUCTION_RATE)
        
    def size(self):
        return SIZE

    def water_level(self):
        return WATER_LEVEL

    def tree_range(self, v):
        return TREE_RANGE_MIN < v < TREE_RANGE_MAX
