# Author: Nimish Mishra
# Email: nmishra36@gatech.edu

import random


# Solves passed in sudoku board
# Params: board: 2d list of ints representing the board
# Return: if board is solved or not
def solve(old_board, flag=False):

    # This flag determines if the original board is to be modified or not
    if flag:
        board = old_board
    else:
        board = list(old_board)

    # Finds the first empty element in the board
    # Returns true if no empty elements found
    pos = find_empty_element(board)
    if not pos:
        return True

    row = pos[0]
    col = pos[1]

    for i in range(1, 10):
        if valid(row, col, i, board):
            # Plugs in first valid move
            board[row][col] = i

            # Recursive statement to continue filling in board
            if solve(board):
                return True

            # If line is reached, current move is not valid and is undone
            board[row][col] = 0

    # Reached if no moves are valid for current index and board
    return False


# Checks if passed in move is valid
# Params: x, y: ints representing the location, num: number to be put in said location, board: 2d list of ints
# Return: True if move is valid, False otherwise
def valid(x, y, num, board):
    # Used to validate the 3x3 square the index is in
    square_x = int(x / 3)
    square_y = int(y / 3)

    for i in range(0, 9):
        if num == board[x][i] or num == board[i][y] \
                or num == board[int(i / 3) + (square_x * 3)][(i % 3) + (square_y * 3)]:
            return False

    return True


# Prints out the board passed in
# Params: board: 2d list of ints representing the board
# Return: None
def print_board(board):
    for x in board:
        print(x)


# Checks to see if a given sudoku board is a valid solution
# Params: board: 2d list of ints representing the board
# Return: True if board is valid, False otherwise
def validate_board(board):
    holder_board = board
    for i in range(0, 9):
        for j in range(0, 9):
            num = holder_board[i][j]
            holder_board[i][j] = 0
            if valid(i, j, num, board):
                holder_board[i][j] = num
            else:
                return False
    return True


# Finds the first empty element in the board
# Params: board: 2d list of ints representing the board
# Return: list of 2 elements containing the x coordinate and y coordinate
def find_empty_element(board):
    for i in range(0, 9):
        for j in range(0, 9):
            if board[i][j] == 0:
                return [i, j]
    return None


# Generates a random board given an empty 2d list
# Params: new_board: empty 2d list
# Returns: True if board is filled properly, False otherwise
def gen_random_filled_board(new_board):
    pos = find_empty_element(new_board)
    if not pos:
        return True

    row = pos[0]
    col = pos[1]

    nums = [i for i in range(1, 10)]
    for i in range(1, 10):
        val = nums[random.randint(0, len(nums) - 1)]
        if valid(row, col, val, new_board):
            # Plugs in first valid random number
            new_board[row][col] = val

            # Recursive statement to continue filling in board
            if gen_random_filled_board(new_board):
                return True

            # If line is reached, current number is not valid and is undone
            new_board[row][col] = 0

        # Removing current value from list of possible values if this line is reached
        nums.remove(val)

    # Reached if no numbers are valid for current board
    return False


# Removes a passed in number of elements from the board to generate a playable sudoku board
# Params: board: 2d list of ints representing the board, elements: num of elements to be removed
# Return: None
def remove_elements(board, elements):
    i = 0
    while i < elements:
        pos = random.randint(0, 80)
        xcoord = int(pos / 9)
        ycoord = pos % 9

        if board[xcoord][ycoord] != 0:
            board[xcoord][ycoord] = 0
            i = i + 1
    return board


# Uses above two methods to generate a new, random, playable sudoku board
# Params: board: 2d list of ints representing the board, elements: num of elements to be removed
# Return: None
def get_new_board(elements):
    zero_board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    gen_random_filled_board(zero_board)
    remove_elements(zero_board, elements)
    return zero_board
