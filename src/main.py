import pygame
import os
import sys

from src.engine import ChessEngine
from src.view import ChessView
from src.controller import ChessGameController


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path,relative_path)

class ChessApp:
    def __init__(self):

        icon_surface = pygame.image.load(resource_path('src/icon.ico'))
        pygame.display.set_icon(icon_surface)

        pygame.init()
        self.screen = pygame.display.set_mode((800, 800), pygame.RESIZABLE)
        self.square_size = 800 // 8
        self.running = True

        self.engine = ChessEngine()
        self.view = ChessView()

        self.active_controller = ChessGameController(self)

    def change_controller(self, new_controller):
        self.active_controller = new_controller

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            dt = clock.tick(60) / 1000.0
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.VIDEORESIZE:
                    smallest_side = min(event.w, event.h)
                    self.screen = pygame.display.set_mode((smallest_side, smallest_side), pygame.RESIZABLE)
                    self.square_size = smallest_side // 8

            self.active_controller.handle_events(events, self.square_size)

            if hasattr(self.active_controller, 'update'):
                self.active_controller.update(dt)


            self.active_controller.render(self.screen, self.square_size)

            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == '__main__':

    app = ChessApp()
    app.run()