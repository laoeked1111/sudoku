
import sudoku

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
    sudoku.print_solved_sudoku(puzzle)

if __name__ == "__main__":
    main()
