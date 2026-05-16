import pygame
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path,relative_path)



class ChessView:
    def __init__(self):

        from .state_main_menu import ViewMainMenuState

        self.state = ViewMainMenuState()
        self.images = self.load_images()
        pygame.font.init()
        self.timer_font = pygame.font.Font(None, 24)
        self.sounds = self.load_sounds()


        self.themes = [
            {"light": (240, 217, 181), "dark": (181, 136, 99)},
            {"light": (238, 238, 210), "dark": (118, 150, 86)},
            {"light": (175, 185, 195), "dark": (120, 135, 148)},
            {"light": (220, 220, 220), "dark": (100, 100, 100)},
        ]

        pygame.mixer.init()


        self.sounds = {
            "move": pygame.mixer.Sound(resource_path("assets/sounds/Move.mp3")),
            "capture": pygame.mixer.Sound(resource_path("assets/sounds/Capture.mp3")),
            "check": pygame.mixer.Sound(resource_path("assets/sounds/Check.mp3")),
            "game_over": pygame.mixer.Sound(resource_path("assets/sounds/capy song.mp3"))
        }

        self.current_theme_index = 0

    def play_sound(self, key,loops = 0):
        if key in self.sounds:
            self.sounds[key].play(loops=loops)

    def load_images(self):
        images = {}
        pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK',
                  'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']

        for piece in pieces:
            img_path = os.path.join('assets/images', f'{piece}.png')

            full_path = resource_path(img_path)

            try:
                images[piece] = pygame.image.load(full_path)
            except FileNotFoundError:
                print(f"Warning: Could not find {full_path}")

        return images

    def load_sounds(self):
        sounds = {}
        # Map the dictionary key to the actual filename
        sound_files = {
            "move": "Move.mp3",
            "capture": "Capture.mp3",
            "check": "Check.mp3",
            "game_over": "capy song.mp3"
        }

        for key, filename in sound_files.items():
            sound_path = os.path.join('assets/sounds', filename)
            full_path = resource_path(sound_path)

            try:
                sounds[key] = pygame.mixer.Sound(full_path)
            except FileNotFoundError:
                print(f"Warning: Could not find sound {full_path}")
            except pygame.error as e:
                # Pygame throws this if the mp3 format is weird/unsupported
                print(f"Warning: Pygame could not load sound {full_path}. Error: {e}")

        return sounds

    def update(self, dt):
        if hasattr(self.state, 'update'):
            self.state.update(self, dt)


    def change_state(self, new_state):
        self.state = new_state

    def render(self, screen, square_size, engine,legal_moves):
        self.state.render(screen, square_size, engine, self,legal_moves)


