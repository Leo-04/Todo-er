from tkinter import ttk
from tkinter.messagebox import *

class DragAndDrop(ttk.Label):
    def __init__(self, tree):
        ttk.Label.__init__(self, tree, text="...")
        tree.bind("<ButtonPress-1>", self.on_down, add="+")
        tree.bind("<ButtonRelease-1>", self.on_up, add="+")
        tree.bind("<B1-Motion>", self.on_drag, add="+")
        self.tree = tree

    def on_down(self, event):
        self.item_id = self.tree.identify("item", event.x, event.y)
        self["text"] = self.tree.item(self.item_id, "text")
    
    def on_up(self, event):
        new_item = self.tree.identify("item", event.x, event.y)

        if new_item != self.item_id:
            try:
                self.tree.move(self.item_id, new_item, 0 if new_item else "end")
            except:
                showerror("Error", "Invalid movement")
            self.tree.flip(None)
            

        self.place_forget()
    
    def on_drag(self, event):
        self.place(x=event.x - self.winfo_width() // 2, y=event.y - self.winfo_height() // 2)
