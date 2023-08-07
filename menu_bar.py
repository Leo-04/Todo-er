from tkinter import ttk
from tkinter import *

class MenuBar(ttk.Frame):
    def __init__(self, master: ttk.Widget = None, side: str = LEFT):
        ttk.Frame.__init__(self, master, relief="raised")
        self.side = side

    def add(self, text: str, command: callable, hotkey: str | None = None, padx: tuple[int, int] = 10, pady: tuple[int, int] = 5):
        button = ttk.Label(self, text = text, relief="raised")
        button.bind("<Button-1>", lambda e: command())
        button.pack(side=self.side, padx=padx, pady=pady)
        
        if hotkey is not None:
            self.winfo_toplevel().bind_all(hotkey, lambda e: command())

    def add_sep(self, padx=20, pady=5):
        ttk.Label(self, text="  ").pack(side=self.side, padx=padx, pady=pady)
