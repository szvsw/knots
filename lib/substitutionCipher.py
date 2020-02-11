
# Replace each word in list with its numerical ID.
def substitutionCipher(plaintext,cipher):
    crypttext=[]
    x=0
    for word in plaintext:
        dictEntry = cipher[word]
        id = dictEntry['id']
        crypttext.append(id)
        x=x+1
    return crypttext

# Convert digit to knotGUI
# To do - make knots a class to add adjacency and easy access?
def digitToQuadrant(digit):
    digits = ["U_", "UU", "Uu", "UO", "Uo", "O_", "OU", "Ou", "OO", "Oo"]
    quadrant = digits[digit]
    return quadrant

def intToKnot(integer):
    digits = [0,0,0,0]
    knots = []
    for i in range(4):
        digits[i] = integer // 10**i % 10
        knots.append(digitToQuadrant(digits[i]))

    return knots

def formatInts(integerList):
    s = ""
    for i in integerList:
        s = s+str(i)+"."
    s = s[0:len(s)-1] ## truncate last character
    return s

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
        for quadrant in knot: # Iterate over quadrants
            word=word+quadrant+"."
        word = word[0:len(word)-1]
        s=s+word+"\n"
        wordCount = wordCount + 1
    return s
