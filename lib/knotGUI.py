from tkinter import *
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk

import os

from lib import dictGenerator as dg
from lib import substitutionCipher as sc

class KnotGUI:

    # Constructor
    def __init__(self,parent,width,height):
        self.master = parent
        self.master.title("Knot Transcription")
        self.master.geometry(str(width)+"x"+str(height))

        # GUI State Variables
        self.path = StringVar()
        self.path.set("Select a file...")
        self.dict = {}
        self.plaintext = StringVar()
        self.plaintext.set("")
        self.words = []
        self.dictSize = IntVar()
        self.wordCount = IntVar()
        self.substitutionText = []
        self.numericalRepresentation = ""
        self.knotText = []
        self.knotRowSize = IntVar()
        self.knotRowSize.set(1) # set the default option
        self.knotRowChoices = [i for i in range(1,10)]
        self.knotScore = ""

        # Create Gridframe
        self.mainframe = ttk.Frame(self.master)
        self.mainframe.grid(column=0,row=0,sticky='news')

        # create default grid sizing?
        rows = 0
        while rows < 50:
            self.master.rowconfigure(rows, weight=1)
            self.master.columnconfigure(rows,weight=1)
            rows += 1

        # Row 0
        self.selectFileButton = ttk.Button(self.mainframe, text="Open",command = self.openFile)
        self.selectFileButton.grid(column=0,row=0,sticky='we')
        self.inputPathLabel = ttk.Label(self.mainframe,textvariable=self.path)
        self.inputPathLabel.grid(column=1,row=0,columnspan=5,sticky="w")

        # Row 1
        self.fileDisplay = ScrolledText(self.mainframe,width=50,height=5,wrap=WORD)
        self.fileDisplay.grid(column=0,row=1,columnspan=5)

        # Row 2
        self.dictSizeTextLabel = ttk.Label(self.mainframe,text="Dictionary Size:")
        self.dictSizeTextLabel.grid(column=0,row=2,sticky="e")
        self.dictSizeNumberLabel = ttk.Label(self.mainframe,textvariable=self.dictSize)
        self.dictSizeNumberLabel.grid(column=1,row=2,sticky="w")
        self.wordCountTextLabel = ttk.Label(self.mainframe,text="Word Count:")
        self.wordCountTextLabel.grid(column=2,row=2,sticky="e")
        self.wordCountNumberLabel = ttk.Label(self.mainframe,textvariable=self.wordCount)
        self.wordCountNumberLabel.grid(column=3,row=2,sticky="w")

        # Row 3
        self.substitionButton = ttk.Button(self.mainframe,text="Substitution Cipher",command = self.runSubstitution)
        self.substitionButton.grid(column=0,row=3,sticky='we')
        self.dropDownMenu = ttk.OptionMenu(self.mainframe, self.knotRowSize, *self.knotRowChoices)
        self.dropDownMenu.grid(column=2,row=3,sticky='e')
        self.dropDownMenuLabel = ttk.Label(self.mainframe, text="Knots/Row")
        self.dropDownMenuLabel.grid(column=3,row=3,sticky='w')

        # Row 4
        self.substitutionDisplay = ScrolledText(self.mainframe,width=50,height=5,wrap=WORD)
        self.substitutionDisplay.grid(column=0,row=4,columnspan=5,sticky='w')

        # Row 5
        self.knotDisplay = ScrolledText(self.mainframe,width=50,height=5,wrap=WORD)
        self.knotDisplay.grid(column=0,row=5,columnspan=5,sticky='w')

        # Row 10
        self.saveButton = ttk.Button(self.mainframe,text="Save",command=self.saveFile)
        self.saveButton.grid(column=0,row=10,stick='w')

        # Row 11
        self.closeButton = ttk.Button(self.mainframe, text="Close", command=self.master.quit)
        self.closeButton.grid(column=0,row=11,sticky='w')





        # Padding
        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=2, pady=5)

    # TODO : separate button callbacks and gui updates?
    # Open Button Callback
    def openFile(self):
        # Get path
        self.path.set(filedialog.askopenfilename(initialdir = "./",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*"))))

        # Open and combine file to single string, update display
        with open(self.path.get()) as lines:
            for line in lines:
                self.plaintext.set(self.plaintext.get()+line)
        self.fileDisplay.delete(1.0,END)
        self.fileDisplay.insert(END,self.plaintext.get())
        self.fileDisplay.config(state=DISABLED)

        # Create Dictionary
        self.words = dg.splitToWords(self.plaintext.get())
        self.dict,dictSize = dg.createDict(self.words) # returns tuple
        self.wordCount.set(len(self.words))
        self.dictSize.set(dictSize)

    def runSubstitution(self):
        # Transcoding
        self.substitutionText = sc.substitutionCipher(self.words,self.dict)
        self.knotText = map(sc.intToKnot,self.substitutionText)

        # Numerical String Generation
        self.numericalRepresentation = sc.formatInts(self.substitutionText)
        self.substitutionDisplay.delete(1.0,END)
        self.substitutionDisplay.insert(END,self.numericalRepresentation)

        # Knot Score String Generation
        self.knotScore = sc.formatKnots(self.knotText,self.knotRowSize.get())
        self.knotDisplay.delete(1.0,END)
        self.knotDisplay.insert(END,self.knotScore)

    def saveFile(self):
        # TODO: Improve file/directory naming
        # TODO: Decide if it should create new directory, or deposit in pre-existing directory.
        saveDirectory = filedialog.askdirectory()
        os.mkdir(saveDirectory+"/scores/")
        with open(saveDirectory+"/scores/knotScore.txt",'w') as file:
            file.write(self.knotScore)
        with open(saveDirectory+"/scores/numericalRepresentation.txt",'w') as file:
            file.write(self.numericalRepresentation)
