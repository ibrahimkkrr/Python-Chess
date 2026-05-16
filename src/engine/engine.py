import copy
from .board import Board


class ChessEngine:
    def __init__(self):
        self.board = Board()

        self.turn = 'white'


        self.move_log = []

        self.is_game_over = False
        self.winner = None

        self.white_time = 600.0
        self.black_time = 600.0

        self.is_timed_game = False
        self.is_ai_game = False

    def evaluate_board(self):
        status = self.check_game_status()
        if status == "white_wins": return -9999
        if status == "black_wins": return 9999
        if status == "stalemate": return 0

        # 2. Count the pieces!
        piece_values = {'Pawn': 10, 'Knight': 30, 'Bishop': 30, 'Rook': 50, 'Queen': 90, 'King': 900}
        score = 0

        for r in range(8):
            for c in range(8):
                piece = self.board.get_piece(r, c)
                if piece:
                    val = piece_values.get(piece.name, 0)
                    if piece.color == 'black':
                        score += val
                    else:
                        score -= val

        return score

    def get_ai_move(self):
        import random
        import copy

        all_moves = self.get_all_possible_legal_moves('black')
        if not all_moves:
            return None

        best_move = None
        best_score = -float('inf')

        for start, end in all_moves:
            simulated_engine = copy.deepcopy(self)
            simulated_engine.make_move(start[0], start[1], end[0], end[1])

            white_moves = simulated_engine.get_all_possible_legal_moves('white')

            worst_case_for_black = float('inf')

            if not white_moves:
                worst_case_for_black = simulated_engine.evaluate_board()
            else:
                for w_start, w_end in white_moves:
                    sim_engine_2 = copy.deepcopy(simulated_engine)
                    sim_engine_2.make_move(w_start[0], w_start[1], w_end[0], w_end[1])

                    score = sim_engine_2.evaluate_board()
                    if score < worst_case_for_black:
                        worst_case_for_black = score

            if worst_case_for_black > best_score:
                best_score = worst_case_for_black
                best_move = (start, end)
            elif worst_case_for_black == best_score:
                if random.random() > 0.5:
                    best_move = (start, end)

        if best_move is None:
            return random.choice(all_moves)

        return best_move

    def get_valid_moves(self, row, col):
        piece = self.board.get_piece(row, col)
        if piece is None or piece.color != self.turn:
            return []

        valid_moves = []
        raw_moves = piece.get_raw_moves(row, col, self.board)

        for move in raw_moves:
            if piece.name in ['Rook', 'Bishop', 'Queen']:
                if not self.is_path_clear(row, col, move[0], move[1], self.board):
                    continue

            # Simulation time!
            ghost_board = copy.deepcopy(self.board)
            ghost_board.move_piece(row, col, move[0], move[1])

            if not self.is_king_in_check(piece.color, ghost_board):
                valid_moves.append(move)

        return valid_moves



    def find_king(self, color, board):

        for row in range(8):
            for col in range(8):
                piece = board.get_piece(row, col)
                if piece is not None:
                    if piece.color == color and piece.name == 'King':
                        return row, col

    def is_king_in_check(self, color, board):
        king_pos = self.find_king(color, board)
        enemy_color = 'black' if color == 'white' else 'white'

        for row in range(8):
            for col in range(8):
                piece = board.get_piece(row, col)
                if piece is None or piece.color != enemy_color:
                    continue

                raw_moves = piece.get_raw_moves(row, col, board)

                if king_pos in raw_moves:
                    if piece.name in ['Knight', 'Pawn', 'King']:
                        return True
                    else:
                        # PASS THE BOARD HERE TOO!
                        if self.is_path_clear(row, col, king_pos[0], king_pos[1], board):
                            return True
        return False

    def undo_last_move(self):
        if len(self.move_log) == 0:
            return

        last_move = self.move_log.pop()

        start_row, start_col = last_move['start']
        target_row, target_col = last_move['target']
        piece_moved = last_move['piece_moved']
        piece_captured = last_move['piece_captured']

        self.board.matrix[start_row][start_col] = piece_moved

        self.board.matrix[target_row][target_col] = piece_captured

        if last_move['moved_first_time']:
            piece_moved.has_moved = False

        self.switch_turn()

    def make_move(self, start_row, start_col, target_row, target_col):

        piece_moved = self.board.get_piece(start_row, start_col)
        piece_captured = self.board.get_piece(target_row, target_col)

        move_record = {
            'start': (start_row, start_col),
            'target': (target_row, target_col),
            'piece_moved': piece_moved,
            'piece_captured': piece_captured,
            'moved_first_time': not piece_moved.has_moved if piece_moved else False
        }

        self.move_log.append(move_record)

        self.board.move_piece(start_row, start_col, target_row, target_col)

        if not self.is_promotion_pending(target_row, target_col):
            self.switch_turn()

    def is_promotion_pending(self, target_row, target_col):
        piece = self.board.matrix[target_row][target_col]

        if piece is not None and piece.name == 'Pawn':
            if (piece.color == 'white' and target_row == 0) or \
                    (piece.color == 'black' and target_row == 7):
                return True

        return False


    def complete_promotion(self, target_square, choice_string):
        row, col = target_square

        from .pieces import Queen
        from .pieces import Knight
        from .pieces import Bishop
        from .pieces import Rook


        if choice_string == 'Queen':
            self.board.matrix[row][col] = Queen(self.turn)
        elif choice_string == 'Rook':
            self.board.matrix[row][col] = Rook(self.turn)
        elif choice_string == 'Knight':
            self.board.matrix[row][col] = Knight(self.turn)
        elif choice_string == 'Bishop':
            self.board.matrix[row][col] = Bishop(self.turn)

        self.turn = 'black' if self.turn == 'white' else 'white'

    def switch_turn(self):

        self.turn = 'black' if self.turn == 'white' else 'white'

    def check_game_status(self):

        all_moves = self.get_all_possible_legal_moves(self.turn)

        if len(all_moves) == 0:
            if self.is_king_in_check(self.turn,self.board):
                return "checkmate"
            else:
                return "stalemate"

        return "active"

    def get_all_possible_legal_moves(self, turn):

        all_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)

                if piece is None or piece.color != turn:
                    continue

                valid_moves = self.get_valid_moves(row, col)
                for target_square in valid_moves:
                    all_moves.append(((row, col), target_square))

        return all_moves

    def is_path_clear(self, start_row, start_col, end_row, end_col, board):
        diff_row = end_row - start_row
        diff_col = end_col - start_col

        step_row = (diff_row // abs(diff_row)) if diff_row != 0 else 0
        step_col = (diff_col // abs(diff_col)) if diff_col != 0 else 0

        curr_row = start_row + step_row
        curr_col = start_col + step_col

        while (curr_row, curr_col) != (end_row, end_col):
            if board.get_piece(curr_row, curr_col) is not None:
                return False
            curr_row += step_row
            curr_col += step_col

        return True













