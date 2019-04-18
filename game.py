from player import Player
from threading import Lock, Thread
from queue import Queue
import time


class Game:
    def __init__(self, terrain):
        self.map = terrain
        self.players = []
        self.score = 0
        self.minimum_score = terrain.size ** 3
        self.turns = 0
        self.target = (2 * self.map.vision_radius + 1) ** 2
        self.landmarks = [False for _ in terrain.landmarks]
        self.updater = None
        self.completed = False
        self.callback_queue = Queue()
        i = 0
        for player in terrain.players:
            i += 1
            self.players.append(Player("player %s" % i, i, player[0], player[1]))

    def finished(self):
        c = len(self.players)
        dists = []
        for i in range(c):
            for j in range(c):
                p1 = self.players[i]
                p2 = self.players[j]
                dists.append((p1.x - p2.x) ** 2 + (p1.y - p2.y)**2)
        self.score = max(dists)
        self.minimum_score = min(self.score, self.minimum_score)
        return self.score <= self.target

    def player_step(self, player):
        if not self.completed:
            map_lock.acquire()
            vision, landmarks = self.map.get_vision(player.x, player.y)
            for landmark in landmarks:
                self.landmarks[landmark] = True
            map_lock.release()
            thread = Thread(target=threaded_function, args=(player, vision, self.updater, self))
            thread.start()

    def play(self, cb):
        self.updater = cb
        for player in self.players:
            self.player_step(player)
        while not self.completed:
            callback, game, player = self.callback_queue.get()
            callback(game, player)


map_lock = Lock()


def threaded_function(player, vision, canvas_callback, game):
    time.sleep(0.02)
    direction = player.move(vision)
    if game.map.is_valid_move(player.x, player.y, direction):
        player.update_position(direction)
    map_lock.acquire()
    game.callback_queue.put((canvas_callback, game, player))
    if not game.finished():
        map_lock.release()
        game.player_step(player)
    else:
        game.completed = True
        map_lock.release()


