from tkinter import ttk
from tkinter import *

class CheckList(ttk.Treeview):
    def __init__(self, master: ttk.Widget = None, off: str = chr(9744), on: str = chr(9745), **kwargs):
        ttk.Treeview.__init__(self, master, **kwargs, selectmode=NONE, show="tree")
        self.column("#0", stretch=True)
        
        self.on_text = on
        self.off_text = off

        self.bind("<<TreeviewOpen>>", self.flip)
        self.bind("<<TreeviewClose>>", self.flip)
        self.bind("<Button-1>", self.on_click)
        self.bind("<Double-Button-1>", lambda e: (self.on_click(e), "break")[1])

    def flip(self, event):
        item_id =  self.focus()
        if item_id:
            text = (self.off_text if self.is_on(item_id) else self.on_text) + self.item(item_id, "text")[1:]
                
            self.item(item_id, text=text)

    def on_click(self, event):
        item_id = self.identify("item", event.x, event.y)
        if item_id:
            text = (self.off_text if self.is_on(item_id) else self.on_text) + self.item(item_id, "text")[1:]
                
            self.item(item_id, text=text)
        

    def is_on(self, iid: str):
        return self.item(iid, "text")[0] == self.on_text
    
    def add_items(self, parent: str, items: list[bool, str, list[...], ...]):
        for i in range(0, len(items), 3):
            done = items[i]
            name = items[i + 1]
            values = items[i + 2]

            node = self.add_item(parent, name, done)
            
            self.add_items(node, values)

    def add_item(self, parent: str, text: str, value: bool = False):
        id = self.insert(parent, index="end", text=(self.on_text if value else self.off_text)+" "+text, open=True)
        
        self.event_generate("<<Inserted>>")
        return id

    def get_items(self, parent: str = ""):
        items = []
        children = self.get_children(parent)
        
        for item_id in children:
            items.append(self.is_on(item_id))
            items.append(self.item(item_id, "text")[2:])
            items.append(self.get_items(item_id))
        
        return items

    def set_item_text(self, item_id: str, text: str):
        self.item(item_id, text=self.item(item_id, "text")[0:2] + text)
