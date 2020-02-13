
# Replace each word in list with its numerical ID.
def substitutionCipher(plaintext,dict):
    ciphertext=[]
    for word in plaintext:
        dictEntry = dict[word]
        id = dictEntry['id']
        ciphertext.append(id)
    return ciphertext

def otpCipher(plaintext,keytext,modulus):
    # TODO: combine substitution of plaintext and keytext with this function
    newText = []
    for i in range(0,len(plaintext)):
        pad = 0
        if (i<len(keytext)):
            pad = keytext[i]
        newnum = (plaintext[i]+pad) % modulus
        newText.append(newnum)
    return newText


# Convert Digit to Knot Quadrant
# TODO: make knots a class to add adjacency and easy access?
def digitToQuadrant(digit):
    digits = ["U ", "UU", "Uu", "UO", "Uo", "O ", "OU", "Ou", "OO", "Oo"]
    quadrant = digits[digit]
    return quadrant

# Convert Integer to Knot
def intToKnot(integer):
    digits = [0,0,0,0]
    knots = []
    for i in range(4):
        digits[i] = integer // 10**i % 10 # digit separator
        knots.append(digitToQuadrant(digits[i]))
    return knots
