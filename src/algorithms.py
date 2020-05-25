#               0  1  2  3  4  5  6  7  8
# board_ex1 = [[3, 0, 6, 5, 0, 8, 4, 0, 0],  # 0
#              [5, 2, 0, 0, 0, 0, 0, 0, 0],  # 1
#              [0, 8, 7, 0, 0, 0, 0, 3, 1],  # 2
#              [0, 0, 3, 0, 1, 0, 0, 8, 0],  # 3
#              [9, 0, 0, 8, 6, 3, 0, 0, 5],  # 4
#              [0, 5, 0, 0, 9, 0, 6, 0, 0],  # 5
#              [1, 3, 0, 0, 0, 0, 2, 5, 0],  # 6
#              [0, 0, 0, 0, 0, 0, 0, 7, 4],  # 7
#              [0, 0, 5, 2, 0, 6, 3, 0, 0]]  # 8

# board_ex1 = [[0 for x in range(9)] for y in range(9)]

import constant as c

#             0  1  2  3  4  5  6  7  8
board_ex1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0],  # 0
             [0, 1, 2, 0, 3, 4, 5, 6, 7],  # 1
             [0, 3, 4, 5, 0, 6, 1, 8, 2],  # 2
             [0, 0, 1, 0, 5, 8, 2, 0, 6],  # 3
             [0, 0, 8, 6, 0, 0, 0, 0, 1],  # 4
             [0, 2, 0, 0, 0, 7, 0, 5, 0],  # 5
             [0, 0, 3, 7, 0, 5, 0, 2, 8],  # 6
             [0, 8, 0, 0, 6, 0, 7, 0, 0],  # 7
             [2, 0, 7, 0, 8, 3, 6, 1, 5]]  # 8



# Trigger backtrack value with dictionary, used with find_prev and find_next
# (row, col) : (value_at_this_position, overwritten(1)/fixed(-1)/writable(0))
backtrack = {}


def init():
    init_backtrack()
    return init_valid_board()


# Init the backtrack BEFORE everything else
def init_backtrack():
    for row in range(9):
        for col in range(9):
            if board_ex1[row][col] == 0:
                backtrack.update({(row, col): [board_ex1[row][col], 0]})
            else:
                backtrack.update({(row, col): [board_ex1[row][col], -1]})


# Must be invoked AFTER init_backtrack()
def init_valid_board():
    for k1 in backtrack.keys():
        for k2 in backtrack.keys():
            if k1 == k2:
                continue
            if backtrack[k1][0] == backtrack[k2][0] != 0:
                if k1[0] == k2[0] or k1[1] == k2[1] or cell_assign(k1) == cell_assign(k2):
                    # print(k1, k2, backtrack[k1][0])
                    return False
    return True


# Return the position of the first assignable cell with it's maximal assignable value
# part of the board solvable question
def find_max():
    value = 0
    if board_ex1[0][0] == 0:
        pos = (0, 0)
    else:
        pos = find_next((0, 0))
    for i in range(9, 0, -1):
        if safe_to_assign(pos, i):
            value = i
            break
    return pos, value


def board_reset():
    for i in range(9):
        for j in range(9):
            board_ex1[i][j] = c.board_const[i][j]
    backtrack.clear()
    init()


# Dumb hardcoded position-assigning
def cell_assign(pos):
    if pos[0] < 3:
        if pos[1] < 3:
            return 0, 0
        elif pos[1] < 6:
            return 0, 3
        else:
            return 0, 6
    elif pos[0] < 6:
        if pos[1] < 3:
            return 3, 0
        elif pos[1] < 6:
            return 3, 3
        else:
            return 3, 6
    else:
        if pos[1] < 3:
            return 6, 0
        elif pos[1] < 6:
            return 6, 3
        else:
            return 6, 6


# Backtrack to the last elem
def find_prev(pos):
    row = pos[0]
    col = pos[1]
    if backtrack[(row, col)][1] == 1:
        return row, col
    if 0 < col < 9:
        col -= 1
    else:
        # Constraint for maximum return
        if row == 0 and col == 0:
            return 0, 0
        # In case of (x, 0)
        row -= 1
        col = 8
    if backtrack[(row, col)][1] == -1:
        return find_prev((row, col))
    return row, col


# Find next cell to fill
def find_next(pos):
    row = pos[0]
    col = pos[1]
    for i in range(9):
        for j in range(9):
            if i > row:
                if board_ex1[i][j] == 0:
                    return i, j
            if i == row and j > col:
                if board_ex1[i][j] == 0:
                    return i, j
    return False


def safe_to_assign(pos, value):
    return not dup_in_row_col(pos, value) and not dup_in_square(pos, value) and value < 10


def dup_in_row_col(pos, value):
    row = pos[0]
    col = pos[1]
    for i in range(9):
        for j in range(9):
            if board_ex1[i][col] == value or board_ex1[row][j] == value:
                return True
    return False


def dup_in_square(pos, value):
    row = pos[0]
    col = pos[1]
    x = cell_assign((row, col))[0]
    y = cell_assign((row, col))[1]
    for i in range(3):
        for j in range(3):
            if board_ex1[i + x][j + y] == value:
                return True
    return False


def solve_one(pos):
    for value in range(backtrack[pos][0] + 1, 10):
        if safe_to_assign(pos, value):
            board_ex1[pos[0]][pos[1]] = value
            backtrack[pos] = [value, 1]
            return value
    else:
        board_ex1[pos[0]][pos[1]] = 0
        backtrack[pos] = [0, 0]
        return 0


def solve_all():
    pos = find_next((0, 0))
    while True:
        tmp = solve_one(pos)
        if tmp != 0:
            if not find_next(pos):
                break
            pos = find_next(pos)
        elif tmp == 0:
            pos = find_prev(pos)
