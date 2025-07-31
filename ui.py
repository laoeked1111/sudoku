
import tkinter as tk

def disp_board_window(canonical: list[list[int]]) -> None:
    """
    Draw the sudoku board in a tkinter window given a canonical representation.    
    """

    SIDE_LENGTH = 40
    
    root = tk.Tk()
    root.title("Sudoku")

    canvas = tk.Canvas(root, width=9*SIDE_LENGTH, height=9*SIDE_LENGTH)
    canvas.pack()
    for row in range(9):
        for col in range(9):
            x1 = col * SIDE_LENGTH
            x2 = x1 + SIDE_LENGTH
            y1 = row * SIDE_LENGTH
            y2 = y1 + SIDE_LENGTH
            canvas.create_rectangle(x1, y1, x2, y2, outline="grey", fill="white")

            if canonical[row][col] != 0:
                num_x = (x1 + x2) // 2
                num_y = (y1 + y2) // 2
                canvas.create_text(num_x, num_y, text=canonical[row][col], font=("Arial", 12))

    for row in range(3):
        for col in range(3):
            x1 = 3 * col * SIDE_LENGTH
            x2 = x1 + 3 * SIDE_LENGTH
            y1 = 3 * row * SIDE_LENGTH
            y2 = y1 + 3 * SIDE_LENGTH
            canvas.create_rectangle(x1, y1, x2, y2, outline="black")
    
    root.mainloop()
