from map import Map
from mapview import MapView

m = Map()
m.add_land()
m.add_trees()
m.add_rivers()
v = MapView(m)
v.save()
