"""
Tic Tac Toe Player
"""

import math
import copy

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
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)

    # X always goes first
    return X if x_count <= o_count else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    actions = set()
    for i, row in enumerate(board):
        for j, column in enumerate(row):
            if column == EMPTY:
                actions.add((i, j))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action  # Unpack the action

    # Validate the action
    # Check if indices are out of bounds
    if not (0 <= i < len(board)) or not (0 <= j < len(board[i])):
        raise Exception("Invalid move: Out-of-bounds action.")
    if board[i][j] != EMPTY:  # Check if the cell is already occupied
        raise Exception("Invalid move: Cell is already occupied.")

    # Make a deep copy of the board
    new_board = copy.deepcopy(board)

    # Determine the current player
    current_player = player(board)

    # Apply the move
    new_board[i][j] = current_player

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    b = board
    winner = None

    for i in range(len(b)):
        # Check the digonals
        if (
            i == 0  # This makes sure we are on the diagonals
            and
            (b[i][i] == b[i+1][i+1] == b[i+2][i+2]
             or
             b[i][i+2] == b[i+1][i+1] == b[i+2][i])):
            if b[i+1][i+1] == X:
                winner = X
                break
            elif b[i+1][i+1] == O:
                winner = O
                break

        # Check the rows and columns if it was not on diagonals
        if (  # Check for X
            b[i][0] == b[i][1] == b[i][2] == X
            or
                b[0][i] == b[1][i] == b[2][i] == X):
            winner = X
            break
        elif (  # Check for O
            b[i][0] == b[i][1] == b[i][2] == O
            or
                b[0][i] == b[1][i] == b[2][i] == O):
            winner = O
            break
    return winner


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If there was a winner
    #
    if winner(board) != None:
        return True

    # If there was no winner but there are possible actions left
    if not actions(board):
        return True

    # If none of the above is True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def minimax(board, return_action=True):
    """
    Returns the optimal action for the current player on the board.
    If `return_action` is True, the function returns the best action.
    Otherwise, it returns the utility value of the board.
    """
    # Base case: If the game is over, return utility or None
    if terminal(board):
        return None if return_action else utility(board)

    current_player = player(board)
    best_action = None

    if current_player == X:  # Maximizing player
        best_value = -math.inf
        for action in actions(board):
            resulting_board = result(board, action)
            value = minimax(resulting_board, return_action=False)  # Recursively get utility
            if value > best_value:
                best_value = value
                best_action = action
    else:  # Minimizing player
        best_value = math.inf
        for action in actions(board):
            resulting_board = result(board, action)
            value = minimax(resulting_board, return_action=False)  # Recursively get utility
            if value < best_value:
                best_value = value
                best_action = action

    # Return the best action (at top level) or the utility value (during recursion)
    return best_action if return_action else best_value
