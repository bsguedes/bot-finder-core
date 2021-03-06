from tkinter import Tk, Canvas, PhotoImage, W, mainloop
import config


class MapCanvas:
    def __init__(self, terrain):
        self.map = terrain
        self.window = Tk()        
        self.objects = []
        self.player_objects = {}
        self.canvas = Canvas(self.window, width=terrain.size_x * config.ZOOM, height=terrain.size_y * config.ZOOM,
                             bg="#000000")
        self.canvas.pack()
        self.img = PhotoImage(width=terrain.size_x * config.ZOOM, height=terrain.size_y * config.ZOOM)
        self.canvas.create_image((terrain.size_x * config.ZOOM / 2, terrain.size_y * config.ZOOM / 2), image=self.img,
                                 state="normal")
        self.draw_start()                 
 
    def draw_start(self):
        z = config.ZOOM
        for x in range(0, self.map.size_x):
            for y in range(0, self.map.size_y):
                for i in range(z):
                    for j in range(z):
                        self.img.put(self.color(x, y, fog=True), (z * x + i, z * y + j))
        for (x, y) in self.map.landmarks:
            self.canvas.create_rectangle(z * x, z * y, z * (x + 1), z * (y + 1), outline="#ff0000", fill="#ff0000")

    def canvas_update(self, game, player):
        z = config.ZOOM
        score = game.score
        target = game.target
        landmarks = len([x for x in game.landmarks if x])

        # cleaning
        if player.name not in self.player_objects:
            self.player_objects[player.name] = []
        for item in self.objects:
            self.canvas.delete(item)
        for item in self.player_objects[player.name]:
            self.canvas.delete(item)
        self.objects.clear()
        self.player_objects[player.name].clear()

        # player icon and label
        self.player_objects[player.name].append(self.create_circle(z * player.x - z / 2, z * player.y - z / 2, (z + 1)))
        if score > 5000:
            self.create_label_with_rectangle(z*player.x, z*player.y, 80, player.name, self.player_objects[player.name])
        if config.SHOW_SCORES:
            self.create_label_with_rectangle(0, z*self.map.size_y - 25 * (player.player_id + 2), 170,
                                             '%s: %s moves' % (player.name, player.steps),
                                             self.player_objects[player.name])

        # player vision
        for x in range(0, self.map.vision_radius * 2 + 1):
            for y in range(0, self.map.vision_radius * 2 + 1):
                a, b = player.x - self.map.vision_radius + x, player.y - self.map.vision_radius + y
                for i in range(z):
                    for j in range(z):
                        if player.vision[x][y] != -1:
                            self.img.put(self.color(a, b, fog=False), (z * a + i, z * b + j))

        # items
        self.create_label_with_rectangle(0, 0, 130, 'Score: %i' % score, self.objects)
        self.create_label_with_rectangle(0, z * self.map.size_y - 25, 130, 'Best: %i' % game.minimum_score,
                                         self.objects)
        self.create_label_with_rectangle(z * self.map.size_x - 135, 0, 130, 'Target: %i' % target, self.objects)
        self.create_label_with_rectangle(z * self.map.size_x - 135, z * self.map.size_y - 25, 130,
                                         'Landmarks: %i' % landmarks,
                                         self.objects)

        self.window.update_idletasks()
        self.window.update()

    def create_circle(self, x, y, r, fill="#f9d71c"):
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return self.canvas.create_oval(x0, y0, x1, y1, fill=fill)

    def create_label_with_rectangle(self, x, y, w, name, collection):
        a = self.canvas.create_rectangle(x + 5, y + 5, x + w, y + 25, fill="white")
        b = self.canvas.create_text(x+8, y+14, text=name, anchor=W)
        collection.append(a)
        collection.append(b)

    def won(self):
        z = config.ZOOM
        self.create_label_with_rectangle(z * self.map.size_x / 2 - 65, z * self.map.size_y / 2 - 15, 130, '   YOU WIN!',
                                         self.objects)
        mainloop()

    def color(self, x, y, fog=False):
        v, t = self.map.board[x][y], self.map.trees[x][y]
        if v < self.map.water_level:
            return "#0000ff" if not fog else "#00004f"
        elif t > self.map.tree_level:
            return "#408000" if not fog else "#102000"
        else:
            return "#00cf00" if not fog else "#004f00"
