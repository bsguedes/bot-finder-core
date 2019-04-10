from map import Map
from mapview import MapView
from game import Game

m = Map()
m.add_land()
m.add_trees()
m.add_rivers()
m.add_landmarks()
m.add_players(4)
g = Game(m)
v = MapView(m, g.players)
for i in range(10):
    g.step()
    v.save()
