"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None
#Num_Turns = 0


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    search board for which has less x or o
    num_Turns += 1
    if num_Turns % 2 == 1:
        return X
    else:
        return O
    """
    num_X = 0
    num_O = 0
    for row in board:
        for i in row:
            if i == X:
                num_X += 1
            elif i == O:
                num_O += 1
    if num_O > num_X:
        return O
    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    search for where board = empyty
    """
    set_Of_Possible_Values = []
    for i in range(len(board)):
            for j in range(len(board[i])):     
                if board[i][j] == EMPTY:
                    tuple = (i,j)
                    set_Of_Possible_Values.append(tuple)
    return set_Of_Possible_Values


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    find action if not allowed raise exection return updated board state
    """
    if board[action[0]][action[1]] != EMPTY:
        raise Exception("Not Valid Move")
    
    tempBoard = board
    turn = player(tempBoard)

    tempBoard[action[0]][action[1]] = turn
    
    return tempBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    search for winner brainstorm best way can check every spot and search for three in a row but 
    seems inefficent
    """
    """
    winning combinatinos 
    rows:
    board[0][0],board[0][1],board[0][2]
    board[1][0],board[1][1],board[1][2]
    board[2][0],board[2][1],board[2][2]

    columns
    board[0][0],board[1][0],board[2][0]
    board[0][1],board[1][1],board[2][1]
    board[0][2],board[1][2],board[2][2]

    diags
    board[0][0],board[1][1],board[2][2]
    board[0][2],board[1][1],board[2][0]
    """

    combos = [
              (board[0][0],board[0][1],board[0][2]),
              (board[1][0],board[1][1],board[1][2]),
              (board[2][0],board[2][1],board[2][2]),
              (board[0][0],board[1][0],board[2][0]),
              (board[0][1],board[1][1],board[2][1]),
              (board[0][2],board[1][2],board[2][2]),
              (board[0][0],board[1][1],board[2][2]),
              (board[0][2],board[1][1],board[2][0])
              ]
    for i in combos:
        if i[0] == i[1] == i[2] != EMPTY:
            return i[0]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    call winner if not none check if all full
    """
    if (winner(board) != None):
        return True
    for row in range(len(board)):
        for column in range(len(row)):
            if board[row][column] == EMPTY:
                return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    use winner if returns x = 1 etc.
    """
    winner = winner(board)
    if winner == X:
        return 1
    elif winner == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    x = max
    0 = min
    function MAX-VALUE(state):
        if TERMINAL(state):
        return UTILITY(state)
        v = -∞
        for action in ACTIONS(state):
        v = MAX(v, MIN-VALUE(RESULT(state, action)))
        return v
    function MIN-VALUE(state):
        if TERMINAL(state):
        return UTILITY(state)
        v = ∞
        for action in ACTIONS(state):
        v = MIN(v, MAX-VALUE(RESULT(state, action)))
        return v
    """
    raise NotImplementedError
