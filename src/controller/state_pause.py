import pygame

from src.view import ViewMainMenuState
from src.view import ViewPlayingState

class ControllerPauseState:
    def handle_mouse_click(self, controller, x, y, square_size):
        center_x = (square_size * 8) // 2

        resume_rect = pygame.Rect(center_x - 100, square_size * 3.5, 200, 60)
        restart_rect = pygame.Rect(center_x - 100, square_size * 4.5, 200, 60)
        menu_rect = pygame.Rect(center_x - 125, square_size * 5.5, 250, 60)

        click_pos = (x, y)

        from .state_playing import ControllerPlayingState
        from .state_main_menu import ControllerMainMenuState

        if resume_rect.collidepoint(click_pos):
            controller.view.change_state(ViewPlayingState())
            controller.change_state(ControllerPlayingState())

        elif restart_rect.collidepoint(click_pos):
            was_timed = controller.engine.is_timed_game
            was_ai = controller.engine.is_ai_game

            controller.app.engine = type(controller.engine)()
            controller.engine = controller.app.engine
            controller.engine.is_timed_game = was_timed
            controller.engine.is_ai_game = was_ai
            controller.view.change_state(ViewPlayingState())
            controller.change_state(ControllerPlayingState())

        elif menu_rect.collidepoint(click_pos):
            controller.app.engine = type(controller.engine)()
            controller.engine = controller.app.engine
            controller.view.change_state(ViewMainMenuState())
            controller.change_state(ControllerMainMenuState())

    def handle_key_press(self, controller, key):
        from .state_playing import ControllerPlayingState

        if key == pygame.K_ESCAPE:
            controller.view.change_state(ViewPlayingState())
            controller.change_state(ControllerPlayingState())