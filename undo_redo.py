from check_list import CheckList

class UndoRedo:
    def __init__(self, check_list: CheckList):
        self.buffer = []
        self.update = True
        self.buffer_pos = -1
        self.check_list = check_list

        self.check_list.bind("<<Inserted>>", self.on_change)
        self.check_list.bind("<<Deleted>>", self.on_change)

        self.check_list.bind_all("<Control-z>", self.undo)
        self.check_list.bind_all("<Control-Shift-Z>", self.redo)
        self.check_list.bind_all("<Control-y>", self.redo)

    def on_change(self, event=None):
        if self.update:
            self.buffer = self.buffer[0: self.buffer_pos + 1]
            self.buffer_pos = len(self.buffer)
            
            items = self.check_list.get_items()
            if len(self.buffer) == 0 or items != self.buffer[-1]:
                self.buffer.append(items)

    def undo(self, event=None):
        if len(self.buffer) and self.buffer_pos > 0:
            self.buffer_pos -= 1

            self.update = False
            self.check_list.delete(*self.check_list.get_children())
            self.check_list.add_items("", self.buffer[self.buffer_pos])
            self.update = True

    def redo(self, event=None):
        if len(self.buffer) and self.buffer_pos < len(self.buffer) - 1:
            self.buffer_pos += 1
            
            self.update = False
            self.check_list.delete(*self.check_list.get_children())
            self.check_list.add_items("", self.buffer[self.buffer_pos])
            self.update = True
