from player import Player
from threading import Lock, Thread
from queue import Queue
import time


class Game:
    def __init__(self, terrain, player_config):
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
        for coord, cfg in zip(terrain.players, player_config):
            i += 1
            ip = cfg[0]
            port = cfg[1]
            x = coord[0]
            y = coord[1]
            self.players.append(Player("player %s" % i, i, x, y, ip, port))

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
        self.turn_radio()
        for player in self.players:
            self.player_step(player)
        while not self.completed:
            callback, game, player = self.callback_queue.get()
            callback(game, player)

    def turn_radio(self):
        thread = Thread(target=play_radio, args=(self, self.players, 10))
        thread.start()


map_lock = Lock()


def play_radio(game, players, sleep_time):
    while not game.completed:
        get_threads = []
        for player in players:
            get_threads.append(ThreadWithReturnValue(target=get_radio_thread, args=(player, player.name)))
        for thread in get_threads:
            thread.start()
        results = {player.name: None for player in players}
        for index, thread in enumerate(get_threads):
            radio, name = thread.join()
            results[name] = radio
        send_threads = []
        for player in players:
            send_threads.append(Thread(target=send_radio_thread, args=(player, results)))
        for thread in send_threads:
            thread.start()
        for thread in send_threads:
            thread.join()
        time.sleep(sleep_time)


def get_radio_thread(player, name):
    return player.obtain_radio(), name


def send_radio_thread(player, radio_stream):
    player.post_radio(radio_stream)


def threaded_function(player, vision, canvas_callback, game):
    time.sleep(0.05)
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


class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, value=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self.player_name = value
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return
