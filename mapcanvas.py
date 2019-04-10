from tkinter import *

class MapCanvas:
    def __init__(self, map):
        master = Tk()
        self.map = map
        self.canvas = Canvas(master, width=map.size(), height=map.size())
        self.canvas.pack()
