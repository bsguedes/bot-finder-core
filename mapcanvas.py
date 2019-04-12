from tkinter import Tk, Canvas, PhotoImage


class MapCanvas:
    def __init__(self, terrain):
        self.map = terrain
        self.window = Tk()        
        self.player_objects = []
        self.canvas = Canvas(self.window, width=terrain.size, height=terrain.size, bg="#000000")
        self.canvas.pack()
        self.img = PhotoImage(width=terrain.size, height=terrain.size)
        self.canvas.create_image((terrain.size/2, terrain.size/2), image=self.img, state="normal")
        self.draw_start()                 
 
    def draw_start(self):        
        for x in range(0, self.map.size):
            for y in range(0, self.map.size):
                self.img.put(self.color(x, y, fog=True), (x, y))
        for (x, y) in self.map.landmarks:
            self.canvas.create_rectangle(x, y, x+1, y+1, outline="#ff0000")
       
    def show(self, players):
        for item in self.player_objects:
            self.canvas.delete(item)
        self.player_objects.clear()
        for player in players:
            self.player_objects.append(self.create_circle(player.x, player.y, 2))
            for x in range(0, self.map.vision_radius * 2 + 1):
                for y in range(0, self.map.vision_radius * 2 + 1):
                    a, b = player.x - self.map.vision_radius + x, player.y - self.map.vision_radius + y
                    if player.vision[x][y] != -1:
                        self.img.put(self.color(a, b, fog=False), (a, b))
        self.window.update_idletasks()
        self.window.update()

    def create_circle(self, x, y, r, fill="#f9d71c"):
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return self.canvas.create_oval(x0, y0, x1, y1, fill=fill)

    def color(self, x, y, fog=False):
        v, t = self.map.board[x][y], self.map.trees[x][y]
        if v < self.map.water_level:
            return "#0000ff" if not fog else "#00004f"
        elif t > self.map.tree_level:
            return "#408000" if not fog else "#102000"
        else:
            return "#00cf00" if not fog else "#004f00"
