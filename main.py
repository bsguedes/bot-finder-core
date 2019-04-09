from map import Map
from mapview import MapView

m = Map()
m.add_land()
m.add_trees()
v = MapView(m)
v.save()
