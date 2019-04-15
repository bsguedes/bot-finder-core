from player import Player
from thread import ThreadWithReturnValue
from threading import Lock, Thread


class Game:
    def __init__(self, terrain, updater):
        self.map = terrain
        self.players = []
        self.score = 0
        self.minimum_score = terrain.size ** 3
        self.turns = 0
        self.target = (2 * self.map.vision_radius + 1) ** 2
        self.landmarks = [False for _ in terrain.landmarks]
        self.updater = updater
        i = 0
        for player in terrain.players:
            i += 1
            self.players.append(Player("player %s" % i, player[0], player[1]))

    def step(self):
        self.turns += 1
        threads = []
        for player in self.players:
            vision, landmarks = self.map.get_vision(player.x, player.y)
            for landmark in landmarks:
                self.landmarks[landmark] = True
            threads.append(ThreadWithReturnValue(target=threaded_function, args=(player, vision)))

        for thread in threads:
            thread.start()

        results = [0 for _ in range(len(self.players))]
        for index, thread in enumerate(threads):
            results[index] = thread.join()

        i = 0
        for player in self.players:
            if self.map.is_valid_move(player.x, player.y, results[i]):
                player.update_position(results[i])
                i += 1

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

    def step(self, player):
        map_lock.acquire()
        vision, landmarks = self.map.get_vision(player.x, player.y)
        for landmark in landmarks:
            self.landmarks[landmark] = True
        map_lock.release()
        thread = Thread(target=threaded_function, args=(player, vision, self.updater, self))
        thread.start()

    def play(self):


        while not g.finished():
            g.step()
            time.sleep(0.02)
            v.show(g)


map_lock = Lock()
done_lock = Lock()


def threaded_function(player, vision, canvas_callback, game):
    direction = player.move(vision)
    if game.map.is_valid_move(player.x, player.y, direction):
        player.update_position(direction)
    map_lock.acquire()
    canvas_callback()
    if not game.finished():
        map_lock.release()
        thread = Thread(target=threaded_function, args=(player, vision, canvas_callback, game))
        thread.start()
    else:
        done_lock.acquire()
        map_lock.release()


