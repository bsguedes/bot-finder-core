from map import Map
from mapview import MapView

m = Map()
m.generate()
v = MapView(m)
v.save()
