
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

# Convert Digit to Knot Quadrant
# TODO: make knots a class to add adjacency and easy access?
def digitToQuadrant(digit):
    digits = ["U_", "UU", "Uu", "UO", "Uo", "O_", "OU", "Ou", "OO", "Oo"]
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
