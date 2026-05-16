from __future__ import annotations
from abc import ABC, abstractmethod


class PieceFactory():

    @staticmethod
    def create_piece(symbol):
        if symbol == '.' or symbol == ' ':
            return None

        is_white = symbol.isupper()
        color = 'white' if is_white else 'black'

        char = symbol.lower()

        if char == 'k': return King(color)
        if char == 'n': return Knight(color)
        if char == 'p': return Pawn(color)
        if char == 'r': return Rook(color)
        if char == 'b': return Bishop(color)
        if char == 'q': return Queen(color)

class Piece(ABC):

    def __init__(self,color,name):
     self.color = color
     self.name = name
     self.has_moved = False

    @abstractmethod
    def get_raw_moves(self):
        pass


class Knight(Piece):

    def __init__(self, color):
        super().__init__(color,'Knight')

    def get_raw_moves(self, row, col, board):
        moves = []
        directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

        for dr, dc in directions:
            current_row = row + dr
            current_col = col + dc

            if board.is_on_board(current_row, current_col):
                target_piece = board.get_piece(current_row, current_col)

                if target_piece is None:
                    moves.append((current_row, current_col))
                elif self.color != target_piece.color:
                    moves.append((current_row, current_col))

        return moves


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, 'Rook')

    def get_raw_moves(self, row, col, board):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dr, dc in directions:
            current_row = row + dr
            current_col = col + dc

            while board.is_on_board(current_row, current_col):

                target_piece = board.get_piece(current_row, current_col)
                if target_piece is None:
                    moves.append((current_row, current_col))
                elif self.color != target_piece.color:
                    moves.append((current_row, current_col))
                    break
                else:
                    break

                current_row += dr
                current_col += dc

        return moves


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, 'Queen')
        self.rook = Rook(self.color)
        self.bishop = Bishop(self.color)

    def get_raw_moves(self, row, col, board):
        line_moves = self.rook.get_raw_moves(row, col, board)
        diagonal_moves = self.bishop.get_raw_moves(row, col, board)
        moves = line_moves + diagonal_moves
        return moves

class Bishop(Piece):

    def __init__(self, color):
        super().__init__(color, 'Bishop')

    def get_raw_moves(self, row, col, board):
        moves = []
        directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

        for dr, dc in directions:
            current_row = row + dr
            current_col = col + dc

            while board.is_on_board(current_row, current_col):

                target_piece = board.get_piece(current_row, current_col)
                if target_piece is None:
                    moves.append((current_row, current_col))
                elif self.color != target_piece.color:
                    moves.append((current_row, current_col))
                    break
                else:
                    break


                current_row += dr
                current_col += dc

        return moves


class King(Piece):
    def __init__(self, color):
        super().__init__(color, 'King')

    def get_castle_moves(self, row, col, board):
        moves = []
        if self.has_moved:
            return moves


        right_piece = board.get_piece(row, 7)

        if right_piece is not None and right_piece.name == 'Rook' and not right_piece.has_moved:
            if board.get_piece(row, 5) is None and board.get_piece(row, 6) is None:
                moves.append((row, 6))


        left_piece = board.get_piece(row, 0)

        if left_piece is not None and left_piece.name == 'Rook' and not left_piece.has_moved:
            if board.get_piece(row, 1) is None and board.get_piece(row, 2) is None and board.get_piece(row, 3) is None:
                moves.append((row, 2))
        return moves

    def get_raw_moves(self, row, col, board):
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]

        for dr, dc in directions:
            current_row = row + dr
            current_col = col + dc

            if board.is_on_board(current_row, current_col):
                target_piece = board.get_piece(current_row, current_col)

                if target_piece is None:
                    moves.append((current_row, current_col))
                elif self.color != target_piece.color:
                    moves.append((current_row, current_col))



        moves = moves + self.get_castle_moves(row, col, board)

        return moves

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, 'Pawn')

    def get_raw_moves(self, row, col, board):
        moves = []


        direction = -1 if self.color.lower() == 'white' else 1

        step_row = row + direction
        if board.is_on_board(step_row, col):
            if board.get_piece(step_row, col) is None:
                moves.append((step_row, col))

                if not self.has_moved:
                    jump_row = row + (direction * 2)
                    if board.is_on_board(jump_row, col):
                        if board.get_piece(jump_row, col) is None:
                            moves.append((jump_row, col))

        for dc in [-1, 1]:
            diag_row = row + direction
            diag_col = col + dc

            if board.is_on_board(diag_row, diag_col):
                target_piece = board.get_piece(diag_row, diag_col)

                if target_piece is not None and target_piece.color != self.color:
                    moves.append((diag_row, diag_col))

        return moves
