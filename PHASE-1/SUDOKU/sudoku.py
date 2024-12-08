from collections import deque


def print_board(board):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")


def find_empty_location(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None


def is_valid(board, row, col, num):

    for i in range(9):
        if board[row][i] == num:
            return False

    for i in range(9):
        if board[i][col] == num:
            return False

    box_start_row = row - row % 3
    box_start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[box_start_row + i][box_start_col + j] == num:
                return False
    return True


def solve_sudoku_backtracking(board):
    empty_loc = find_empty_location(board)
    if not empty_loc:
        return True

    row, col = empty_loc

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num

            if solve_sudoku_backtracking(board):
                return True

            board[row][col] = 0

    return False


def solve_sudoku_bfs(board):
    q = deque([board])
    step = 0

    while q:
        current_board = q.popleft()
        step += 1

        if step % 1000 == 0:
            print(f"BFS Step: {step}")
            print_board(current_board)
            print("\n")

        empty_loc = find_empty_location(current_board)
        if not empty_loc:
            print(f"Solution found with BFS after {step} steps:")
            print_board(current_board)
            return True

        row, col = empty_loc

        for num in range(1, 10):
            if is_valid(current_board, row, col, num):
                new_board = [row[:] for row in current_board]
                new_board[row][col] = num
                q.append(new_board)

    return False



def generate_board(level):
    boards = {
        "easy": [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ],
        "medium": [
            [0, 0, 0, 0, 0, 7, 0, 0, 0],
            [1, 0, 0, 0, 3, 0, 0, 0, 9],
            [0, 0, 2, 0, 6, 0, 8, 0, 0],
            [0, 0, 0, 6, 0, 0, 0, 7, 0],
            [0, 0, 8, 0, 0, 0, 1, 0, 0],
            [0, 7, 0, 0, 0, 4, 0, 0, 0],
            [0, 0, 3, 0, 8, 0, 9, 0, 0],
            [2, 0, 0, 0, 5, 0, 0, 0, 1],
            [0, 0, 0, 4, 0, 0, 0, 0, 0]
        ],
        "hard": [
            [0, 0, 0, 0, 0, 0, 8, 0, 0],
            [0, 0, 0, 7, 0, 4, 5, 3, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 1, 0, 9, 0, 5, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 6, 0, 1, 0, 8, 0],
            [0, 0, 0, 0, 9, 0, 0, 0, 0],
            [0, 8, 4, 1, 0, 7, 0, 0, 0],
            [0, 0, 7, 0, 0, 0, 0, 0, 0]
        ]
    }

    return boards[level]


def main():
    print("Choose Sudoku level: ")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")

    level_choice = input("Your choice (1/2/3): ")
    if level_choice == '1':
        board = generate_board("easy")
    elif level_choice == '2':
        board = generate_board("medium")
    elif level_choice == '3':
        board = generate_board("hard")
    else:
        print("Invalid choice!")
        return

    print("\nSudoku board before solving:")
    print_board(board)

    print("\nChoose the algorithm to solve Sudoku: ")
    print("1. Backtracking")
    print("2. BFS")

    algo_choice = input("Your choice (1/2): ")
    if algo_choice == '1':
        if solve_sudoku_backtracking(board):
            print("\nSolution found using Backtracking:")
            print_board(board)
        else:
            print("Cannot be solved using Backtracking!")
    elif algo_choice == '2':
        if not solve_sudoku_bfs(board):
            print("Cannot be solved using BFS!")
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
