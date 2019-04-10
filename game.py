from player import Player

class Game:
    def __init__(self, map):
        self.map = map
        self.players = []
        for player in map.players:
            self.players.append(Player("a", player[0], player[1]))

    def step(self):
        for player in self.players:
            vision = self.map.get_vision(player.x, player.y)
            direction = player.move(vision)            
            player.update_position(direction)
