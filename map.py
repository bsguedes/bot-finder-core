import random

SIZE = 25
SEED = 1337
WATER_LEVEL = 30
REDUCTION_RATE = 20

class Map:
    def __init__(self):
        random.seed = SEED
        self.board = [[0]*SIZE for x in range(SIZE)]

    def generate(self):
        sx = int(SIZE / 2)
        sy = int(SIZE / 2)        
        self._generate(sx, sy, 100)

    def _generate(self, x, y, v):
        if x >= 0 and x < SIZE and y >= 0 and y < SIZE and self.board[x][y] == 0:            
            self.board[x][y] = v        
            self._generate(x-1, y, self.red(v))
            self._generate(x+1, y, self.red(v))
            self._generate(x, y-1, self.red(v))
            self._generate(x, y+1, self.red(v))
            
    def red(self, v):
        return v * ((REDUCTION_RATE - 1) / REDUCTION_RATE + random.random() / REDUCTION_RATE)
        
    def size(self):
        return SIZE

    def water_level(self):
        return WATER_LEVEL
