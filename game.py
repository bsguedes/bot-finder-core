from player import Player


class Game:
    def __init__(self, terrain):
        self.map = terrain
        self.players = []
        self.score = 0
        self.turns = 0
        self.target = (2 * self.map.vision_radius + 1) ** 2
        i = 0
        for player in terrain.players:
            i += 1
            self.players.append(Player("player %s" % i, player[0], player[1]))

    def step(self):
        self.turns += 1
        for player in self.players:
            vision = self.map.get_vision(player.x, player.y)
            direction = player.move(vision)
            if self.map.is_valid_move(player.x, player.y, direction):
                player.update_position(direction)

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
