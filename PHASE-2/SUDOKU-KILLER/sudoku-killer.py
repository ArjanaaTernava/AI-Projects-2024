class Cage:
    def __init__(self, sum_value):
        self.cells = []
        self.sum = sum_value

def is_cell_in_cage(cage, row, col):
    return any(cell[0] == row and cell[1] == col for cell in cage.cells)

def is_valid(board, row, col, num, cages):
    GRID_SIZE = 9

    for i in range(GRID_SIZE):
        if board[row][i] == num or board[i][col] == num:
            return False

    box_row_start = (row // 3) * 3
    box_col_start = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[box_row_start + i][box_col_start + j] == num:
                return False

    for cage in cages:
        if is_cell_in_cage(cage, row, col):
            current_sum = num
            empty_cells = 0

            for r, c in cage.cells:
                if board[r][c] != 0:
                    current_sum += board[r][c]
                elif (r, c) != (row, col):
                    empty_cells += 1

            if current_sum > cage.sum or (empty_cells == 0 and current_sum != cage.sum):
                return False

    return True

def solve(board, cages):
    GRID_SIZE = 9
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == 0:
                for num in range(1, GRID_SIZE + 1):
                    if is_valid(board, row, col, num, cages):
                        board[row][col] = num

                        if solve(board, cages):
                            return True

                        board[row][col] = 0
                return False
    return True

def print_board(board):
    for row in board:
        print(" ".join(map(str, row)))

board = [[0] * 9 for _ in range(9)]

cages = []

cage1 = Cage(10)
cage1.cells.extend([(0, 0), (0, 1)])
cages.append(cage1)

cage2 = Cage(7)
cage2.cells.extend([(1, 0), (1, 1)])
cages.append(cage2)

cage3 = Cage(15)
cage3.cells.extend([(0, 2), (0, 3), (1, 3)])
cages.append(cage3)

cage4 = Cage(6)
cage4.cells.extend([(1, 2), (2, 2)])
cages.append(cage4)

cage5 = Cage(20)
cage5.cells.extend([(2, 0), (2, 1), (3, 1)])
cages.append(cage5)

cage6 = Cage(14)
cage6.cells.extend([(0, 4), (0, 5), (1, 4)])
cages.append(cage6)

cage7 = Cage(9)
cage7.cells.extend([(1, 5), (2, 5)])
cages.append(cage7)

cage8 = Cage(12)
cage8.cells.extend([(3, 0), (4, 0), (4, 1)])
cages.append(cage8)

cage9 = Cage(8)
cage9.cells.extend([(2, 3), (3, 2)])
cages.append(cage9)

cage10 = Cage(5)
cage10.cells.extend([(3, 3), (3, 4)])
cages.append(cage10)

cage11 = Cage(17)
cage11.cells.extend([(4, 2), (4, 3), (4, 4)])
cages.append(cage11)


if solve(board, cages):
    print("Zgjidhja e Sudoku:")
    print_board(board)
else:
    print("Nuk ekziston asnjë zgjidhje.")