def is_safe(num, row, col, used_rows, used_cols):
    return not used_rows[row][num] and not used_cols[col][num]

def backtrack(matrix, n, cell_index, max_depth, used_rows, used_cols, empty_cells):
    if cell_index == len(empty_cells):  
        return True

    if cell_index >= max_depth:  
        return False

    row, col = empty_cells[cell_index]

    for num in range(1, n + 1):
        if is_safe(num, row, col, used_rows, used_cols):
            matrix[row][col] = num
            used_rows[row][num] = True
            used_cols[col][num] = True

            if backtrack(matrix, n, cell_index + 1, max_depth, used_rows, used_cols, empty_cells):
                return True

            # Undo the placement
            matrix[row][col] = 0
            used_rows[row][num] = False
            used_cols[col][num] = False

    return False

def iddfs_latin_square(n):
    print("\nStarting the Latin Square Solver...")
    matrix = [[0] * n for _ in range(n)]
    used_rows = [[False] * (n + 1) for _ in range(n)]
    used_cols = [[False] * (n + 1) for _ in range(n)]
    empty_cells = [(row, col) for row in range(n) for col in range(n)]

    # Pre-fill diagonals for better efficiency
    for i in range(n):
        matrix[i][i] = i + 1
        used_rows[i][i + 1] = True
        used_cols[i][i + 1] = True
        empty_cells.remove((i, i))

    for max_depth in range(1, len(empty_cells) + 1):
        print(f"--- Trying with max depth: {max_depth} ---")
        if backtrack(matrix, n, 0, max_depth, used_rows, used_cols, empty_cells):
            print_matrix(matrix)
            return

    print("\nNo solution exists for the given Latin square size with IDDFS.")

def print_matrix(matrix):
    print("\nFinal Solution:")
    for row in matrix:
        print(" ".join(map(str, row)))

def main():
    print("A Latin square of size n is an n×n grid where each number from 1 to n appears exactly once in every row and column.")
    
    while True:
        try:
            square_number = int(input("\nEnter the order of the Latin square (n, e.g., 3 or 4): "))
            if square_number <= 0:
                raise ValueError("The size must be a positive integer greater than 0.")
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")
            continue

        iddfs_latin_square(square_number)

        # Ask if the user wants to solve another square
        try_again = input("\nSolve another Latin square? (y/n): ").strip().lower()
        if try_again not in ["yes", "y"]:
            print("\nExiting!!")
            break

if __name__ == "__main__":
    main()
