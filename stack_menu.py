import tkinter
from tkinter import ttk
class StackMenuWidget :

    def __init__ (self, root) :
        self.root = root

        frame = ttk.Frame(self.root)
        frame.pack(expand=1, fill=tkinter.BOTH)
        self.stack = [frame]

    def push (self) :
        self.stack[-1].pack_forget()
        frame = ttk.Frame(self.root)
        frame.pack(expand=1, fill=tkinter.BOTH)
        self.stack.append(frame)

    def get (self) :
        return self.stack[-1]

    def pop (self) :
        self.stack[-1].pack_forget()
        self.stack.pop(-1)
        self.stack[-1].pack(expand=1, fill=tkinter.BOTH)
