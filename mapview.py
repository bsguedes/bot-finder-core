from PIL import Image


class MapView:
    def __init__(self, map):
        self.map = map

    def save(self):
        image = Image.new("RGB", (self.map.size(), self.map.size()))
        for x in range(0, self.map.size()):
            for y in range(0, self.map.size()):
                image.putpixel((x, y), self.color(x, y).get_tuple())
        image.save("Generated.png")
        image.show()

    def color(self, x, y):
        v, t = self.map.board[x][y], self.map.trees[x][y]
        if v >= self.map.top_level():
            return Color(255, 0, 0)
        if v < self.map.water_level():
            return Color(0, 0, 255)
        elif t > self.map.tree_level():
            return Color(64, 128, 0)
        else:
            return Color(0, 255, 0)


class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def get_tuple(self):
        return int(self.r), int(self.g), int(self.b)

