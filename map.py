import random
import time

SIZE = 900
TOP_LEVEL = 100
WATER_LEVEL = 5
TREE_LEVEL = 30
REDUCTION_RATE = 90
TREE_PERCENTAGE = 15
RIVERS = 10
RIVER_LEVEL = 20
LANDMARKS = 100


class Map:
    def __init__(self):
        self.board = [[0] * SIZE for _ in range(SIZE)]
        self.trees = [[0] * SIZE for _ in range(SIZE)]

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
            upwards(x, y, self.board, RIVER_LEVEL)
            print("And there were rivers... after %.2f seconds." % (time.time() - start))

    def add_landmarks(self):
        start = time.time()
        print('Let there be trees')
        for i in range(LANDMARKS):
            x, y = self.find_elevation_point(WATER_LEVEL)
            if self.trees[x][y] == 0:
                self.board[x][y] = TOP_LEVEL + i
                self.board[x+1][y] = TOP_LEVEL + i
                self.board[x][y+1] = TOP_LEVEL + i
                self.board[x+1][y+1] = TOP_LEVEL + i
        print("And there were landmarks... after %.2f seconds." % (time.time() - start))

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
