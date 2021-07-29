#Rohan's CS540 P6 GameAI
import random
import math
class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.
            
        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.
                
                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).
        
        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """
        
        drop_phase = self.checkDropPhase()   # TODO: detect drop phase
        move = []
        if not drop_phase:
            #print("NOT IN DROP PHASE")
            #print(succ(self, self.board))

            new1, old1 = findNextMove(state, Max_Value(self, state, 0)[1])
            #self.place_piece([(new1[0], new1[1]), (old1[0], old1[1])], self.my_piece)
            move = [(new1[0], new1[1]), (old1[0], old1[1])]
            # TODO: choose a piece to move and remove it from the board
            # (You may move this condition anywhere, just be sure to handle it)
            #
            # Until this part is implemented and the move list is updated
            # accordingly, the AI will not follow the rules after the drop phase!
            pass

        # select an unoccupied space randomly
        # TODO: implement a minimax algorithm to play better



        # ensure the destination (row,col) tuple is at the beginning of the move list

        if drop_phase:
            next =  Max_Value(self, state, 0)[1]
            if next == None:
                return None

            new2, old2 = findNextMove(state, next)
            move = [(new2[0], new2[1])]
        return move



    def checkDropPhase(self):
        if piece_count >= 8:
            return False
        return True



    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                raise Exception("You don't have a piece there!")
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)
        
    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece
        
        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
                
                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece
        
    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition
        
        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and 2x2 box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # TODO: check \ diagonal wins
        for d in range(2):
                if state[d][d] != ' ' and state[d][d] == state[d+1][d+1] == state[d+2][d+2] == state[d + 3][d+3]:
                    return 1 if state[d][d] == self.my_piece else -1
        if state[0][1] != ' ' and state[0][1] == state[1][2] == state[2][3] == state[3][4]:
            return 1 if state[0][1] == self.my_piece else -1
        if state[1][0] != ' ' and state[1][0] == state[2][1] == state[3][2] == state[4][3]:
            return 1 if state[1][0] == self.my_piece else -1

        # TODO: check / diagonal wins
        for d in range(2):
            if state[d][4 - d] != ' ' and state[d][4 - d] == state[d + 1][4 - (d + 1)] == state[d + 2][4 - (d + 2)] == \
                    state[d + 3][4 - (d + 3)]:
                return 1 if state[d][4 - d] == self.my_piece else -1
        if state[3][0] != ' ' and state[3][0] == state[2][1] == state[1][2] == state[0][3]:
            return 1 if state[3][0] == self.my_piece else -1
        if state[4][1] != ' ' and state[4][1] == state[3][2] == state[2][3] == state[1][4]:
            return 1 if state[4][1] == self.my_piece else -1
        # TODO: check 2x2 box wins
        myPieces = []
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == self.my_piece:
                    myPieces.append([i, j])
        if len(myPieces) == 4 and squareCheck(myPieces):
            return 1
        myPieces2 = []
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == self.opp:
                    myPieces2.append([i, j])
        if len(myPieces2) == 4 and squareCheck(myPieces2):
            return -1

        return 0 # no winner yet
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



def findNextMove(curr,succ):
    new = []
    old = []
    for i in range(len(curr)):
        for j in range(len(curr[i])):
            if curr[i][j] != succ[i][j] and succ[i][j] != ' ':# detects piece shift
                new = [i,j]
            if curr[i][j] != succ[i][j] and succ[i][j] == ' ':# detect old piece shift
                old = [i,j]
    return new, old

def Max_Value(self, state, depth):  # first call will be Max_Value(curr_state, 0)
    game = self.game_value(state)
    if (game == 1 or game == -1):
        return [game, state]
    elif depth > 2:
        game = heuristic_game_value(self, state)
        return [game, state]
    else:
        a = [-1000, None]
        succs = succ(self, state)
        for s in succs:
            trial = Min_Value(self, s, depth + 1)
            if trial[0] > a[0]:
                a = trial

    return a

def Min_Value(self, state, depth):
    game = self.game_value(state)
    if (game == 1 or game == -1):
        return [game, state]
    elif (depth > 2):
        game = heuristic_game_value(self, state)
        return [game, state]
    else:
        b = [1000, state]
        succs = succ(self, state)
        for s in succs:
            trial = Max_Value(self,s, depth + 1)
            if trial[0] < b[0]:
                b = trial
    return b


def heuristic_game_value(self, state):
    checkTerminal = self.game_value(state)
    if checkTerminal == 0:
        myScore = getScore(self.my_piece, state)
        oppScore = getScore(self.opp, state)

        if myScore > oppScore:
            return float(myScore)/float(67)
        elif myScore == oppScore:
            return 0
        else:
            return float(-1 *oppScore)/float(67)

    return checkTerminal

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


# returns the Euclidean distance between two dictionary data points from the data set
def distance(loc1, loc2):
    a = math.pow((loc1[0] - loc2[0]), 2)  # calculates and squares difference between TMAX
    b = math.pow((loc1[1] - loc2[1]), 2)  # calculates and squares difference between PRCP
    sum = a + b
    return sum ** (.5)  # returns the square root of the sum

def resetBoard(board1):
    k = len(board1)
    copy = [[0 for x in range(k)] for y in range(k)]
    for i in range(k):
        for j in range(k):
            copy[i][j] = board1[i][j]
    return copy

def removeDuplicates(successors):
    singles = []
    for i in successors:
        if i not in singles:
            singles.append(i)
    return singles

def succ(self, state):
    count = 0
    cp = resetBoard(state)
    succ = []
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] != ' ':
                count = count + 1
    if count < 8:  # drop phase
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == ' ':
                    cp[i][j] = self.my_piece
                    succ.append((cp))
                    cp = resetBoard(state)
    else: # not in drop phase
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == self.my_piece:
                    if i - 1 >= 0 and state[i - 1][j] == ' ':# check left
                        cp[i][j] = ' '
                        cp[i - 1][j] = self.my_piece
                        succ.append(cp)
                        cp = resetBoard(state)
                    if i + 1 < len(state) and state[i + 1][j] == ' ':# check right
                        cp[i][j] = ' '
                        cp[i + 1][j] = self.my_piece
                        succ.append(cp)
                        cp = resetBoard(state)
                    if j + 1 < len(state[i])  and state[i][j + 1] == ' ':# check top
                        cp[i][j] = ' '
                        cp[i][j + 1] = self.my_piece
                        succ.append(cp)
                        cp = resetBoard(state)
                    if j - 1 >= 0 and state[i][j - 1] == ' ':# check bottom
                        cp[i][j] = ' '
                        cp[i][j - 1] = self.my_piece
                        succ.append(cp)
                        cp = resetBoard(state)
                    if j + 1 < len(state[i]) and i - 1 >= 0 and state[i - 1][j + 1] == ' ':# check top left diagonal
                        cp[i][j] = ' '
                        cp[i - 1][j + 1] = self.my_piece
                        succ.append(cp)
                        cp = resetBoard(state)
                    if  j + 1 < len(state[i]) and i + 1 < len(state) and state[i + 1][j + 1] == ' ':# check top right diagonal
                        cp[i][j] = ' '
                        cp[i + 1][j + 1] = self.my_piece
                        succ.append(cp)
                        cp = resetBoard(state)
                    if i - 1 >= 0 and j - 1 >= 0 and state[i - 1][j - 1] == ' ':# check bottom left diagonal
                        cp[i][j] = ' '
                        cp[i - 1][j - 1] = self.my_piece
                        succ.append(cp)
                        cp = resetBoard(state)
                    if i + 1 < len(state) and j - 1 >= 0 and state[i + 1][j - 1] == ' ':# check bottom right diagonal
                        cp[i][j] = ' '
                        cp[i + 1][j - 1] = self.my_piece
                        succ.append(cp)
                        cp = resetBoard(state)

    return removeDuplicates(succ)


############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################

ai = TeekoPlayer()
piece_count = 0
turn = 0

# drop phase
while piece_count < 8 and ai.game_value(ai.board) == 0:

    # get the player or AI's move
    if ai.my_piece == ai.pieces[turn]:
        ai.print_board()
        #print(succ(ai, ai.board))
        move = ai.make_move(ai.board)
        ai.place_piece(move, ai.my_piece)
        print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
    else:
        move_made = False
        ai.print_board()
        print(ai.opp+"'s turn")
        while not move_made:
            player_move = input("Move (e.g. B3): ")
            while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                player_move = input("Move (e.g. B3): ")
            try:
                ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                move_made = True
            except Exception as e:
                print(e)

    # update the game variables
    piece_count += 1
    turn += 1
    turn %= 2

# move phase - can't have a winner until all 8 pieces are on the board
while ai.game_value(ai.board) == 0:
    print(ai.game_value(ai.board))
    # get the player or AI's move
    if ai.my_piece == ai.pieces[turn]:
        ai.print_board()
        move = ai.make_move(ai.board)
        ai.place_piece(move, ai.my_piece)
        print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
        print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
    else:
        move_made = False
        ai.print_board()
        print(ai.opp+"'s turn")
        while not move_made:
            move_from = input("Move from (e.g. B3): ")
            while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                move_from = input("Move from (e.g. B3): ")
            move_to = input("Move to (e.g. B3): ")
            while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                move_to = input("Move to (e.g. B3): ")
            try:
                ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                 (int(move_from[1]), ord(move_from[0])-ord("A"))])
                move_made = True
            except Exception as e:
                print(e)

    # update the game variables
    turn += 1
    turn %= 2

ai.print_board()
if ai.game_value(ai.board) == 1:
    print("AI wins! Game over.")
else:
    print("You win! Game over.")
