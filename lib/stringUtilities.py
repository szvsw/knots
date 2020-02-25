# Pretty Printing Function
def formatInts(integerList,optsObj):
    s = ""
    delimiterL = ""
    delimiterC = ""
    delimiterR = ""
    formatter = "{:01d}"
    if len(optsObj.delimiter.get())==1 or optsObj.delimiter.get() == "<space>":
        delimiterC = optsObj.delimiter.get()
    elif optsObj.delimiter.get() == "None (Padded)" or optsObj.padding.get() == "Padded":
        formatter = "{:04d}"
    if len(optsObj.delimiter.get())==2:
        delimiterL = optsObj.delimiter.get()[0]
        delimiterR = optsObj.delimiter.get()[1]
    for i in integerList:
        s = s+delimiterL+formatter.format(i)+delimiterR+delimiterC
    if delimiterC != "":
        s = s[0:len(s)-1] # truncate last character - get rid of this when using s formatting

    return s

# Pretty Printing Function
def formatKnotsSimple(knotList,optsObj):
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

def formatKnotsPretty(knotList,optsObj):
    rowSize = optsObj.blockSize.get()
    orientation = optsObj.orientation.get()
    currentRow = 0
    s = "KNOT SCORE\n"
    while currentRow*rowSize < len(knotList):
        knotRow = knotList[currentRow*rowSize:(currentRow*rowSize+rowSize)]
        s=s+"\n--- "+orientation[0:-1]+" %03d ---\n" % currentRow
        if orientation == "Rows": s = s+"\n"
        # Column Labeling
        for i in range(1,rowSize*2+1):
            if ((i%2 != 0 and currentRow%2 ==0) or (i%2==0 and currentRow%2!=0)) and orientation == "Rows": s=s+"COL"+"{:02d}".format(i)+"  "
            elif ((i%2!=0 and currentRow%2 !=0) or (i%2==0 and currentRow%2==0)) and orientation == "Rows": s = s+"       "

        s=s+"\n"
        # Offset
        if (currentRow%2)!=0 and orientation == "Rows": s = s+"       "
        # Top Halves
        for knot in knotRow: s = s+knot[0]+"|"+knot[1]+"         "
        s = s+"\n"
        # Offset
        if (currentRow%2)!=0 and orientation == "Rows": s = s+"       "
        # Bottom Halves
        for knot in knotRow: s = s+knot[2]+"|"+knot[3]+"         "
        s=s+"\n"
        currentRow = currentRow + 1
    return s

def fileToStr(path):
    text = ""
    with open(path) as lines:
        for line in lines:
            text = text+line
    return text
