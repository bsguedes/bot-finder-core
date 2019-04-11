import random
import time
from math import sqrt

DIRS = {0: (1,  0),  1: (0,  1),  2: (-1,  0),  3: (0,  -1)}
SIZE = 900
TOP_LEVEL = 100
WATER_LEVEL = 5
TREE_LEVEL = 30
REDUCTION_RATE = 90
TREE_PERCENTAGE = 10
RIVERS = 20
RIVER_LEVEL = 10
LANDMARKS = 100
MASK = [[-1, -1, 1, 1, 1, -1, -1],
        [-1, 1, 1, 1, 1, 1, -1],
        [1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1],
        [-1, 1, 1, 1, 1, 1, -1],
        [-1, -1, 1, 1, 1, -1, -1]]
VISION_RADIUS = len(MASK)


class Map:
    def __init__(self):
        self.board = [[0] * SIZE for _ in range(SIZE)]
        self.trees = [[0] * SIZE for _ in range(SIZE)]
        self.players = []
        self.landmarks = []

    def add_land(self):
        start = time.time()
        print('Let there be land')
        generate(int(SIZE / 2), int(SIZE / 2), self.board, 0, generate_bias(0.999))
        print("And there was land... after %.2f seconds." % (time.time() - start))

    def add_trees(self):
        start = time.time()
        print('Let there be trees')
        land = self.land_mass()
        while self.tree_area() < land * TREE_PERCENTAGE / 100:
            x, y = self.find_elevation_point(WATER_LEVEL)
            generate(x, y, self.trees, random.randrange(TREE_LEVEL, TOP_LEVEL), generate_bias(0.93))
            print("And there were trees... after %.2f seconds." % (time.time() - start), self.tree_area(), land)

    def add_rivers(self):
        start = time.time()
        print('Let there be rivers')
        for _ in range(RIVERS):
            x, y = self.find_water_point()
            upwards(x, y, self.board, random.randrange(RIVER_LEVEL, TREE_LEVEL))
            print("And there were rivers... after %.2f seconds." % (time.time() - start))

    def add_landmarks(self):
        start = time.time()
        print('Let there be landmarks')
        for i in range(LANDMARKS):
            x, y = self.find_elevation_point(WATER_LEVEL)
            while self.trees[x][y] != 0 or self.min_dist(self.landmarks, x, y) < 2 * VISION_RADIUS:
                x, y = self.find_elevation_point(WATER_LEVEL)
            self.landmarks.append((x, y))
        print("And there were landmarks... after %.2f seconds." % (time.time() - start))

    def add_players(self, player_count):
        for i in range(player_count):
            x, y = self.find_elevation_point(WATER_LEVEL * 2)
            while self.trees[x][y] != 0 or self.board[x][y] > TREE_LEVEL or self.min_dist(self.players, x,
                                                                                          y) < SIZE / VISION_RADIUS:
                x, y = self.find_elevation_point(WATER_LEVEL * 2)
            print("Let there be player ", i + 1, self.board[x][y])
            self.players.append((x, y))

    def is_valid_move(self, x, y, direction):
        x += DIRS[direction][0]
        y += DIRS[direction][1]
        return not self.trees[x][y] and not (x, y) in self.landmarks and self.board[x][y] > WATER_LEVEL

    def get_vision(self, x, y):        
        vision = MASK.copy()        
        x1 = x - int(VISION_RADIUS / 2)
        y1 = y - int(VISION_RADIUS / 2)
        for i in range(VISION_RADIUS):
            for j in range(VISION_RADIUS):
                v = self.board[x1+i][y1+j]
                t = self.trees[x1+i][y1+j]                
                if MASK[i][j] == -1:
                    vision[i][j] = -1
                elif (x1 + i, y1 + j) in self.landmarks:
                    vision[i][j] = TOP_LEVEL + self.landmarks.index((x1 + i, y1 + j))
                elif v < self.water_level():
                    vision[i][j] = 1
                elif t > self.tree_level():
                    vision[i][j] = 2
                else:
                    vision[i][j] = 0

    def find_water_point(self):
        while True:
            x = int(random.random() * SIZE)
            y = int(random.random() * SIZE)
            if self.board[x][y] < WATER_LEVEL:
                return x, y

    def find_elevation_point(self, level):
        while True:
            x = int(random.random() * SIZE)
            y = int(random.random() * SIZE)
            if self.board[x][y] > level:
                return x, y

    def land_mass(self):
        land = 0
        for x in range(SIZE):
            for y in range(SIZE):
                if self.board[x][y] > WATER_LEVEL:
                    land += 1
        return land

    def tree_area(self):
        tree = 0
        for x in range(SIZE):
            for y in range(SIZE):
                if self.trees[x][y] > TREE_LEVEL:
                    tree += 1
        return tree

    def min_dist(self, arr, x, y):
        if len(arr) == 0:
            return SIZE
        return min([sqrt((p[0] - x)**2 + (p[1] - y)**2) for p in arr])

    def size(self):
        return SIZE

    def water_level(self):
        return WATER_LEVEL

    def tree_level(self):
        return TREE_LEVEL

    def top_level(self):
        return TOP_LEVEL


def red(v):
    return v * ((REDUCTION_RATE - 1) / REDUCTION_RATE + random.random() / REDUCTION_RATE)


def generate_bias(minimum):
    bias = [1, 1, 1, 1]
    bias[random.randint(0, 3)] = random.uniform(minimum, 1)
    if random.random() < 0.5:
        bias[random.randint(0, 3)] = random.uniform(minimum, 1)
    return bias


def upwards(x, y, target, level):
    while target[x][y] < level:
        target[x][y] = 0
        if 0 < x < SIZE - 1 and 0 < y < SIZE - 1:
            v, x, y = max([(target[x - 1][y], x - 1, y), (target[x + 1][y], x + 1, y), (target[x][y - 1], x, y - 1),
                           (target[x][y + 1], x, y + 1)])
        else:
            break


def generate(sx, sy, target, stop, bias):
    queue = set()
    queue.add((sx, sy, TOP_LEVEL))
    while len(queue) > 0:
        (x, y, l) = queue.pop()
        if not target[x][y] == 0:
            continue
        target[x][y] = red(l)
        if l > stop:
            if x > 0:
                queue.add((x - 1, y, target[x][y] * bias[0]))
            if x < SIZE - 1:
                queue.add((x + 1, y, target[x][y] * bias[1]))
            if y > 0:
                queue.add((x, y - 1, target[x][y] * bias[2]))
            if y < SIZE - 1:
                queue.add((x, y + 1, target[x][y] * bias[3]))
