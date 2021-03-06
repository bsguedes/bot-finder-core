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
        self.size_x = config.SIZE_X
        self.size_y = config.SIZE_Y
        self.board = [[0] * self.size_y for _ in range(self.size_x)]
        self.trees = [[0] * self.size_y for _ in range(self.size_x)]
        self.players = []
        self.landmarks = []
        self.top_level = config.TOP_LEVEL
        self.tree_level = config.TREE_LEVEL
        self.water_level = config.WATER_LEVEL
        self.vision_radius = config.VISION_RADIUS
        self.island_top_level = config.ISLAND_TOP_LEVEL
        self.island_lower_level = config.ISLAND_LOWER_LEVEL

    def add_land(self):
        start = time.time()
        print('Let there be land')
        generate(int(self.size_x / 2), int(self.size_y / 2), self.board, 0, smart_bias(self.size_x, self.size_y),
                 stretch=True)
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
                    or min_dist(self.players, x, y) < min(self.size_x, self.size_y) / 5:
                x, y = self.find_elevation_point(self.water_level * 2)
            print("Let there be player ", i + 1, self.board[x][y])
            self.players.append((x, y))

    def is_valid_move(self, x, y, direction):
        if direction == -1:
            return True
        x += config.DIRS[direction][0]
        y += config.DIRS[direction][1]
        return not self.trees[x][y] and not (x, y) in self.landmarks and self.board[x][y] > self.water_level

    def get_vision(self, x, y, players, pid):
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
                    if i == self.vision_radius and j == self.vision_radius:
                        vision[i][j] = 1000 + pid
                    elif (x1 + i, y1 + j) in self.landmarks:
                        landmarks.append(self.landmarks.index((x1 + i, y1 + j)))
                        vision[i][j] = self.top_level + self.landmarks.index((x1 + i, y1 + j))
                    elif v < self.water_level:
                        vision[i][j] = 1
                    elif t > self.tree_level:
                        vision[i][j] = 2
                    else:
                        is_player = False
                        for p in players:
                            if p.x == x1 + i and p.y == y1 + j:
                                is_player = True
                                vision[i][j] = p.player_id + 1000
                                break
                        if not is_player:
                            vision[i][j] = 0
        return vision, landmarks

    def find_water_point(self):
        while True:
            x = int(random.random() * self.size_x)
            y = int(random.random() * self.size_y)
            if self.island_top_level < self.board[x][y] < self.water_level:
                return x, y

    def find_elevation_point(self, level):
        while True:
            x = int(random.random() * self.size_x)
            y = int(random.random() * self.size_y)
            if self.board[x][y] > level:
                return x, y

    def land_mass(self):
        land = 0
        for x in range(self.size_x):
            for y in range(self.size_y):
                if self.board[x][y] > self.water_level:
                    land += 1
        return land

    def tree_area(self):
        tree = 0
        for x in range(self.size_x):
            for y in range(self.size_y):
                if self.trees[x][y] > self.water_level:
                    tree += 1
        return tree


def min_dist(arr, x, y):
    if len(arr) == 0:
        return min(config.SIZE_X, config.SIZE_Y)
    return min([sqrt((p[0] - x)**2 + (p[1] - y)**2) for p in arr])


def descend(v, p):
    factor = v - v * ((config.REDUCTION_RATE - 1) / config.REDUCTION_RATE + random.random() / config.REDUCTION_RATE)
    factor = factor * p
    return v - factor


def generate_bias(minimum):
    bias = [1, 1, 1, 1]
    bias[random.randint(0, 3)] = random.uniform(minimum, 1)
    if random.random() < 0.5:
        bias[random.randint(0, 3)] = random.uniform(minimum, 1)
    return bias


def smart_bias(sx, sy):
    v = 0.98 + 0.02 * min(sx, sy) / max(sx, sy)
    bias = [1, 1, 1, 1]
    if sx > sy:
        bias = [1, 1, v, v]
    elif sy > sx:
        bias = [v, v, 1, 1]
    return bias


def upwards(x, y, target, level):
    while target[x][y] < level:
        target[x][y] = 0
        if 0 < x < config.SIZE_X - 1 and 0 < y < config.SIZE_Y - 1:
            v, x, y = max([(target[x - 1][y], x - 1, y), (target[x + 1][y], x + 1, y), (target[x][y - 1], x, y - 1),
                           (target[x][y + 1], x, y + 1)])
        else:
            break


def generate(sx, sy, target, stop, bias, stretch=False):
    queue = set()
    queue.add((sx, sy, config.TOP_LEVEL))
    while len(queue) > 0:
        (x, y, l) = queue.pop()
        if not target[x][y] == 0:
            continue
        target[x][y] = descend(l, phi(x, y, config.SIZE_X, config.SIZE_Y) if stretch else 1)
        if l > stop:
            if x > 0:
                d = target[x][y] * bias[0]
                queue.add((x - 1, y, d))
            if x < config.SIZE_X - 1:
                d = target[x][y] * bias[1]
                queue.add((x + 1, y, d))
            if y > 0:
                d = target[x][y] * bias[2]
                queue.add((x, y - 1, d))
            if y < config.SIZE_Y - 1:
                d = target[x][y] * bias[3]
                queue.add((x, y + 1, d))


def phi(x, y, sx, sy):
    f = 0.35
    x = x if x < sx / 2 else sx - x
    y = y if y < sy / 2 else sy - y
    return f if abs(x - y) < min(sx, sy) / 100 else 1
