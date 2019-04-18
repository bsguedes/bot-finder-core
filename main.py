from map import Map
from game import Game
from mapcanvas import MapCanvas
import config


m = Map()
m.add_land()
m.add_trees()
m.add_rivers()
m.add_landmarks()
m.add_players(len(config.PLAYERS))
g = Game(m, config.PLAYERS)
v = MapCanvas(m)
g.play(v.canvas_update)
v.won()
