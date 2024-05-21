"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


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
    """
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    search for where board = empyty
    """
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    find action if not allowed raise exection return updated board state
    """
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    search for winner brainstorm best way can check every spot and search for three in a row but 
    seems inefficent
    """
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    call winner if not none check if all full
    """
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    use winner if returns x = 1 etc.
    """
    raise NotImplementedError


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
