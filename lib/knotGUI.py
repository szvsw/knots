from tkinter import *
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk

import os

from lib import dictGenerator as dg
from lib import substitutionCipher as sc
from lib import stringUtilities as strUtil

# TODO: Add ability to use folder library as dict; select files for transcoding

class KnotGUI:

    # Constructor
    def __init__(self,parent,width,height):
        self.master = parent
        self.master.title("Knot Transcription")
        self.master.geometry(str(width)+"x"+str(height))

        # GUI State Variables
        self.sourceDirectory = ""

        self.plaintext = StringVar(name="plaintext")
        self.plaintext.set("")

        self.dict = {}
        self.dicttext = StringVar(name="dicttext")
        self.dicttext.set("")
        self.dictSize = IntVar(name="dictsize")

        self.words = []
        self.wordCount = IntVar(name="wordcount")

        self.substitutionText = []
        self.numericalRepresentation = StringVar(name="numericalRepresentation")
        self.knotText = []
        self.knotRowSize = IntVar(name="knotRowSize")
        self.knotRowSize.set(1) # set the default option
        self.knotRowChoices = [i for i in range(1,10)]
        self.knotScore = StringVar(name="knotscore")

        # Create Gridframe
        self.mainframe = ttk.Frame(self.master)
        self.mainframe.grid(column=0,row=1,sticky='news')

        # create default grid sizing?
        rows = 0
        while rows < 50:
            self.master.rowconfigure(rows, weight=1)
            self.master.columnconfigure(rows,weight=1)
            rows += 1


        # Row 1
        self.plaintextDisplay = ScrolledText(self.mainframe,width=50,height=5,wrap=WORD)
        self.plaintextDisplay.grid(column=0,row=1,columnspan=5)


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

        # Row 12
        self.dictBrowserFrame = ttk.Frame(self.master)
        self.dictBrowserFrame.grid(column=0,row=0,sticky='we')
        self.directoryList = Listbox(self.dictBrowserFrame,selectmode=EXTENDED)
        self.directoryList.grid(column=0,row=0,rowspan=3,sticky='ew')
        self.addFilestoDictButton = ttk.Button(self.dictBrowserFrame,text="> Add to Dictionary >",command=self.addFilesToDict)
        self.addFilestoDictButton.grid(column=1,row=1,sticky='ew')
        self.dictionaryList = Listbox(self.dictBrowserFrame)
        self.dictionaryList.grid(column=2,row=0,rowspan=3,sticky='ew')
        self.folderButton = ttk.Button(self.dictBrowserFrame,text="Select Folder",command=self.openFolder)
        self.folderButton.grid(column=0,row=3,sticky='ew')
        self.selectPlaintextButton = ttk.Button(self.dictBrowserFrame,text="Select Plaintext",command = self.selectPlaintext)
        self.selectPlaintextButton.grid(column=2,row=3,sticky='ew')

        # Row 13

        # Padding
        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=2, pady=5)

    # TODO : separate button callbacks and gui updates?
    def openFolder(self):
        self.sourceDirectory = filedialog.askdirectory()
        files = os.listdir(self.sourceDirectory)
        self.directoryList.delete(0,END)
        for file in files:
            if file.endswith(".txt"):
                self.directoryList.insert(END,file)

    def addFilesToDict(self):
        selectedIndices = self.directoryList.curselection()
        selectedFilepaths = map(self.directoryList.get,selectedIndices)
        text = ""
        for file in selectedFilepaths:
            text = text+strUtil.fileToStr(self.sourceDirectory+"/"+file)+"\n"
            self.dictionaryList.insert(END,file)
        self.dicttext.set(self.dicttext.get()+text)
        dictWords = dg.splitToWords(self.dicttext.get())
        self.dict,dictsize = dg.createDict(dictWords)
        self.dictSize.set(dictsize)

    def selectPlaintext(self):
        selectedIndices = self.dictionaryList.curselection()
        selectedFilepaths = map(self.dictionaryList.get,selectedIndices)
        text = ""
        for file in selectedFilepaths:
            path = self.sourceDirectory+"/"+file
            text = text+strUtil.fileToStr(path)+"\n"
        self.plaintext.set(text)

        self.words = dg.splitToWords(self.plaintext.get())
        self.wordCount.set(len(self.words))
        # Update Display
        # TODO: put in single gui updater callback
        self.plaintextDisplay.delete(1.0,END)
        self.plaintextDisplay.insert(END,self.plaintext.get())
        self.plaintextDisplay.config(state=DISABLED)

    def runSubstitution(self):
        # Transcoding
        self.substitutionText = sc.substitutionCipher(self.words,self.dict)
        self.knotText = map(sc.intToKnot,self.substitutionText)

        # Numerical String Generation
        self.numericalRepresentation.set(strUtil.formatInts(self.substitutionText))
        # TODO: move to gui callback
        self.substitutionDisplay.delete(1.0,END)
        self.substitutionDisplay.insert(END,self.numericalRepresentation.get())

        # Knot Score String Generation
        self.knotScore.set(strUtil.formatKnots(self.knotText,self.knotRowSize.get()))
        # TODO: move to gui callback
        self.knotDisplay.delete(1.0,END)
        self.knotDisplay.insert(END,self.knotScore.get())

    def saveFile(self):
        # TODO: Improve file/directory naming
        # TODO: Decide if it should create new directory, or deposit in pre-existing directory.
        saveDirectory = filedialog.askdirectory()
        os.mkdir(saveDirectory+"/scores/")
        with open(saveDirectory+"/scores/knotScore.txt",'w') as file:
            file.write(self.knotScore.get())
        with open(saveDirectory+"/scores/numericalRepresentation.txt",'w') as file:
            file.write(self.numericalRepresentation.get())
