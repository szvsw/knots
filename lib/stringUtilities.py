# Pretty Printing Function
def formatInts(integerList):
    s = ""
    for i in integerList:
        s = s+str(i)+"."
    s = s[0:len(s)-1] ## truncate last character
    return s

# Pretty Printing Function
def formatKnots(knotList,rowSize):
    wordCount = rowSize
    currentRow = 0
    s = "KNOT SCORE\n"
    for knot in knotList: # Iterate over knots
        if wordCount == rowSize: # Break on row size
            wordCount = 0
            currentRow = currentRow+1
            s = s+"\n--- ROW %03d ---\n" % currentRow
        word = ""
        for quadrant in knot: # Iterate over quadrants of knot
            word=word+quadrant+"."
        word = word[0:len(word)-1]
        s=s+word+"\n"
        wordCount = wordCount + 1
    return s

def fileToStr(path):
    text = ""
    with open(path) as lines:
        for line in lines:
            text = text+line
    return text
