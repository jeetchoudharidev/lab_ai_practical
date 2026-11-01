
N = 8

# Each index represents a column.
# Each value represents the row of its queen.
board = [-1] * N


# Check whether a queen can be placed safely
def is_safe(row, col):

    # Check all previously filled columns
    for previous_col in range(col):

        previous_row = board[previous_col]

        # Check same row
        if previous_row == row:
            return False

        # Check diagonal
        if abs(previous_row - row) == abs(previous_col - col):
            return False

    return True


# Backtracking function
def solve(col):

    # Base case: all 8 queens are placed
    if col == N:
        return True

    # Try every row in the current column
    for row in range(N):

        if is_safe(row, col):

            # Place queen
            board[col] = row

            # Recursively solve next column
            if solve(col + 1):
                return True

            # Backtrack: remove queen
            board[col] = -1

    return False


# Print chessboard
def print_board():

    for row in range(N):
        for col in range(N):

            if board[col] == row:
                print("Q", end=" ")
            else:
                print(".", end=" ")

        print()


# Main program
if solve(0):
    print("Solution Found!")
    print_board()
else:
    print("No solution exists.")
