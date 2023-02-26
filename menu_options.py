from tkinter import *
from tkinter.simpledialog import *
from tkinter.messagebox import *
from check_list import CheckList

class MenuOptions(Menu):
    def __init__(self, check_list: CheckList):
        self.check_list = check_list
        self.item_id = ""
        
        Menu.__init__(self, check_list, tearoff=False)
        self.add_command(label="Add", command=self.create_node)
        self.add_command(label="Edit", command=self.rename_node)
        self.add_separator()
        self.add_command(label="Remove", command=self.delete_node)
        
        self.check_list.bind("<Button-3>", self.popup)

    def popup(self, event):
        self.item_id = self.check_list.identify("item", event.x, event.y)
        
        try:
            self.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.grab_release()

    def create_node(self):
        name = askstring("Add Value", "Name of new value")

        if name:
            self.check_list.add_item(self.item_id, name)

    def rename_node(self):
        name = askstring("Edit Value", "Name of new value")

        if name:
            self.check_list.set_item_text(self.item_id, name)

    def delete_node(self):
        if askyesno("Delete", "Are you sure you want to delete this tree?"):
            self.check_list.delete(self.item_id)
            self.event_generate("<<Deleted>>")
