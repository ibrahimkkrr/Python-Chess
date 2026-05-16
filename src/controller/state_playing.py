import pygame

from src.view import ViewGameOverState
from src.view import ViewPauseState
from src.view import ViewPromotingState

class ControllerPlayingState:
    def __init__(self):
        self.selected_square = None
        self.legal_moves = []
        self.ai_delay = 0.5


    def update(self, controller, dt):

        from .state_game_over import ControllerGameOverState

        if getattr(controller.engine, 'is_ai_game', False) and controller.engine.turn == 'black':
            self.ai_delay -= dt
            if self.ai_delay <= 0:
                ai_move = controller.engine.get_ai_move()
                if ai_move:
                    start, end = ai_move
                    controller.engine.make_move(start[0], start[1], end[0], end[1])

                    status = controller.engine.check_game_status()
                    if status != "active":

                        controller.change_state(ControllerGameOverState(status))
                        controller.view.change_state(ViewGameOverState(status))

                    self.ai_delay = 0.5
            return

        if not controller.engine.is_timed_game:
            return

        if controller.engine.turn == 'white':
            controller.engine.white_time -= dt
            if controller.engine.white_time <= 0:
                controller.engine.white_time = 0
                controller.change_state(ControllerGameOverState("black_wins_on_time"))
                controller.view.change_state(ViewGameOverState("black_wins_on_time"))
        else:
            controller.engine.black_time -= dt
            if controller.engine.black_time <= 0:
                controller.engine.black_time = 0
                controller.change_state(ControllerGameOverState("white_wins_on_time"))
                controller.view.change_state(ViewGameOverState("white_wins_on_time"))

    def handle_key_press(self, controller, key):
        if key == pygame.K_ESCAPE:
            from .state_pause import ControllerPauseState

            controller.view.change_state(ViewPauseState())
            controller.change_state(ControllerPauseState())
        elif key == pygame.K_u:
            controller.engine.undo_last_move()

            self.selected_square = None

    def handle_mouse_click(self, controller, x, y, square_size):
        row, col = controller.get_board_coords(x, y, square_size)

        if not (0 <= col < 8 and 0 <= row < 8): return

        if self.selected_square is None:
            piece = controller.engine.board.get_piece(row, col)
            if piece and piece.color == controller.engine.turn:
                self.selected_square = (row, col)
                self.legal_moves = controller.engine.get_valid_moves(row, col)

        else:
            target = (row, col)
            if target in self.legal_moves:

                captured_piece = controller.engine.board.get_piece(target[0], target[1])

                controller.engine.make_move(self.selected_square[0], self.selected_square[1], target[0], target[1])
                in_check = controller.engine.is_king_in_check(controller.engine.turn, controller.engine.board)
                status = controller.engine.check_game_status()

                if status != "active":
                    from .state_game_over import ControllerGameOverState

                    controller.change_state(ControllerGameOverState(status))
                    controller.view.change_state(ViewGameOverState(status))

                elif in_check:
                    controller.view.play_sound("check")

                elif captured_piece is not None:
                    controller.view.play_sound("capture")

                else:
                    controller.view.play_sound("move")

                if controller.engine.is_promotion_pending(target[0], target[1]):
                    from .state_promoting import ControllerPromotingState

                    controller.change_state(ControllerPromotingState(target))
                    controller.view.change_state(ViewPromotingState())

            self.selected_square = None
            self.legal_moves = []
