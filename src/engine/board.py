
from .pieces import PieceFactory

class Board:
    def __init__(self):
        self.factory = PieceFactory()

        self._create_empty_matrix()

    def is_on_board(self, row, col):

       return 0 <= row < 8 and 0 <= col < 8

    def get_piece(self, row, col):
        if(self.is_on_board(row, col)):
         return self.matrix[row][col]
        else:
            return None
    def move_piece(self, start_row, start_col, target_row, target_col):


        piece = self.matrix[start_row][start_col]

        if piece is None:
            return

        if piece.name == 'King' and abs(target_col - start_col) == 2:

            if target_col > start_col:
                rook = self.matrix[start_row][7]
                self.matrix[start_row][7] = None
                self.matrix[start_row][5] = rook
                rook.has_moved = True
            else:
                rook = self.matrix[start_row][0]
                self.matrix[start_row][0] = None
                self.matrix[start_row][3] = rook
                rook.has_moved = True


        self.matrix[target_row][target_col] = piece
        self.matrix[start_row][start_col] = None

        if piece is not None:
            piece.has_moved = True



    def _create_empty_matrix(self):
        starting_map = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]

        self.matrix = [[None for _ in range(8)] for _ in range(8)]

        for row in range(8):
            for col in range(8):
                symbol = starting_map[row][col]
                self.matrix[row][col] = PieceFactory.create_piece(symbol)
