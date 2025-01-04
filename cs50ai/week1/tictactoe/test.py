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
    x_count = 0
    o_count = 0

    # If the game is starting x starts
    if board == initial_state():
        turn = X
    # Else, count the x and o on the board
    else:
        for row in board:
            for cell in row:
                if cell == X:
                    x_count += 1
                elif cell == O:
                    o_count += 1
    # Since x always starts, its count will always be more than or equal to o 
    if x_count > o_count:
        turn = O
    else:
        turn = X
                
    return turn

b1 = [[EMPTY, EMPTY, EMPTY],
      [EMPTY, EMPTY, EMPTY],
      [EMPTY, EMPTY, EMPTY]]

b2 = [[EMPTY,  X  ,EMPTY],
      [EMPTY,EMPTY,EMPTY],
      [EMPTY,EMPTY,EMPTY]]

b3 = [[EMPTY,EMPTY,EMPTY],
      [EMPTY,  X  ,  O  ],
      [EMPTY,EMPTY,EMPTY]]

b4 = [[  X  ,  O  ,EMPTY],
      [EMPTY,  X  ,  O  ],
      [  X  ,EMPTY,EMPTY]]

b5 = [[EMPTY,  X  ,EMPTY],
      [EMPTY,  X  ,  O  ],
      [EMPTY,EMPTY,  O  ]]

b6 = [[  O  ,  X  ,  O  ],
      [  X  ,  X  ,  O  ],
      [  O  ,EMPTY,EMPTY]]

scenario = [b1, b2, b3, b4, b5, b6]


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i, row in enumerate(board):
        for j, column in enumerate(row):
            if column == EMPTY:
                actions.add((i,j))
    

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action  # Unpack the action

    # Validate the action
    if board[i][j] != EMPTY:
        raise Exception("Invalid move: Cell is already occupied.")

    # Make a deep copy of the board
    new_board = copy.deepcopy(board)

    # Determine the current player
    current_player = player(board)  # Use the original board for this

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
            i == 0 # This makes sure we are on the diagonals
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
        if ( # Check for X
            b[i][0] == b[i][1] == b[i][2] == X
            or
            b[0][i] == b[1][i] == b[2][i] == X):
            winner = X
            break
        elif ( # Check for O
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
        return  -1
    else:
        return 0

#####################################################################
#Scenarios
#####################################################################
for i, b in enumerate(scenario):
    print(f"Scenario {i}")
    print("Board:", b)
    print("*" * 20)
    p = player(b)
    print("Player:", p)
    print("*" * 20)
    action_list = actions(b)
    print("Actions:", action_list)
    print("*" * 20)
    r = result(b, (2,1))
    print("New board:", r)
    print("*" * 20)
    w = winner(r)
    print("Winner:", w)
    print("#" * 100)


        
