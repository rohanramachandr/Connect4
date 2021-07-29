import math

succ = [['r', 'r', ' ', ' ', ' '], [' ' , 'b', 'b', ' ', ' '], [' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', 'b', 'b'],
         ['r', 'r','r', ' ', ' ']]

def countColor(color, section):
    count = 0
    for i in section:
        if color == i:
            count = count + 1
    return count

def getScore(color, state):
    if color == 'r':
        opp = 'b'
    if color == 'b':
        opp = 'r'
    score = 0
    #rows
    scores = []
    for i in state:

            if i[1] != opp and i[2] != opp and i[3] != opp:
                scores.append(countColor(color, i))
    #columns
    for i in range(5):
        col = []
        for j in range(5):
            col.append(state[j][i])
        if col[1] != opp and col[2] != opp and col[3] != opp:
                scores.append(countColor(color, col))
    #main diagonal
    diag = []
    for i in range(5):
        diag.append(state[i][i])
    if diag[1] != opp and diag[2] != opp and diag[3] != opp:
        scores.append(countColor(color, diag))
    #upper main diagonal
    diag2 = [state[0][1], state[1][2], state[2][3], state[3][4]]
    if diag2[0] != opp and diag2[1] != opp and diag2[2] != opp and diag2[3] != opp:
        scores.append(countColor(color, diag2))
    #lower main diagonal
    diag3 = [state[1][0], state[2][1], state[3][2], state[4][3]]
    if diag3[0] != opp and diag3[1] != opp and diag3[2] != opp and diag3[3] != opp:
        scores.append(countColor(color, diag3))
    #reverse main diagonal
    diag4 = [state[4][0], state[3][1], state[2][2], state[1][3], state[0][4]]
    if diag4[1] != opp and diag4[2] != opp and diag4[3] != opp:
        scores.append(countColor(color, diag4))
    #upper reverse diagonal
    diag5 = [state[3][0], state[2][1], state[1][2], state[0][3]]
    if diag5[0] != opp and diag5[1] != opp and diag5[2] != opp and diag5[3] != opp:
        scores.append(countColor(color, diag5))
    #lower reverse diagonal
    diag6 = [state[4][1], state[3][2], state[2][3], state[1][4]]
    if diag6[0] != opp and diag6[1] != opp and diag6[2] != opp and diag6[3] != opp:
        scores.append(countColor(color, diag6))
    #squares
    square = []
    for i in range(4):
        for j in range(4):
            square = [state[i][j], state[i][j+1], state[i+1][j], state[i+1][j+1]]
            if square[0] != opp and square[1] != opp and square[2] != opp and square[3] != opp:
                 scores.append(countColor(color, square))
    return max(scores)


def squareCheck(myPieces):
    passed = True
    if distance(myPieces[0], myPieces[1]) + distance(myPieces[0], myPieces[2]) + distance(myPieces[0],
                                                                                              myPieces[3]) != 2 + (
            2 ** (.5)):
        passed = False
    if distance(myPieces[1], myPieces[0]) + distance(myPieces[1], myPieces[2]) + distance(myPieces[1],
                                                                                          myPieces[3]) != 2 + (
            2 ** (.5)):
        passed = False
    if distance(myPieces[2], myPieces[0]) + distance(myPieces[2], myPieces[1]) + distance(myPieces[2],
                                                                                          myPieces[3]) != 2 + (
            2 ** (.5)):
        passed = False
    if distance(myPieces[3], myPieces[0]) + distance(myPieces[3], myPieces[1]) + distance(myPieces[3],
                                                                                          myPieces[2]) != 2 + (
            2 ** (.5)):
        passed = False
    return passed
def distance(loc1, loc2):
    a = math.pow((loc1[0] - loc2[0]), 2)  # calculates and squares difference between TMAX
    b = math.pow((loc1[1] - loc2[1]), 2)  # calculates and squares difference between PRCP
    sum = a + b
    return sum ** (.5)



print(getScore('r', succ))
