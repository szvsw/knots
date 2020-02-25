from lib import dictGenerator as dg
from tkinter import *

class TextObject:
    def __init__(self,parent,name):
        self.parent = parent
        self.name = name
        self.text = StringVar(name=name)
        self.text.set("")
        self.text.trace('w',self.stringCallback)
        self.splits = []
        self.wordCount = IntVar(name=name+"WordCount")
        self.counter = 0

    def stringCallback(self,name,*args):
        # TODO: Give different behaviors for dict vs normal strings
        if name!="dicttext":
            display = getattr(self.parent,name+"Display")
            # textObject = getattr(self.parent,name)
            display.config(state=NORMAL)
            display.delete(1.0,END)
            display.insert(END,self.text.get())
            display.config(state=DISABLED)
            if name == "plaintext" or name == "keytext":
                self.splits = dg.splitToWords(self.text.get())
                self.wordCount.set(len(self.splits))

    def clear(self):
        self.text.set("")

    # TODO: Give each a listbox & popup window which can be viewed with a single click.
