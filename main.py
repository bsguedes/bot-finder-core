from map import Map
from game import Game
from mapcanvas import MapCanvas

m = Map()
m.add_land()
m.add_trees()
m.add_rivers()
m.add_landmarks()
m.add_players(4)
g = Game(m)
v = MapCanvas(m)
g.play(v.canvas_update)
v.won()
