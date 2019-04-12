from player import Player
from thread import ThreadWithReturnValue


class Game:
    def __init__(self, terrain):
        self.map = terrain
        self.players = []
        self.score = 0
        self.turns = 0
        self.target = (2 * self.map.vision_radius + 1) ** 2
        self.landmarks = [False for _ in terrain.landmarks]
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
        return self.score <= self.target


def threaded_function(player, vision):
    return player.move(vision)
