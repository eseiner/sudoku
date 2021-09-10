# Eli Seiner
# CS1 Lab 7c

"""This program allows the user to interactively play the game of Sudoku."""

import sys


class SudokuError(Exception):
    """Base class for all Sudoku errors."""

    pass


class SudokuLoadError(SudokuError):
    """Exception class for Sudoku file loading errors."""

    pass


class SudokuMoveError(SudokuError):
    """Exception class for Sudoku move errors."""

    pass


class SudokuCommandError(SudokuError):
    """Exception class for Sudoku input command errors."""

    pass


class SudokuCommandError(SudokuError):
    """Base class for all Sudoku errors."""

    pass


class Sudoku:
    """Interactively play the game of Sudoku."""

    def __init__(self):
        """Create the Sudoku board."""
        self.grid = [[0 for j in range(9)] for i in range(9)]
        self.moves = []

    def load(self, filename):
        """
        Load the contents of a file into the board.

        A board file must have 9 lines of 9 characters each
        (not counting newlines).  The characters must be digits
        from 0-9.  0 means a blank space; others represent filled
        squares.  The contents of the file are loaded into the board
        as integers.

        Arguments:
        - filename: the name of the file to load

        Return value: none
        """
        file = open(filename, 'r')
        lst = []
        for line in file:
            cut_line = line.rstrip('\n')
            if cut_line.isdigit() is False:
                raise SudokuLoadError('File has invalid characters!')
            if len(cut_line) != 9:
                raise SudokuLoadError('File has invalid ' +
                                      'number of characters per line!')
            row = []
            for num in cut_line:
                row.append(int(num))
            lst.append(row)
        if len(lst) != 9:
            raise SudokuLoadError('File has invalid number of lines!')
        self.grid = lst
        self.moves = []
        file.close()

    def save(self, filename):
        """
        Save the current state of the board to a file.

        A `FileNotFoundError` is raised if the file doesn't exist.

        Arguments:
        - filename: the name of the file to load

        Return value: none
        """
        file = open(filename, 'w')
        line = ''
        for i in range(8):
            for val in self.grid[i]:
                line += str(val)
            file.write(line + '\n')
            line = ''
        for num in self.grid[8]:
            line += str(num)
        file.write(line)

    def show(self):
        """Pretty-print the current board representation."""
        print()
        print('   1 2 3 4 5 6 7 8 9 ')
        for i in range(9):
            if i % 3 == 0:
                print('  +-----+-----+-----+')
            print(f'{i + 1} |', end='')
            for j in range(9):
                if self.grid[i][j] == 0:
                    print(end=' ')
                else:
                    print(f'{self.grid[i][j]}', end='')
                if j % 3 != 2:
                    print(end=' ')
                else:
                    print('|', end='')
            print()
        print('  +-----+-----+-----+')
        print()

    def move(self, row, col, val):
        """
        Place a number 'val' at row 'row' and column 'col'.

        Don't place the number if it duplicates another number
        in a row, column, or box.  Rows are indexed from 1-9
        and columns are indexed from a-i.

        Arguments:
        - row: a row index (0 for the first)
        - col: a column index (0 for the first)
        - val: the number to place (1-9)

        Return value: none
        """
        if str(row) not in '123456789':
            raise SudokuMoveError('Invalid row number!')
        if str(col) not in '123456789':
            raise SudokuMoveError('Invalid column number!')
        if self.grid[int(row) - 1][int(col) - 1] != 0:
            raise SudokuMoveError('Location is not empty!')
        if int(val) in self.grid[int(row) - 1]:
            raise SudokuMoveError('Invalid move: ' +
                                  'row conflict; please try again.')
        cols = []
        for r in range(9):
            cols.append(self.grid[r][int(col) - 1])
        if int(val) in cols:
            raise SudokuMoveError('Invalid move: ' +
                                  'column conflict; please try again.')
        row_box = (int(row) - 1) // 3
        col_box = (int(col) - 1) // 3

        for box_row in range(3 * row_box, 3 * row_box + 3):
            for box_col in range(3 * col_box, 3 * col_box + 3):
                if int(val) == self.grid[box_row][box_col]:
                    raise SudokuMoveError('Invalid move: ' +
                                          'box conflict; please try again.')
        self.moves.append((row, col, val))
        self.grid[int(row) - 1][int(col) - 1] = val

    def undo(self):
        """
        Undo the last move.

        Restore the state of the board to the state it was in
        one move previously.
        """
        (row, col) = self.moves.pop()[:2]
        self.grid[int(row) - 1][int(col) - 1] = 0
        print('Undoing last move...')

    def solve(self):
        """Solve a Sudoku game interactively."""
        while True:
            try:
                command = input('soduko> ')
                if command == 'q':
                    break
                elif command == 'u':
                    self.undo()
                    self.show()
                elif command[0:2] == 's ':
                    self.save(command[2:])
                elif len(command) == 3:
                    for num in command:
                        if num not in '123456789':
                            break
                    self.move(command[0], command[1], command[2])
                    self.show()
                else:
                    raise SudokuCommandError(command)
            except SudokuCommandError as e:
                print(e)
            except SudokuMoveError as e:
                print(e)


if __name__ == '__main__':
    s = Sudoku()

    while True:
        filename = input('Enter the sudoku filename: ')
        try:
            s.load(filename)
            break
        except FileNotFoundError as e:
            print(e)
        except SudokuLoadError as e:
            print(e)

    s.show()
    s.solve()
