from tkinter import Tk, Canvas, PhotoImage


class MapCanvas:
    def __init__(self, terrain):
        self.map = terrain
        self.window = Tk()        
        self.player_objects = []
        self.canvas = Canvas(self.window, width=terrain.size(), height=terrain.size(), bg="#000000")
        self.canvas.pack()
        self.img = PhotoImage(width=terrain.size(), height=terrain.size())
        self.canvas.create_image((terrain.size()/2, terrain.size()/2), image=self.img, state="normal")
        self.draw_start()       
 
    def draw_start(self):        
        for x in range(0, self.map.size()):
            for y in range(0, self.map.size()):
                self.img.put(self.color(x, y), (x, y))
        for (x, y) in self.map.landmarks:
            self.create_circle(x, y, 1, fill="#ff0000")
       
    def show(self, players):
        for item in self.player_objects:
            self.canvas.delete(item)
        self.player_objects.clear()
        for player in players:
            self.player_objects.append(self.create_circle(player.x, player.y, 2))
        self.window.update_idletasks()
        self.window.update()

    def create_circle(self, x, y, r, fill="#000000"):
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return self.canvas.create_oval(x0, y0, x1, y1, fill=fill)

    def color(self, x, y):
        v, t = self.map.board[x][y], self.map.trees[x][y]
        if v < self.map.water_level():
            return "#0000ff"
        elif t > self.map.tree_level():
            return "#408000"
        else:
            return "#00ff00"
