from player import Player


class Game:
    def __init__(self, terrain):
        self.map = terrain
        self.players = []
        for player in terrain.players:
            self.players.append(Player("a", player[0], player[1]))

    def step(self):
        for player in self.players:
            vision = self.map.get_vision(player.x, player.y)
            direction = player.move(vision)
            if self.map.is_valid_move(player.x, player.y, direction):
                player.update_position(direction)
