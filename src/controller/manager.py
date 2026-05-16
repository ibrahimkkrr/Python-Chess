import pygame

class ChessGameController:
    def __init__(self, app):
        self.app = app
        self.engine = app.engine

        self.view = app.view

        from .state_main_menu import ControllerMainMenuState

        self.state = ControllerMainMenuState()


    def change_state(self, new_state):
        self.state = new_state

    def handle_events(self, events, square_size):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                self.state.handle_mouse_click(self, x, y, square_size)


            elif event.type == pygame.KEYDOWN:
                if hasattr(self.state, 'handle_key_press'):
                    self.state.handle_key_press(self, event.key)

    def render(self, screen, square_size):
        moves = getattr(self.state, 'legal_moves', [])
        self.view.render(screen, square_size, self.engine,moves)


    def get_board_coords(self, x, y, square_size):
        col = x // square_size
        row = y // square_size

        if self.engine.turn == 'black':
            col = 7 - col
            row = 7 - row
        return row, col

    def update(self, dt):
        if hasattr(self.state, 'update'):
            self.state.update(self, dt)










