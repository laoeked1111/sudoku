
import sudoku
import time

def main() -> None:
    """
    Entry point. 
    """
    print("Welcome to the Sudoku Solver!")
    print("Please enter your Sudoku puzzle in the following format:")
    print("Each row should be a string of 9 characters, where '0' represents an empty cell.")
    puzzle = []
    for i in range(9):
        row = input(f"Enter row {i+1}: ").strip()
        puzzle.append([int(digit) for digit in row])
    sudoku.dump_board(puzzle)

    start_time = time.time()
    sudoku.print_solved_sudoku(puzzle)
    end_time = time.time()
    print(f"Solved in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    main()
