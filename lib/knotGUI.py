from tkinter import *
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk

import os

from lib import dictGenerator as dg
from lib import substitutionCipher as sc
from lib import stringUtilities as strUtil

class KnotGUI:

    # Constructor
    def __init__(self,parent,width,height):
        # Configure Window
        self.master = parent
        self.master.title("Knot Transcription")
        self.master.geometry(str(width)+"x"+str(height))

        # GUI State Fields
        self.sourceDirectory = ""

        self.dict = {}
        self.dicttext = StringVar(name="dicttext")
        self.dicttext.set("")
        self.dicttextSize = IntVar(name="dicttextSize")

        self.plaintext = StringVar(name="plaintext")
        self.plaintext.set("")
        self.plaintext.trace('w',self.scrolledTextUpdater)
        self.plaintextWords = []
        self.plaintextWordCount = IntVar(name="plaintextWordCount")

        self.keytext = StringVar(name="keytext")
        self.keytext.set("")
        self.keytext.trace('w',self.scrolledTextUpdater)
        self.keytextWords = []

        self.subtext = StringVar(name="subtext")
        self.subtext.set("")
        self.subtext.trace('w',self.scrolledTextUpdater)
        self.subtextWords = []

        self.keysubtext = StringVar(name="keysubtext")
        self.keysubtext.set("")
        # self.keysubtext.trace('w',self.scrolledTextUpdater)
        self.keysubtextWords = []

        self.knottextWords = []
        self.knottext = StringVar(name="knottext")
        self.knottext.set("")
        self.knottext.trace('w',self.scrolledTextUpdater)
        self.knotRowSize = IntVar(name="knotRowSize")
        self.knotRowSize.set(1) # set the default option
        self.knotRowChoices = [i for i in range(1,10)]

        # Create Gridframe
        self.mainframe = ttk.Frame(self.master)
        self.mainframe.grid(column=0,row=1,sticky='news')

        # create default grid sizing?
        rows = 0
        while rows < 50:
            self.mainframe.rowconfigure(rows, weight=1)
            self.mainframe.columnconfigure(rows,weight=1)
            rows += 1

        # Dictionary Browser
        self.dictBrowserFrame = ttk.Frame(self.master)
        self.dictBrowserFrame.grid(column=0,row=0,sticky='we')
        self.folderButton = ttk.Button(self.dictBrowserFrame,text="Select Folder >",command=self.openFolder)
        self.folderButton.grid(column=0,row=1,sticky='ns')
        self.directoryListbox = Listbox(self.dictBrowserFrame,selectmode=EXTENDED)
        self.directoryListbox.grid(column=1,row=0,rowspan=3,sticky='news')
        self.selectDicttext = ttk.Button(self.dictBrowserFrame,text="> Dictionary >",command=self.selectDicttext)
        self.selectDicttext.grid(column=2,row=1)
        self.dicttextListbox = Listbox(self.dictBrowserFrame)
        self.dicttextListbox.grid(column=3,row=0,rowspan=3,sticky='news')
        self.selectPlaintextButton = ttk.Button(self.dictBrowserFrame,text="> Plaintext >",command = self.selectPlaintext)
        self.selectPlaintextButton.grid(column=5,row=0,sticky="ns")
        self.selectotpKeyButton = ttk.Button(self.dictBrowserFrame,text="> OTP Key >",command = self.selectOTPKey)
        self.selectotpKeyButton.grid(column=5,row=2,sticky="ns")
        self.plaintextListbox = Listbox(self.dictBrowserFrame,selectmode=BROWSE)
        self.plaintextListbox.grid(column=6,row=0,sticky='ew')
        self.keytextListbox = Listbox(self.dictBrowserFrame,selectmode=BROWSE)
        self.keytextListbox.grid(column=6,row=2,sticky='ew')

        for child in self.dictBrowserFrame.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.plaintextDisplay = ScrolledText(self.dictBrowserFrame,width=40,height=10,wrap=WORD)
        self.plaintextDisplay.grid(column=7,row=0)
        self.keytextDisplay = ScrolledText(self.dictBrowserFrame,width=40,height=10,wrap=WORD)
        self.keytextDisplay.grid(column=7,row=2)

        self.wordCountFrame = ttk.Frame(self.dictBrowserFrame)
        self.wordCountFrame.grid(column=7,row=1)
        self.wordCountTextLabel = ttk.Label(self.wordCountFrame,text="Word Count:")
        self.wordCountTextLabel.grid(column=0,row=0,sticky="e")
        self.wordCountNumberLabel = ttk.Label(self.wordCountFrame,textvariable=self.plaintextWordCount)
        self.wordCountNumberLabel.grid(column=1,row=0,sticky="w")

        # Row 2
        self.dictSizeFrame = ttk.Frame(self.dictBrowserFrame)
        self.dictSizeFrame.grid(column=3,row=3)
        self.dictSizeTextLabel = ttk.Label(self.dictSizeFrame,text="Dictionary Size:")
        self.dictSizeTextLabel.grid(column=0,row=0,sticky="e")
        self.dictSizeNumberLabel = ttk.Label(self.dictSizeFrame,textvariable=self.dicttextSize)
        self.dictSizeNumberLabel.grid(column=1,row=0,sticky="w")


        # Row 3
        self.substitionButton = ttk.Button(self.mainframe,text="Substitution Cipher",command = self.runSubstitution)
        self.substitionButton.grid(column=0,row=3,sticky='we')
        self.dropDownMenu = ttk.OptionMenu(self.mainframe, self.knotRowSize, *self.knotRowChoices)
        self.dropDownMenu.grid(column=2,row=3,sticky='e')
        self.dropDownMenuLabel = ttk.Label(self.mainframe, text="Knots/Row")
        self.dropDownMenuLabel.grid(column=3,row=3,sticky='w')

        # Row 4
        self.subtextDisplay = ScrolledText(self.mainframe,width=50,height=5,wrap=WORD)
        self.subtextDisplay.grid(column=0,row=4,columnspan=5,sticky='w')

        # Row 5
        self.knottextDisplay = ScrolledText(self.mainframe,width=50,height=5,wrap=WORD)
        self.knottextDisplay.grid(column=0,row=5,columnspan=5,sticky='w')

        # Row 10
        self.saveButton = ttk.Button(self.mainframe,text="Save",command=self.saveFile)
        self.saveButton.grid(column=0,row=10,stick='w')

        # Row 11
        self.closeButton = ttk.Button(self.mainframe, text="Close", command=self.master.quit)
        self.closeButton.grid(column=0,row=11,sticky='w')

        # Padding
        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=2, pady=5)

    def openFolder(self):
        self.sourceDirectory = filedialog.askdirectory()
        files = os.listdir(self.sourceDirectory)
        self.directoryListbox.delete(0,END)
        for file in files:
            if file.endswith(".txt"):
                self.directoryListbox.insert(END,file)

    def selectDicttext(self):
        self.selectFiles("directory","dicttext")
        dictWords = dg.splitToWords(self.dicttext.get())
        self.dict,dictsize = dg.createDict(dictWords)
        self.dicttextSize.set(dictsize)

    def selectPlaintext(self):
        self.selectFiles("dicttext","plaintext")
        self.plaintextWords = dg.splitToWords(self.plaintext.get())
        self.plaintextWordCount.set(len(self.plaintextWords))

    def selectOTPKey(self):
        self.selectFiles("dicttext","keytext")
        self.keytextWords = dg.splitToWords(self.keytext.get())

    def runSubstitution(self):
        # TODO: Add ability to choose between knottextformatting
        # TODO: Add OTP functionality
        self.subtextWords = sc.substitutionCipher(self.plaintextWords,self.dict)            # Transcoding
        self.keysubtextWords = sc.substitutionCipher(self.keytextWords,self.dict)           # Transcoding
        self.knottextWords = [*map(sc.intToKnot,self.subtextWords)]                         # Transcoding (map and unpack)
        self.subtext.set(strUtil.formatInts(self.subtextWords))                             # Numerical String Generation
        self.knottext.set(strUtil.formatKnotsA(self.knottextWords,self.knotRowSize.get()))  # Knot Score String Generation

    def saveFile(self):
        # TODO: Improve file/directory naming
        # TODO: Decide if it should create new directory, or deposit in pre-existing directory.
        saveDirectory = filedialog.askdirectory()
        os.mkdir(saveDirectory+"/scores/")
        with open(saveDirectory+"/scores/knottext.txt",'w') as file:
            file.write(self.knottext.get())
        with open(saveDirectory+"/scores/subtext.txt",'w') as file:
            file.write(self.subtext.get())

    def scrolledTextUpdater(self,objectName,*args):
        # Overwrite scrolled text when traced StringVar changes
        obj = getattr(self,objectName+"Display")
        obj.config(state=NORMAL)
        obj.delete(1.0,END)
        obj.insert(END,getattr(self,objectName).get())
        obj.config(state=DISABLED)

    def selectFiles(self,source,destination):
        # Get source Listbox selected indices as filenames
        indices = getattr(self,source+"Listbox").curselection()
        filenames = map(getattr(self,source+"Listbox").get,indices)

        # Clear Destination Listbox
        getattr(self,destination+"Listbox").delete(0,END)

        # Convert selected files to strings and concatenate
        text = ""
        for file in filenames:
            path = self.sourceDirectory+"/"+file
            text = text+strUtil.fileToStr(path)+"\n"
            getattr(self,destination+"Listbox").insert(END,file)

        # Set destination StringVar
        getattr(self,destination).set(text)
