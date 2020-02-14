# Pretty Printing Function
def formatInts(integerList):
    s = ""
    for i in integerList:
        s = s+str(i)+"."
    s = s[0:len(s)-1] ## truncate last character
    return s

# Pretty Printing Function
def formatKnotsSimple(knotList,rowSize):
    currentRow = 0
    s = "KNOT SCORE\n"
    while currentRow*rowSize < len(knotList): # stop when no knots remain
        knotRow = knotList[currentRow*rowSize:(currentRow*rowSize+rowSize)] # get rows worth of knots
        s = s+"\n--- ROW %03d ---\n" % currentRow

        knotRow = "\n".join([*map(lambda x: ".".join(x),knotRow)])
        s=s+knotRow+"\n"

        currentRow = currentRow+1
    return s

def formatKnotsPretty(knotList,rowSize):
    currentRow = 0
    s = "KNOT SCORE\n"
    while currentRow*rowSize < len(knotList):
        knotRow = knotList[currentRow*rowSize:(currentRow*rowSize+rowSize)]
        s=s+"\n--- ROW %03d ---\n" % currentRow
        for knot in knotRow:
            s = s+knot[0]+"|"+knot[1]+"  "
        s = s+"\n"
        for knot in knotRow:
            s = s+knot[2]+"|"+knot[3]+"  "
        s=s+"\n"
        currentRow = currentRow + 1
    return s

def fileToStr(path):
    text = ""
    with open(path) as lines:
        for line in lines:
            text = text+line
    return text
