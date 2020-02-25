from tkinter import *
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
from datetime import datetime

import os

from lib import dictGenerator as dg
from lib import substitutionCipher as sc
from lib import stringUtilities as strUtil
from lib import printGUI as pg
from lib import textObject as to

class MainWindow:

    # Constructor
    def __init__(self,parent,width,height):
        # Configure Window
        self.master = parent
        self.master.title("Knot Transcription")
        # self.master.geometry(str(width)+"x"+str(height))

        # Create Gridframe
        self.mainframe = ttk.Frame(self.master)
        self.mainframe.grid(column=0,row=1,sticky='news')
        rows = 0
        while rows < 50:
            self.mainframe.rowconfigure(rows, minsize=10)
            self.mainframe.columnconfigure(rows,weight=1)
            rows += 1

        ###################### Create Subframes ######################
        self.dictBrowserFrame = ttk.Frame(self.mainframe)
        self.dictBrowserFrame.grid(column=0,row=0,sticky='we')

        self.substitutionButtonFrame = ttk.Frame(self.mainframe)
        self.substitutionButtonFrame.grid(column=0,row=1,columnspan=2,sticky="news")

        self.transcriptionFrame = ttk.Frame(self.mainframe)
        self.transcriptionFrame.grid(column=0,row=5,columnspan=2,sticky='news')
        self.transcriptionFrame.columnconfigure(0,weight=1)

        ###################### Create Children Objects ######################
        self.printOpts = pg.PrintGUI(self)

        self.plaintext = to.TextObject(self,"plaintext")
        self.keytext = to.TextObject(self,"keytext")
        self.subtext = to.TextObject(self,"subtext")
        self.keysubtext = to.TextObject(self,"keysubtext")
        self.ciphertext = to.TextObject(self,"ciphertext")
        self.decrypttext = to.TextObject(self,"decrypttext")
        self.knottext = to.TextObject(self,"knottext")

        ###################### GUI State Fields ######################
        self.sourceDirectory = ""

        self.dict = {}
        self.dicttext = to.TextObject(self,"dicttext")

        self.dicttextSize = IntVar(name="dicttextSize")





        ###################### Dictionary Browser Frame ######################
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
        self.wordCountNumberLabel = ttk.Label(self.wordCountFrame,textvariable=self.plaintext.wordCount)
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
        self.keywordCountNumberLabel = ttk.Label(self.keywordCountFrame,textvariable=self.keytext.wordCount)
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



        ###################### Transcription Buttons Frame ######################

        self.showPrintOptsWindowBtn = ttk.Button(self.substitutionButtonFrame,text="Printing Options",command = self.printOpts.show)
        self.showPrintOptsWindowBtn.grid(column=0,row=0,sticky='news')
        self.substitutionButton = ttk.Button(self.substitutionButtonFrame,text="Run",command = self.runSubstitution)
        self.substitutionButton.grid(column=0,row=2,sticky='news')
        self.saveButton = ttk.Button(self.substitutionButtonFrame,text="Save",command=self.saveFile)
        self.saveButton.grid(column=0,row=3,sticky='news')
        self.closeButton = ttk.Button(self.substitutionButtonFrame, text="Close", command=self.master.quit)
        self.closeButton.grid(column=0,row=4,sticky='news')

        for i in range(0,3):
            self.substitutionButtonFrame.columnconfigure(i,weight=1)


        # Transcription Display Frame

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
        dictWords = dg.splitToWords(self.dicttext.text.get())
        self.dict,dictsize = dg.createDict(dictWords)
        self.dicttextSize.set(dictsize)

    def selectPlaintext(self):
        self.selectFiles("dicttext","plaintext")

    def selectOTPKey(self):
        self.selectFiles("dicttext","keytext")

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
        getattr(self,destination).text.set(text)

    ## TODO: make clears methods of to.TextObject.
    def clearPlaintext(self):
        self.plaintext.text.set("")
        self.plaintextListbox.delete(0,END)
        self.subtext.text.set("")

    def clearOTPKey(self):
        self.keytext.text.set("")
        self.keytextListbox.delete(0,END)
        self.keysubtext.text.set("")

    def runSubstitution(self):
        # Transcoding
        self.subtext.splits = sc.substitutionCipher(self.plaintext.splits,self.dict)
        self.keysubtext.splits = sc.substitutionCipher(self.keytext.splits,self.dict)
        self.ciphertext.splits = sc.otpCipher(self.subtext.splits,self.keysubtext.splits,self.dicttextSize.get())
        self.knottext.splits = [*map(sc.intToKnot,self.ciphertext.splits)]

        self.decrypttext.splits = sc.decrypt(self.dict,self.ciphertext.splits)

        # Numerical String Generation
        self.subtext.text.set(strUtil.formatInts(self.subtext.splits, self.printOpts))
        self.keysubtext.text.set(strUtil.formatInts(self.keysubtext.splits, self.printOpts))
        self.ciphertext.text.set(strUtil.formatInts(self.ciphertext.splits, self.printOpts))

        self.decrypttext.text.set(" ".join(self.decrypttext.splits))

        # Knot String Formatting
        strFormatter = getattr(strUtil,"formatKnots"+self.printOpts.knotPrintStyle.get())
        self.knottext.text.set(strFormatter(self.knottext.splits,self.printOpts.blockSize.get()))

    def saveFile(self):
        saveDirectory = filedialog.askdirectory()
        saveDirectory = saveDirectory + "/exports_"+datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+"/"
        print("Exporting Files to "+saveDirectory)
        os.mkdir(saveDirectory)
        with open(saveDirectory+"knottext.txt",'w') as file:
            file.write(self.knottext.text.get())
        with open(saveDirectory+"ciphertext.txt",'w') as file:
            file.write(self.ciphertext.text.get())
        with open(saveDirectory+"invertedciphertext.txt",'w') as file:
            file.write(self.decrypttext.text.get())
        with open(saveDirectory+"keytext.txt",'w') as file:
            file.write(self.keysubtext.text.get())
        with open(saveDirectory+"plaintext.txt",'w') as file:
            file.write(self.subtext.text.get())
