from map import Map
from game import Game
from mapcanvas import MapCanvas
import time

m = Map()
m.add_land()
m.add_trees()
m.add_rivers()
m.add_landmarks()
m.add_players(4)
g = Game(m)
v = MapCanvas(m)
while True:
    g.step()
    time.sleep(0.1)
    v.show(g.players)
