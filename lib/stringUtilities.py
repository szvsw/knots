from random import randint as ri

def formatInts(integerList,optsObj):
    s = ""
    delimiterL = ""
    delimiterC = ""
    delimiterR = ""
    formatter = "{:01d}"
    if len(optsObj.delimiter.get())==1:
        delimiterC = optsObj.delimiter.get()
    elif optsObj.delimiter.get() == "<space>":
        delimiterC = " "
    if optsObj.delimiter.get() == "None (Padded)" or optsObj.padding.get() == "Padded":
        formatter = "{:04d}"
    if len(optsObj.delimiter.get())==2:
        delimiterL = optsObj.delimiter.get()[0]
        delimiterR = optsObj.delimiter.get()[1]
    for i in integerList:
        s = s+delimiterL+formatter.format(i)+delimiterR+delimiterC
    if delimiterC != "":
        s = s[0:len(s)-1] # truncate last character - get rid of this when using s formatting

    return s

def formatKnotsRowsSimple(knotList,optsObj):
    rowSize = optsObj.blockSize.get()
    orientation = optsObj.orientation.get()
    currentRow = 0
    s = "KNOT SCORE\n"
    while currentRow*rowSize < len(knotList): # stop when no knots remain
        knotRow = knotList[currentRow*rowSize:(currentRow*rowSize+rowSize)] # get rows worth of knots
        s = s+"\n--- "+orientation[0:-1]+" %03d ---\n" % currentRow

        knotRow = "\n".join([*map(lambda x: ".".join(x),knotRow)])
        s=s+knotRow+"\n"

        currentRow = currentRow+1
    return s

def formatKnotsRowsPretty(knotList,optsObj):
    rowSize = optsObj.blockSize.get()
    orientation = optsObj.orientation.get()
    currentRow = 0
    textLocation = 0
    s = "KNOT SCORE\n\n"
    while textLocation!=len(knotList):
        currentRow = currentRow +1

        ### Title ###
        s = s+"--- "+orientation[0:-1]+" %03d ---\n\n" % currentRow

        ### ColN ###
        # Offset
        if (currentRow%2)==0: s = s+"       "
        for k in range(rowSize):
            colNo = k*2+2-(currentRow%2)
            s=s+"COL%02d" % (colNo)
            s=s+"         "
        s=s+"\n"

        ### Tops ###
        # Offset
        if (currentRow%2)==0: s = s+"       "
        i = 0
        specialCharCounter = 0
        # Advance forward in knot list until n knots are found
        # Pop out indicators; knots should stay aligned.
        while i<rowSize and textLocation+i != len(knotList):
            knot = knotList[textLocation+i]
            if knot != "\\STOP" or knot != "\\NEWLINE":
                # if we are on a new line, no need to make up
                # for previous indicators pritned.
                if i != 0:
                    # accurate separation between knots must account for special chars
                    for k in range(8-specialCharCounter): # (9 is number of spaces between knots)
                        s = s+" "
                specialCharCounter = 0 # Reset Special Char Counter
                s = s+knot[0]+"|"+knot[1]+" " # Add knot top halves
                i = i+1 # Move to next location
                if textLocation+i == len(knotList): # stop everything if no knots left
                    break
                # before we get next true knot, let's get rid of all
                # special indicators.
                while knotList[textLocation+i]=="\\STOP" or knotList[textLocation+i] == "\\NEWLINE":
                    s = s+knotList[textLocation+i][0:2]
                    knotList.pop(textLocation+i)
                    specialCharCounter = specialCharCounter+2
                    if textLocation+i==len(knotList):
                        break
        s=s+"\n"

        ### Bottoms ###
        # Offset
        if (currentRow%2)==0: s = s+"       "
        i = 0
        specialCharCounter = 0
        while i<rowSize and textLocation+i != len(knotList):
            knot = knotList[textLocation+i]
            if knot != "\\STOP" or knot != "\\NEWLINE":
                # if we are on a new line, no need to make up
                # for previous indicators pritned.
                if i != 0:
                    # accurate separation between knots must account for special chars
                    for k in range(8-specialCharCounter): # (9 is number of spaces between knots)
                        s = s+" "
                specialCharCounter = 0 # Reset Special Char Counter
                s = s+knot[2]+"|"+knot[3]+" " # Add knot top halves
                i = i+1 # Move to next location
                if textLocation+i == len(knotList): # stop everything if no knots left
                    break
                # before we get next true knot, let's get rid of all
                # special indicators.
                while knotList[textLocation+i]=="\\STOP" or knotList[textLocation+i] == "\\NEWLINE":
                    s = s+knotList[textLocation+i][0:2]
                    knotList.pop(textLocation+i)
                    specialCharCounter = specialCharCounter+2
                    if textLocation+i==len(knotList):
                        break
        textLocation = textLocation+i
        s=s+"\n\n"
    return s

def formatKnotsColumnsSimple(knotList,optsObj): ## add spacing list arg
    textLocation = 0
    slotLocation = 0
    currentColumn = 0
    blockSize = optsObj.blockSize.get()
    orientation = optsObj.orientation.get()
    spacingList = [ri(0,1) for x in range(len(knotList)*100)]
    s = "KNOT SCORE\n"
    for slot in spacingList:
        if textLocation==len(knotList):
            break;
        # if we are at the start of a new row, create it!
        if slotLocation % blockSize == 0:
            s=s+"\n--- "+orientation[0:-1]+" %03d ---\n" % currentColumn
            currentColumn = currentColumn+1
        # if the slot should have something in it, give it what it has
        if slot == "x" or slot == "1" or slot == 1:
            knot = knotList[textLocation]
            s = s+".".join(knot)
            textLocation = textLocation+1
            if textLocation==len(knotList):
                break;
            while (knotList[textLocation] == "\\STOP" or knotList[textLocation]=="\\NEWLINE"):
                s = s+" "+knotList[textLocation]
                textLocation = textLocation +1
                if textLocation==len(knotList):
                    break;
            s = s+"\n"
        elif slot == " " or slot == "0" or slot == 0:
            s=s+"\n"
        slotLocation = slotLocation+1
    return s

def formatKnotsColumnsPretty(knotList,optsObj): ## add spacing list arg
    textLocation = 0
    slotLocation = 0
    currentColumn = 0
    blockSize = optsObj.blockSize.get()
    orientation = optsObj.orientation.get()
    spacingList = [ri(0,1) for x in range(len(knotList)*100)]
    s = "KNOT SCORE\n"
    for slot in spacingList:
        if textLocation==len(knotList):
            break;
        # if we are at the start of a new row, create it!
        if slotLocation % blockSize == 0:
            s=s+"-----\n"+orientation[0:-1]+" %03d\n" % currentColumn
            currentColumn = currentColumn+1
        # if the slot should have something in it, give it what it has
        if slot == "x" or slot == "1" or slot == 1:
            knot = knotList[textLocation]
            s = s+"-----\n"+knot[0]+"|"+knot[1]+"\n"+knot[2]+"|"+knot[3]
            textLocation = textLocation+1
            if textLocation==len(knotList):
                break;
            while (knotList[textLocation] == "\\STOP" or knotList[textLocation]=="\\NEWLINE"):
                s = s+" "+knotList[textLocation]
                textLocation = textLocation +1
                if textLocation==len(knotList):
                    break;
            s = s+"\n"
        elif slot == " " or slot == "0" or slot == 0:
            s=s+"-----\n\n\n"
        slotLocation = slotLocation+1
    return s

def fileToStr(path):
    text = ""
    with open(path) as lines:
        for line in lines:
            text = text+line
    return text

def generateSpacingList(path):
    spacingList = []
    with open("./texts/spacingMatrix.txt") as lines:
        lineStrings = lines.readlines()
        numOfColumns = len(lineStrings[0])-1
        for column in range(numOfColumns):
            for row in lineStrings:
                try:
                    if row[column] != "\n":
                        spacingList.append(row[column])
                    else:
                        spacingList.append("0")
                except IndexError:
                    spacingList.append("0")
    return spacingList
