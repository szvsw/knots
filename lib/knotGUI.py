from tkinter import *
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
from datetime import datetime

import os

from lib import dictGenerator as dg
from lib import substitutionCipher as sc
from lib import stringUtilities as strUtil


class MainWindow:

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
        self.keytextWordCount = IntVar(name="keytextWordCount")

        self.subtext = StringVar(name="subtext")
        self.subtext.set("")
        self.subtext.trace('w',self.scrolledTextUpdater)
        self.subtextWords = []

        self.keysubtext = StringVar(name="keysubtext")
        self.keysubtext.set("")
        self.keysubtext.trace('w',self.scrolledTextUpdater)
        self.keysubtextWords = []

        self.ciphertext = StringVar(name="ciphertext")
        self.ciphertext.set("")
        self.ciphertext.trace('w',self.scrolledTextUpdater)
        self.ciphertextWords = []

        self.decrypttext = StringVar(name="decrypttext")
        self.decrypttext.set("")
        self.decrypttext.trace('w',self.scrolledTextUpdater)
        self.decrypttextWords = []

        self.knottextWords = []
        self.knottext = StringVar(name="knottext")
        self.knottext.set("")
        self.knottext.trace('w',self.scrolledTextUpdater)
        self.knotRowSize = IntVar(name="knotRowSize")
        self.knotRowSize.set(1) # set the default option
        self.knotRowSizeChoices = [i for i in range(1,30)]
        self.knotPrintStyleChoices = ["Simple", "Pretty"]
        self.knotPrintStyle = StringVar(name="knotPrintStyle")
        self.knotPrintStyle.set("")

        self.delimiterOpts = {'delimited' : False, 'delimiterR' : "", 'delimiterL' : "", 'delimiterC' : ".", 'formatting':"zeros"}

        # Create Gridframe
        self.mainframe = ttk.Frame(self.master)
        self.mainframe.grid(column=0,row=1,sticky='news')

        # create default grid sizing?
        rows = 0
        while rows < 50:
            self.mainframe.rowconfigure(rows, minsize=10)
            self.mainframe.columnconfigure(rows,weight=1)
            rows += 1

        # Dictionary Browser
        self.dictBrowserFrame = ttk.Frame(self.mainframe)
        self.dictBrowserFrame.grid(column=0,row=0,sticky='we')
        self.folderButton = ttk.Button(self.dictBrowserFrame,text="Select Folder >",command=self.openFolder)
        self.folderButton.grid(column=0,row=1,sticky='ns')
        self.directoryListbox = Listbox(self.dictBrowserFrame,selectmode=EXTENDED)
        self.directoryListbox.grid(column=1,row=0,rowspan=3,sticky='news')



        self.dictSelectionFrame = ttk.Frame(self.dictBrowserFrame)
        self.dictSelectionFrame.grid(column=2,row=1)
        self.dictSelectionFrame.columnconfigure(0,minsize=120)

        self.selectDicttext = ttk.Button(self.dictSelectionFrame,text="> Dictionary >",command=self.selectDicttext)
        self.selectDicttext.grid(column=0,row=0,sticky='ew')

        self.dictSizeFrame = ttk.Frame(self.dictSelectionFrame)
        self.dictSizeFrame.grid(column=0,row=1)
        self.dictSizeTextLabel = ttk.Label(self.dictSizeFrame,text="Dictionary Size:")
        self.dictSizeTextLabel.grid(column=0,row=0,sticky="ne")
        self.dictSizeNumberLabel = ttk.Label(self.dictSizeFrame,textvariable=self.dicttextSize)
        self.dictSizeNumberLabel.grid(column=1,row=0,sticky="nw")

        self.dicttextListbox = Listbox(self.dictBrowserFrame,selectmode=EXTENDED)
        self.dicttextListbox.grid(column=3,row=0,rowspan=3,sticky='news')

        # Setup Plaintext Frame
        self.plaintextFrame = ttk.Frame(self.dictBrowserFrame)
        self.plaintextFrame.grid(column=4,row=0,sticky='news')
        # Setup Buttons Subframe
        self.plaintextButtonsFrame = ttk.Frame(self.plaintextFrame)
        self.plaintextButtonsFrame.grid(column = 0,row=0,sticky="ns")
        self.plaintextButtonsFrame.rowconfigure(0,weight=1)
        self.plaintextButtonsFrame.columnconfigure(0,minsize = 120)
        self.selectPlaintextButton = ttk.Button(self.plaintextButtonsFrame,text="> Plaintext >",command = self.selectPlaintext)
        self.selectPlaintextButton.grid(column=0,row=0,sticky="news")
        self.clearPlaintextButton = ttk.Button(self.plaintextButtonsFrame,text="Clear Plaintext", command = self.clearPlaintext)
        self.clearPlaintextButton.grid(column=0,row=1,sticky='news')
        # Setup Wordcount Subframe
        self.wordCountFrame = ttk.Frame(self.plaintextButtonsFrame)
        self.wordCountFrame.grid(column=0,row=2)
        self.wordCountTextLabel = ttk.Label(self.wordCountFrame,text="Word Count:")
        self.wordCountTextLabel.grid(column=0,row=0,sticky="e")
        self.wordCountNumberLabel = ttk.Label(self.wordCountFrame,textvariable=self.plaintextWordCount)
        self.wordCountNumberLabel.grid(column=1,row=0,sticky="w")
        # Finish Plaintext Frame
        self.plaintextListbox = Listbox(self.plaintextFrame,selectmode=BROWSE)
        self.plaintextListbox.grid(column=1,row=0,sticky='ew')
        self.plaintextDisplay = ScrolledText(self.plaintextFrame,width=40,height=10,wrap=WORD)
        self.plaintextDisplay.grid(column=2,row=0)
        self.subtextDisplay = ScrolledText(self.plaintextFrame,width=40,height=10,wrap=WORD)
        self.subtextDisplay.grid(column=3,row=0)

        # Setup Keytext Frame
        self.keytextFrame = ttk.Frame(self.dictBrowserFrame)
        self.keytextFrame.grid(column=4,row=2,sticky='news')
        # Setup Buttons Subframe
        self.keytextButtonsFrame = ttk.Frame(self.keytextFrame)
        self.keytextButtonsFrame.grid(column = 0,row=0,sticky="ns")
        self.keytextButtonsFrame.rowconfigure(0,weight=1)
        self.keytextButtonsFrame.columnconfigure(0,minsize = 120)
        self.selectotpKeyButton = ttk.Button(self.keytextButtonsFrame,text="> Vigenere Key >",command = self.selectOTPKey)
        self.selectotpKeyButton.grid(column=0,row=0,sticky="news")
        self.clearKeytextButton = ttk.Button(self.keytextButtonsFrame,text="Clear Vigenere Key", command = self.clearOTPKey)
        self.clearKeytextButton.grid(column=0,row=1,sticky='news')
        # Setup Wordcount Subframe
        self.keywordCountFrame = ttk.Frame(self.keytextButtonsFrame)
        self.keywordCountFrame.grid(column=0,row=2)
        self.keywordCountTextLabel = ttk.Label(self.keywordCountFrame,text="Word Count:")
        self.keywordCountTextLabel.grid(column=0,row=0,sticky="e")
        self.keywordCountNumberLabel = ttk.Label(self.keywordCountFrame,textvariable=self.keytextWordCount)
        self.keywordCountNumberLabel.grid(column=1,row=0,sticky="w")
        # Finish Keytext Frame
        self.keytextListbox = Listbox(self.keytextFrame,selectmode=BROWSE)
        self.keytextListbox.grid(column=1,row=0,sticky='ew')
        self.keytextDisplay = ScrolledText(self.keytextFrame,width=40,height=10,wrap=WORD)
        self.keytextDisplay.grid(column=2,row=0)
        self.keysubtextDisplay = ScrolledText(self.keytextFrame,width=40,height=10,wrap=WORD)
        self.keysubtextDisplay.grid(column=3,row=0)

        for child in self.dictBrowserFrame.winfo_children():
            child.grid_configure(padx=2,pady=5)

        for child in self.plaintextFrame.winfo_children():
            child.grid_configure(padx=2)

        for child in self.keytextFrame.winfo_children():
            child.grid_configure(padx=2)



        # Transcription Buttons Frame
        self.substitutionButtonFrame = ttk.Frame(self.mainframe)
        self.substitutionButtonFrame.grid(column=1,row=0,sticky="ews")

        self.dropDownMenu = ttk.OptionMenu(self.substitutionButtonFrame, self.knotRowSize, *self.knotRowSizeChoices)
        self.dropDownMenu.grid(column=0,row=0,sticky='ew')
        self.dropDownMenuLabel = ttk.Label(self.substitutionButtonFrame, text="Knots/Row")
        self.dropDownMenuLabel.grid(column=1,row=0,sticky='w')
        self.knotPrintStyleMenu = ttk.OptionMenu(self.substitutionButtonFrame,self.knotPrintStyle, *self.knotPrintStyleChoices)
        self.knotPrintStyleMenu.grid(column=0,row=1,sticky='ew')
        self.knotPrintStyleMenuLabel = ttk.Label(self.substitutionButtonFrame, text="Formatting")
        self.knotPrintStyleMenuLabel.grid(column=1,row=1,sticky='w')
        self.substitutionButton = ttk.Button(self.substitutionButtonFrame,text="Run",command = self.runSubstitution)
        self.substitutionButton.grid(column=0,row=2,columnspan=2,sticky='news')
        self.saveButton = ttk.Button(self.substitutionButtonFrame,text="Save",command=self.saveFile)
        self.saveButton.grid(column=0,row=3,columnspan=2,sticky='news')
        self.closeButton = ttk.Button(self.substitutionButtonFrame, text="Close", command=self.master.quit)
        self.closeButton.grid(column=0,row=4,columnspan=2,sticky='news')


        # Transcription Display Frame
        self.transcriptionFrame = ttk.Frame(self.mainframe)
        self.transcriptionFrame.grid(column=0,row=5,columnspan=2,sticky='news')
        self.transcriptionFrame.columnconfigure(0,weight=1)

        self.ciphertextDisplay = ScrolledText(self.transcriptionFrame,width=100,height=8,wrap=WORD)
        self.ciphertextDisplay.grid(column=0,row=0,sticky='news')
        self.decrypttextDisplay = ScrolledText(self.transcriptionFrame,width=100,height=8,wrap=WORD)
        self.decrypttextDisplay.grid(column=0,row=1,sticky='news')
        self.knottextDisplay = ScrolledText(self.transcriptionFrame,width=100,height=8,wrap=WORD)
        self.knottextDisplay.grid(column=0,row=2,sticky='news')
        ttk.Label(self.transcriptionFrame,text="VIGENERE CIPHERTEXT").grid(column=1,row=0)
        ttk.Label(self.transcriptionFrame,text="INVERTED CIPHERTEXT").grid(column=1,row=1)
        ttk.Label(self.transcriptionFrame,text="KNOT TRANSCRIPTION").grid(column=1,row=2)


        # Padding
        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=20, pady=5)

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
        self.keytextWordCount.set(len(self.keytextWords))

    def clearPlaintext(self):
        self.plaintext.set("")
        self.plaintextWords = []
        self.plaintextWordCount.set(0)
        self.plaintextListbox.delete(0,END)
        self.subtext.set("")
        self.subtextWords = []

    def clearOTPKey(self):
        self.keytext.set("")
        self.keytextWords = []
        self.keytextWordCount.set(0)
        self.keytextListbox.delete(0,END)
        self.keysubtext.set("")
        self.keysubtextWords = []

    def runSubstitution(self):
        # Transcoding
        self.subtextWords = sc.substitutionCipher(self.plaintextWords,self.dict)
        self.keysubtextWords = sc.substitutionCipher(self.keytextWords,self.dict)
        self.ciphertextWords = sc.otpCipher(self.subtextWords,self.keysubtextWords,self.dicttextSize.get())
        self.knottextWords = [*map(sc.intToKnot,self.ciphertextWords)]

        self.decrypttextWords = sc.decrypt(self.dict,self.ciphertextWords)

        # Numerical String Generation
        self.subtext.set(strUtil.formatInts(self.subtextWords, self.delimiterOpts))
        self.keysubtext.set(strUtil.formatInts(self.keysubtextWords, self.delimiterOpts))
        self.ciphertext.set(strUtil.formatInts(self.ciphertextWords, self.delimiterOpts))

        self.decrypttext.set(" ".join(self.decrypttextWords))

        # Knot String Formatting
        strFormatter = getattr(strUtil,"formatKnots"+self.knotPrintStyle.get())
        self.knottext.set(strFormatter(self.knottextWords,self.knotRowSize.get()))

    def saveFile(self):
        saveDirectory = filedialog.askdirectory()
        saveDirectory = saveDirectory + "/exports_"+datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+"/"
        print("Exporting Files to "+saveDirectory)
        os.mkdir(saveDirectory)
        with open(saveDirectory+"knottext.txt",'w') as file:
            file.write(self.knottext.get())
        with open(saveDirectory+"ciphertext.txt",'w') as file:
            file.write(self.ciphertext.get())
        with open(saveDirectory+"invertedciphertext.txt",'w') as file:
            file.write(self.decrypttext.get())
        with open(saveDirectory+"keytext.txt",'w') as file:
            file.write(self.keysubtext.get())
        with open(saveDirectory+"plaintext.txt",'w') as file:
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
