import pygame

from src.view import ViewPlayingState

class ControllerGameOverState:
    def __init__(self, status):
        self.status = status # 'checkmate' or 'stalemate'

    def handle_mouse_click(self, controller, x, y, square_size):
        pass

    def handle_key_press(self, controller, key):
        if key == pygame.K_RETURN:
            from .state_playing import ControllerPlayingState

            pygame.mixer.stop()
            was_timed = controller.engine.is_timed_game
            was_ai = controller.engine.is_ai_game
            controller.app.engine = type(controller.engine)()
            controller.engine = controller.app.engine
            controller.engine.is_timed_game = was_timed
            controller.engine.is_ai_game = was_ai

            controller.view.change_state(ViewPlayingState())

            controller.change_state(ControllerPlayingState())
