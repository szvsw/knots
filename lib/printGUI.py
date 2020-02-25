from tkinter import *
from tkinter import ttk


class PrintGUI:
    def __init__(self,parent):
        self.parent = parent
        self.window = Toplevel(parent.master)
        self.frame =  Frame(self.window)
        self.frame.grid(row=0,column=0,sticky='news')
        self.window.protocol("WM_DELETE_WINDOW", self.window.withdraw)
        self.window.title("Subwindow")
        self.window.columnconfigure(0,minsize=200,weight=1)

        self.orientationChoices = ["Rows", "Rows", "Columns"]
        self.orientation = StringVar(name = "orientation")
        self.orientation.set("Rows")

        self.delimiterChoices = ["None (Padded)", "None (Padded)", "[]", "{}", "()", "<>", "<space>", ".", ":", "|"]
        self.delimiter = StringVar(name="delimiter")
        self.delimiter.set("None (Padded)")

        self.paddingChoices = ["Padded", "Padded", "Unpadded"]
        self.padding = StringVar(name="padding")
        self.padding.set("Padded")

        self.blockSizeChoices = [i for i in range(1,30)]
        self.blockSizeChoices.insert(0,1)
        self.blockSize = IntVar(name="blockSize")
        self.blockSize.set(1)

        self.knotPrintStyleChoices = ["Pretty", "Pretty","Simple"]
        self.knotPrintStyle = StringVar(name = "knotPrintStyle")
        self.knotPrintStyle.set("Pretty")

        self.menus = {  'Orientation': ttk.OptionMenu(self.frame, self.orientation, *self.orientationChoices), \
                        'Delimiter': ttk.OptionMenu(self.frame, self.delimiter, *self.delimiterChoices), \
                        'Padding': ttk.OptionMenu(self.frame, self.padding, *self.paddingChoices), \
                        'Block Size': ttk.OptionMenu(self.frame, self.blockSize, *self.blockSizeChoices), \
                        'Print Style': ttk.OptionMenu(self.frame, self.knotPrintStyle,*self.knotPrintStyleChoices) \
                    }

        self.labels = {}

        menuCounter = 0
        for menu in self.menus:
            self.menus[menu].grid(column = 1,row = menuCounter,sticky='we')
            self.labels[menu] = ttk.Label(self.frame, text = menu+":")
            self.labels[menu].grid(column=0,row=menuCounter,sticky='e')
            menuCounter+=1


        self.orientation.trace('w',self.optsCallback)
        self.delimiter.trace('w',self.optsCallback)
        self.padding.trace('w',self.optsCallback)
        self.blockSize.trace('w',self.optsCallback)
        self.knotPrintStyle.trace('w',self.optsCallback)

        self.hideBtn = ttk.Button(self.frame, text="Go",command=self.hide)
        self.hideBtn.grid(columnspan=2,column=0,row=menuCounter,sticky="news")
        self.labels['Padding'].grid_forget()
        self.menus['Padding'].grid_forget()

        self.frame.grid_configure(padx=10,pady=10)
        self.frame.columnconfigure(1,minsize=120)




        self.window.withdraw()


    def optsCallback(self,objectName,*args):
        if objectName == "delimiter":
            if getattr(self,"delimiter").get() == "None (Padded)":
                self.padding.set("Padded")
                self.labels['Padding'].grid_forget()
                self.menus['Padding'].grid_forget()
            else:
                self.labels['Padding'].grid(column=0,row=2,sticky="e")
                self.menus['Padding'].grid(column=1,row=2,sticky="we")


    def hide(self):
        self.window.withdraw()
        self.parent.runSubstitution()

    def show(self):
        self.window.deiconify()
