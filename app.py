import math
from tkinter import *
from tkinter.font import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.simpledialog import *
from tkinter import ttk

from check_list import CheckList
from menu_bar import MenuBar
from menu_options import MenuOptions
from undo_redo import UndoRedo

import file

class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Todo-er")
        try:
            self.iconbitmap("./icon.ico")
        except:
            self.withdraw()
            showerror("Error", "Error: Icon file not found")
            self.deiconify()
            self.update()
        
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.font = Font(self)
        self.check_list = CheckList(self, height=10)
        self.menu_bar = MenuBar(self)
        self.options = MenuOptions(self.check_list)
        self.undo_redo = UndoRedo(self.check_list)
        
        scroll_bar = ttk.Scrollbar(self)
        scroll_bar.configure(command=self.check_list.yview)
        self.check_list.configure(yscrollcommand=scroll_bar.set)

        self.menu_bar.add("New", self.new, "<Control-n>")
        self.menu_bar.add("Save", self.save, "<Control-s>")
        self.menu_bar.add("Open", self.open, "<Control-o>")
        self.menu_bar.add_sep()
        self.menu_bar.add("Add", self.add_value, "<Control-t>")
        self.menu_bar.add_sep()
        self.menu_bar.add("Dark Mode", lambda: self.set_colors("#DDDDDD", "#333333"), "<Control-d>")
        self.menu_bar.add("Light Mode", lambda: self.set_colors("#000000", "#EEEEEE"), "<Control-l>")
        self.menu_bar.add_sep()
        self.menu_bar.add("Reset Zoom", lambda: self.set_font_size(20), "<Control-0>")

        self.menu_bar.pack(side=TOP, fill=X)
        scroll_bar.pack(side=RIGHT, fill=Y)
        self.check_list.pack(fill=BOTH, expand=1)

        self.bind("<Control-MouseWheel>", self.zoom)

        self.set_colors("#DDDDDD", "#333333")
        self.set_font_size(20)
        
        self.filename = None
    
    def zoom(self, event):
        delta_size = int(math.copysign(1, event.delta))

        size = self.font.cget("size")

        if 5 < size + delta_size < 100:
            self.set_font_size(size + delta_size)

    def add_value(self):
        self.options.item_id = ""
        self.options.create_node()
    
    def new(self):
        if not askokcancel("Todo-er", "Any unsaved work will be lost"):
            return

        self.title("Todo-er")
        
        self.undo_redo.buffer = []
        self.undo_redo.buffer_pos = 0
        self.filename = None

        self.undo_redo.update = False
        self.check_list.delete(*self.check_list.get_children())
        self.check_list.add_items("", [])
        self.undo_redo.update = True
        
    def save(self):
        out_string = file.data_to_string(self.check_list.get_items())
        if not self.filename:
            self.filename = asksaveasfilename()

        if self.filename:
            self.title("Todo-er - " + self.filename)
            
            open(self.filename, "w").write(out_string)

    def open(self):
        if not askokcancel("Todo-er", "Any unsaved work will be lost"):
            return
            
        self.filename = askopenfilename()

        if self.filename:
            self.title("Todo-er - " + self.filename)
            
            data = file.string_to_data(open(self.filename, "r").read())

            self.undo_redo.buffer = []
            self.undo_redo.buffer_pos = 0
            
            self.undo_redo.update = False
            self.check_list.delete(*self.check_list.get_children())
            self.check_list.add_items("", data)
            self.undo_redo.update = True
            self.undo_redo.on_change()

    
    def set_colors(self, fg, bg):
        self["bg"] = bg
        self.option_add("*Background", bg)
        self.option_add("*Foreground", fg)
        
        self.style.configure("TFrame", background=bg)
        self.style.configure("Treeview", background=bg, foreground=fg, fieldbackground=bg)
        self.style.configure("TLabel", background=bg, foreground=fg)

    def set_font_size(self, size):
        self.font.config(size=size)
        
        self.style.configure("TLabel", font=self.font)
        self.style.configure("Treeview", font=self.font, rowheight=self.font.metrics('linespace'))
