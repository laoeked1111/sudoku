
"""
This module provides a sudoku SAT solver for finding one solution to a given sudoku puzzle.
"""

# The canonical representation of the sudoku game board is a list of lists
# representing each row in the board. Each entry is 0 if blank and the
# number if a number is known to be filled in.


def dump_board(canonical: list[list[int]]) -> None:
    """
    Debug function for printing out the canonical board in a
    readable way.

    Args:
        canonical - the canonical representation of the board
    Ret:
        None

    >>> row1 = [5, 0, 9, 0, 0, 0, 4, 0, 0]
    >>> row2 = [7, 0, 8, 3, 0, 4, 9, 0, 0]
    >>> row3 = [6, 0, 1, 0, 0, 0, 7, 3, 0]
    >>> row4 = [4, 6, 2, 5, 0, 0, 0, 0, 0]
    >>> row5 = [3, 8, 5, 7, 2, 0, 6, 4, 9]
    >>> row6 = [1, 0, 7, 4, 0, 8, 2, 0, 0]
    >>> row7 = [2, 0, 0, 1, 0, 0, 0, 0, 4]
    >>> row8 = [0, 0, 3, 0, 4, 0, 0, 8, 7]
    >>> row9 = [0, 7, 0, 0, 5, 3, 0, 0, 6]
    >>> dump_board([row1, row2, row3, row4, row5, row6, row7, row8, row9])
    Game board:
    [5, '_', 9, '_', '_', '_', 4, '_', '_']
    [7, '_', 8, 3, '_', 4, 9, '_', '_']
    [6, '_', 1, '_', '_', '_', 7, 3, '_']
    [4, 6, 2, 5, '_', '_', '_', '_', '_']
    [3, 8, 5, 7, 2, '_', 6, 4, 9]
    [1, '_', 7, 4, '_', 8, 2, '_', '_']
    [2, '_', '_', 1, '_', '_', '_', '_', 4]
    ['_', '_', 3, '_', 4, '_', '_', 8, 7]
    ['_', 7, '_', '_', 5, 3, '_', '_', 6]
    """
    print("Game board:")
    for row in canonical:
        print([(cell if cell != 0 else "_") for cell in row])


# The variables in the literals are integers, where the digits are row,
# column, and cell value, respectively e.g. 123 represents a 3 in row 1,
# column 2. We start counting from 1.


def canonical_to_cnf_literals(canonical: list[list]):
    """
    A generator for getting the CNF literals from the canonical
    representation of the board.

    Args:
        canonical - the canonical representation of the board
    Yields:
        CNF literals representing the board
    """
    for r, row in enumerate(canonical):
        for c, cell in enumerate(row):
            if cell != 0:
                yield ((r+1) * 100 + (c+1) * 10 + cell, True)
    return


def max_one(variables: list) -> list:
    """
    Given a list of variables, return a list of clauses that ensure 
    that at most one variable is true. In other words, for every two variables,
    at most one is true.

    Args:
        literals - a list of CNF literals

    >>> max_one([555, 545, 535])
    [[(555, False), (545, False)], [(555, False), (535, False)], [(545, False), (535, False)]]
    """
    ret = []
    for i, literal1 in enumerate(variables):
        for literal2 in variables[i + 1 :]:
            ret.append([(literal1, False), (literal2, False)])

    return ret

def one_digit_this_row(digit: int, row: int) -> list:
    """
    For a particular digit and row, return a list of clauses that ensure that
    exactly one instance of that digit appears in the row. 

    Args:
        digit - the digit to check for
        row - the row number (1-9)
    Returns:
        A list of clauses that ensure exactly one instance of the digit in the row
    """
    variables = [row * 100 + col * 10 + digit for col in range(1, 10)]
    formula = max_one(variables)
    at_least_one = [(var, True) for var in variables]
    formula.append(at_least_one)
    return formula

def one_digit_this_column(digit: int, column: int) -> list:
    """
    For a particular digit and column, return a list of clauses that ensure that
    exactly one instance of that digit appears in the column. 

    Args:
        digit - the digit to check for
        column - the column number (1-9)
    Returns:
        A list of clauses that ensure exactly one instance of the digit in the column
    """
    variables = [row * 100 + column * 10 + digit for row in range(1, 10)]
    formula = max_one(variables)
    at_least_one = [(var, True) for var in variables]
    formula.append(at_least_one)
    return formula

def one_digit_this_square(digit: int, square: tuple[int, int]) -> list: 
    """
    For a particular digit and square, return a list of clauses that ensure that
    exactly one instance of that digit appears in the square. 
    The square is represented by a tuple (row, column) where each can be 1, 2, or 3. 

    Args:
        digit - the digit to check for
        square - a tuple representing the square (row, column)
    Returns:
        A list of clauses that ensure exactly one instance of the digit in the square
    """
    SQUARES = {
        (1, 1): [110, 120, 130, 210, 220, 230, 310, 320, 330],
        (1, 2): [140, 150, 160, 240, 250, 260, 340, 350, 360],
        (1, 3): [170, 180, 190, 270, 280, 290, 370, 380, 390],
        (2, 1): [410, 420, 430, 510, 520, 530, 610, 620, 630],
        (2, 2): [440, 450, 460, 540, 550, 560, 640, 650, 660],
        (2, 3): [470, 480, 490, 570, 580, 590, 670, 680, 690],
        (3, 1): [710, 720, 730, 810, 820, 830, 910, 920, 930],
        (3, 2): [740, 750, 760, 840, 850, 860, 940, 950, 960],
        (3, 3): [770, 780, 790, 870, 880, 890, 970, 980, 990]
    }
    variables = [val + digit for val in SQUARES[square]]
    formula = max_one(variables)
    at_least_one = [(var, True) for var in variables]
    formula.append(at_least_one)
    return formula

def digit_constraints(digit: int) -> list:
    """
    For a particular digit, return a list of clauses that ensure that
    exactly one instance of that digit appears in each row, column, and square.
    Args:
        digit - the digit to check for
    Returns:
        A list of clauses that ensure exactly one instance of the digit in each row, column, and square
    """
    rows_check = []
    for row in range(1, 10):
        rows_check.extend(one_digit_this_row(digit, row))
    columns_check = []
    for column in range(1, 10):
        columns_check.extend(one_digit_this_column(digit, column))
    squares_check = []
    for square_row in range(1, 4):
        for square_col in range(1, 4):
            squares_check.extend(one_digit_this_square(digit, (square_row, square_col)))
    return rows_check + columns_check + squares_check

def sudoku_constraints() -> list:
    """
    Return a list of clauses that ensure the sudoku constraints are met.

    Returns:
        A list of clauses that ensure the sudoku constraints are met
    """
    formula = []
    for digit in range(1, 10):
        formula.extend(digit_constraints(digit))

    # each cell has one digit
    for row in range(1, 10):
        for col in range(1, 10):
            variables = [row * 100 + col * 10 + digit for digit in range(1, 10)]
            formula.extend(max_one(variables)) # max one
            formula.append([(var, True) for var in variables])  # at least one

    return formula

def update_formula(old_formula: list, literal: tuple) -> list | None:
    """
    Given an old CNF formula and a literal,
    return a new CNF formula with the literal substituted everywhere.

    Args:
        old_formula - the old CNF formula
        literal - the literal to substitute, represented as a tuple (variable, value)
    Returns:
        A new CNF formula with the literal substituted everywhere, or None if the literal leads to an empty clause 
    """
    new_formula = []
    for clause in old_formula:
        clause_copy = clause.copy()
        if literal in clause_copy:
            continue
        while (literal[0], not literal[1]) in clause_copy:
            clause_copy.remove((literal[0], not literal[1]))
        if clause_copy == []:
            return None
        new_formula.append(clause_copy)
    return new_formula

def sat_solver(formula, assignment=None):
    """
    Find a solution for a given CNF formula.

    Args:
        formula - a list of clauses representing the CNF formula
        assignment - a dictionary mapping variables to their values (True/False)
    Returns:
        A dictionary mapping variables to their values if a solution exists, or None if no solution exists
    """
    if assignment is None:
        assignment = {}
    # Unit clause propagation
    while True:
        unit_clauses = [c[0] for c in formula if len(c) == 1]
        if not unit_clauses:
            break
        for unit in unit_clauses:
            var, val = unit
            if var in assignment:
                if assignment[var] != val:
                    return None  # Conflict
            assignment[var] = val
            formula = update_formula(formula, unit)
            if formula is None:
                return None
    # If empty, all clauses satisfied
    if not formula or formula == []:
        return assignment
    # If any clause is empty, failure
    if any(len(clause) == 0 for clause in formula):
        return None
    # Branch: pick next literal
    for clause in formula:
        if len(clause) > 0:
            lit = clause[0]
            break
    var, val = lit
    # Try True branch
    new_assignment = dict(assignment)
    new_assignment[var] = val
    new_formula = update_formula(formula, (var, val))
    result = sat_solver(new_formula, new_assignment)
    if result is not None:
        return result
    # Try False branch
    new_assignment = dict(assignment)
    new_assignment[var] = not val
    new_formula = update_formula(formula, (var, not val))
    result = sat_solver(new_formula, new_assignment)
    if result is not None:
        return result
    return None


def solve_sudoku(canonical: list[list[int]]) -> list:
    """
    Solve the sudoku.

    Args:
        canonical - the canonical representation of the sudoku board
    Ret:
        A list of CNF literals representing the solution, or None if no solution exists 
    """
    # initial CNF formula based on given cells
    formula = sudoku_constraints()
    for literal in canonical_to_cnf_literals(canonical):
        formula.append([literal])  # Add the given literals as clauses
    return sat_solver(formula)

def cnf_to_canonical(cnf: list) -> list[list[int]]:
    """
    Convert a solved sudoku puzzle as a list of CNF literals
    back to the canonical representation of the board.
    
    Args:
        cnf - a list of CNF literals representing the solved sudoku puzzle
    Returns:
        A canonical representation of the sudoku board
    """
    board = [[0 for _ in range(9)] for _ in range(9)]

    for variable, val in cnf.items():
        if val:
            value = variable % 10 # last digit is value
            column = (variable // 10) % 10 - 1
            row = variable // 100 - 1
            board[row][column] = value

    return board  # Exclude the first row which is just a placeholder for 0 index

def print_solved_sudoku(canonical: list[list[int]]) -> None:
    """
    Print the solved sudoku in a readable format.

    Args:
        canonical - the canonical representation of the solved sudoku board
    
    >>> row1 = [5, 0, 9, 0, 0, 0, 4, 0, 0]
    >>> row2 = [7, 0, 8, 3, 0, 4, 9, 0, 0]
    >>> row3 = [6, 0, 1, 0, 0, 0, 7, 3, 0]
    >>> row4 = [4, 6, 2, 5, 0, 0, 0, 0, 0]
    >>> row5 = [3, 8, 5, 7, 2, 0, 6, 4, 9]
    >>> row6 = [1, 0, 7, 4, 0, 8, 2, 0, 0]
    >>> row7 = [2, 0, 0, 1, 0, 0, 0, 0, 4]
    >>> row8 = [0, 0, 3, 0, 4, 0, 0, 8, 7]
    >>> row9 = [0, 7, 0, 0, 5, 3, 0, 0, 6]
    >>> canonical = [row1, row2, row3, row4, row5, row6, row7, row8, row9]
    >>> print_solved_sudoku(canonical)
    Working...
    Game board:
    [5, 3, 9, 8, 7, 6, 4, 1, 2]
    [7, 2, 8, 3, 1, 4, 9, 6, 5]
    [6, 4, 1, 2, 9, 5, 7, 3, 8]
    [4, 6, 2, 5, 3, 9, 8, 7, 1]
    [3, 8, 5, 7, 2, 1, 6, 4, 9]
    [1, 9, 7, 4, 6, 8, 2, 5, 3]
    [2, 5, 6, 1, 8, 7, 3, 9, 4]
    [9, 1, 3, 6, 4, 2, 5, 8, 7]
    [8, 7, 4, 9, 5, 3, 1, 2, 6]
    """
    print("Working...")
    dump_board(cnf_to_canonical(solve_sudoku(canonical)))


if __name__ == "__main__":
    import doctest
    doctest.testmod()