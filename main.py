from map import Map
from mapview import MapView

m = Map()
m.add_land()
m.add_trees()
m.add_rivers()
m.add_landmarks()
m.add_players(4)
v = MapView(m)
v.save()
