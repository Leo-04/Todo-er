from tkinter import ttk
from tkinter import *

class MenuBar(ttk.Frame):
    def __init__(self, master: ttk.Widget = None, side: str = LEFT, padx: tuple[int, int] = 10, pady: tuple[int, int] = 5):
        ttk.Frame.__init__(self, master, relief="raised")
        self.side = side
        self.padx = padx
        self.pady = pady

    def add(self, text: str, command: callable, hotkey: str | None = None):
        button = ttk.Label(self, text = text, relief="raised")
        button.bind("<Button-1>", lambda e: command())
        button.pack(side=self.side, padx=self.padx, pady=self.pady)
        
        if hotkey is not None:
            self.winfo_toplevel().bind_all(hotkey, lambda e: command())

    def add_sep(self, padx=10, pady=0):
        ttk.Label(self, text="  ").pack(side=self.side, padx=self.padx+padx, pady=self.pady+pady)
