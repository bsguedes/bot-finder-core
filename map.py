import random
import time
from math import sqrt
import config


class Map:
    def __init__(self):
        seed = config.SEED
        if seed is None:
            seed = random.randint(0, 65536)
        random.seed(seed)
        print('Using seed ', seed)
        self.size = config.SIZE
        self.board = [[0] * self.size for _ in range(self.size)]
        self.trees = [[0] * self.size for _ in range(self.size)]
        self.players = []
        self.landmarks = []
        self.top_level = config.TOP_LEVEL
        self.tree_level = config.TREE_LEVEL
        self.water_level = config.WATER_LEVEL
        self.vision_radius = config.VISION_RADIUS

    def add_land(self):
        start = time.time()
        print('Let there be land')
        generate(int(self.size / 2), int(self.size / 2), self.board, 0, generate_bias(0.999))
        print("And there was land... after %.2f seconds." % (time.time() - start))

    def add_trees(self):
        start = time.time()
        print('Let there be trees')
        land = self.land_mass()
        while self.tree_area() < land * config.TREE_PERCENTAGE / 100:
            x, y = self.find_elevation_point(self.water_level)
            generate(x, y, self.trees, random.randrange(self.tree_level, self.top_level), generate_bias(0.93))
            print("And there were trees... after %.2f seconds." % (time.time() - start), self.tree_area(), land)

    def add_rivers(self):
        start = time.time()
        print('Let there be rivers')
        for _ in range(config.RIVERS):
            x, y = self.find_water_point()
            upwards(x, y, self.board, random.randrange(config.RIVER_LEVEL, self.tree_level))
            print("And there were rivers... after %.2f seconds." % (time.time() - start))

    def add_landmarks(self):
        start = time.time()
        print('Let there be landmarks')
        for i in range(config.LANDMARKS):
            x, y = self.find_elevation_point(self.water_level)
            while self.trees[x][y] != 0 or min_dist(self.landmarks, x, y) < 2 * self.vision_radius:
                x, y = self.find_elevation_point(self.water_level)
            self.landmarks.append((x, y))
        print("And there were landmarks... after %.2f seconds." % (time.time() - start))

    def add_players(self, player_count):
        for i in range(player_count):
            x, y = self.find_elevation_point(self.water_level * 2)
            while self.trees[x][y] != 0 or self.board[x][y] > self.tree_level \
                    or min_dist(self.players, x, y) < self.size / 5:
                x, y = self.find_elevation_point(self.water_level * 2)
            print("Let there be player ", i + 1, self.board[x][y])
            self.players.append((x, y))

    def is_valid_move(self, x, y, direction):
        if direction == -1:
            return True
        x += config.DIRS[direction][0]
        y += config.DIRS[direction][1]
        return not self.trees[x][y] and not (x, y) in self.landmarks and self.board[x][y] > self.water_level

    def get_vision(self, x, y):
        d = (self.vision_radius * 2) + 1
        vision = [[-1] * d for y in range(d)]
        x1 = x - self.vision_radius
        y1 = y - self.vision_radius
        landmarks = []
        for i in range(d):
            for j in range(d):
                if (i - self.vision_radius)**2 + (j - self.vision_radius)**2 - self.vision_radius**2 <= 4:
                    v = self.board[x1+i][y1+j]
                    t = self.trees[x1+i][y1+j]
                    if (x1 + i, y1 + j) in self.landmarks:
                        landmarks.append(self.landmarks.index((x1 + i, y1 + j)))
                        vision[i][j] = self.top_level + self.landmarks.index((x1 + i, y1 + j))
                    elif v < self.water_level:
                        vision[i][j] = 1
                    elif t > self.tree_level:
                        vision[i][j] = 2
                    else:
                        vision[i][j] = 0
        return vision, landmarks

    def find_water_point(self):
        while True:
            x = int(random.random() * self.size)
            y = int(random.random() * self.size)
            if self.board[x][y] < self.water_level:
                return x, y

    def find_elevation_point(self, level):
        while True:
            x = int(random.random() * self.size)
            y = int(random.random() * self.size)
            if self.board[x][y] > level:
                return x, y

    def land_mass(self):
        land = 0
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] > self.water_level:
                    land += 1
        return land

    def tree_area(self):
        tree = 0
        for x in range(self.size):
            for y in range(self.size):
                if self.trees[x][y] > self.water_level:
                    tree += 1
        return tree


def min_dist(arr, x, y):
    if len(arr) == 0:
        return config.SIZE
    return min([sqrt((p[0] - x)**2 + (p[1] - y)**2) for p in arr])


def red(v):
    return v * ((config.REDUCTION_RATE - 1) / config.REDUCTION_RATE + random.random() / config.REDUCTION_RATE)


def generate_bias(minimum):
    bias = [1, 1, 1, 1]
    bias[random.randint(0, 3)] = random.uniform(minimum, 1)
    if random.random() < 0.5:
        bias[random.randint(0, 3)] = random.uniform(minimum, 1)
    return bias


def upwards(x, y, target, level):
    while target[x][y] < level:
        target[x][y] = 0
        if 0 < x < config.SIZE - 1 and 0 < y < config.SIZE - 1:
            v, x, y = max([(target[x - 1][y], x - 1, y), (target[x + 1][y], x + 1, y), (target[x][y - 1], x, y - 1),
                           (target[x][y + 1], x, y + 1)])
        else:
            break


def generate(sx, sy, target, stop, bias):
    queue = set()
    queue.add((sx, sy, config.TOP_LEVEL))
    while len(queue) > 0:
        (x, y, l) = queue.pop()
        if not target[x][y] == 0:
            continue
        target[x][y] = red(l)
        if l > stop:
            if x > 0:
                queue.add((x - 1, y, target[x][y] * bias[0]))
            if x < config.SIZE - 1:
                queue.add((x + 1, y, target[x][y] * bias[1]))
            if y > 0:
                queue.add((x, y - 1, target[x][y] * bias[2]))
            if y < config.SIZE - 1:
                queue.add((x, y + 1, target[x][y] * bias[3]))
