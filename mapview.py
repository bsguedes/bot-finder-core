from PIL import Image

class MapView():
    def __init__(self, map):
        self.map = map

    def save(self):
        image = Image.new("RGB", (self.map.size(),self.map.size()))
        for x in range(0, self.map.size()):
            for y in range(0, self.map.size()):
                image.putpixel((x,y), self.color(self.map.board[x][y]).GetTuple());
        image.save("Generated.png");
        image.show();        

    def color(self, v):
        c = Color()
        if v < self.map.water_level():            
            c.SetColor(0,0,255)
        else:
            c.SetColor(0,255,0)
        return c

class Color:
    r = 0.0;
    g = 0.0;
    b = 0.0;
    a = 1.0;

    def __init__(self, r = 0.0, g = 0.0, b = 0.0):
        self.r = r;
        self.g = g;
        self.b = b;
        self.a = 1;
    def GetTuple(self):
        return (int(self.r),int(self.g),int(self.b));
    def SetColor(self, r, g, b):
        self.r = r;
        self.g = g;
        self.b = b;
