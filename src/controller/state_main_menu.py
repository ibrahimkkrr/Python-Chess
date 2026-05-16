import pygame
import sys

from src.view import ViewPlayingState

class ControllerMainMenuState:
    def handle_mouse_click(self, controller, x, y, square_size):
        import pygame
        import sys

        # Make sure ViewPlayingState is imported at the top of your file or here
        from .state_playing import ControllerPlayingState

        click_pos = (x, y)
        current_view_state = controller.view.state

        if hasattr(current_view_state, 'theme_button'):
            if current_view_state.theme_button.collidepoint(click_pos):
                controller.view.current_theme_index = (controller.view.current_theme_index + 1) % len(
                    controller.view.themes)

                if hasattr(current_view_state, 'blurred_background'):
                    current_view_state.blurred_background = None
                return

        center_x = (square_size * 8) // 2

        play_rect = pygame.Rect(center_x - 100, square_size * 3.5, 200, 50)
        timer_rect = pygame.Rect(center_x - 125, square_size * 4.5, 250, 50)
        ai_rect = pygame.Rect(center_x - 100, square_size * 5.5, 200, 50)
        exit_rect = pygame.Rect(center_x - 100, square_size * 6.5, 200, 50)

        if play_rect.collidepoint(click_pos):
            controller.engine.is_timed_game = False
            controller.engine.is_ai_game = False
            controller.view.change_state(ViewPlayingState())
            controller.change_state(ControllerPlayingState())

        elif timer_rect.collidepoint(click_pos):
            controller.engine.is_timed_game = True
            controller.engine.is_ai_game = False
            controller.view.change_state(ViewPlayingState())
            controller.change_state(ControllerPlayingState())

        elif ai_rect.collidepoint(click_pos):
            controller.engine.is_timed_game = False
            controller.engine.is_ai_game = True
            controller.view.change_state(ViewPlayingState())
            controller.change_state(ControllerPlayingState())

        elif exit_rect.collidepoint(click_pos):
            pygame.quit()
            sys.exit()

    def handle_key_press(self, controller, key):
        pass
