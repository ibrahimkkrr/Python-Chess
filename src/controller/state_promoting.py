
from src.view import ViewPlayingState

class ControllerPromotingState:
    def __init__(self, pawn_square):
        self.pawn_square = pawn_square

    def handle_mouse_click(self, controller, x, y, square_size):
        col = x // square_size
        row = y // square_size

        choice = None

        if row == 3:
            if col == 2:
                choice = 'Queen'
            elif col == 3:
                choice = 'Rook'
            elif col == 4:
                choice = 'Bishop'
            elif col == 5:
                choice = 'Knight'

        if choice:
            from .state_playing import ControllerPlayingState

            controller.engine.complete_promotion(self.pawn_square, choice)

            controller.change_state(ControllerPlayingState())
            controller.view.change_state(ViewPlayingState())
