from lib import dictGenerator as dg
from tkinter import *
from tkinter.scrolledtext import ScrolledText

class TextObject:
    def __init__(self,parent,name):
        self.parent = parent
        self.name = name
        self.text = StringVar(name=name)
        self.text.set("")
        self.text.trace('w',self.stringCallback)
        self.splits = []
        self.wordCount = IntVar(name=name+"WordCount")

        self.window = Toplevel(self.parent.master)
        self.window.title(self.name)
        self.frame =  Frame(self.window)
        self.textBox = ScrolledText(self.frame,width=60,height=20,wrap=WORD)
        self.frame.grid(row=0,column=0,sticky='news')
        self.textBox.grid(column=0,row=0,sticky='news')
        self.window.withdraw()
        self.window.protocol("WM_DELETE_WINDOW", self.window.withdraw)


    def stringCallback(self,name,*args):
        if name!="dicttext":
            if name == "knottext" or name == "plaintext" or name =="keytext":
                display = getattr(self.parent,name+"Display")
                display.config(state=NORMAL)
                display.delete(1.0,END)
                display.insert(END,self.text.get())
                display.config(state=DISABLED)
            if name == "plaintext" or name == "keytext":
                self.splits = dg.splitToWords(self.text.get())
                self.wordCount.set(len(self.splits))
            else:
                # TODO: implement automatic dicttext splitting
                x=0

    def clear(self):
        self.text.set("")

    def show(self):
        self.textBox.config(state=NORMAL)
        self.textBox.delete(1.0,END)
        self.textBox.insert(END,self.text.get())
        self.textBox.config(state=DISABLED)
        self.window.deiconify()
