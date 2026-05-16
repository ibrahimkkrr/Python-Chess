import pygame


class ViewGameOverState:
    def __init__(self, result):
        self.result = result
        self.font = pygame.font.Font(None, 64)
        self.font.set_bold(True)

        self.sub_font = pygame.font.Font(None, 32)
        self.played_sound = False


    def render(self, screen, square_size, engine, view ,legal_moves):

        if not self.played_sound:
            view.play_sound("game_over" ,1)

        self.played_sound = True

        from .state_playing import ViewPlayingState

        ViewPlayingState().render(screen, square_size, engine, view, legal_moves)

        overlay = pygame.Surface((square_size * 8, square_size * 8))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        if "time" in self.result:
            main_text = "TIME'S UP!"
            winner = "WHITE" if "white" in self.result else "BLACK"
            sub_text = f"{winner} WINS ON TIME"
        else:
            winner = "BLACK" if engine.turn == "white" else "WHITE"
            main_text = "CHECKMATE!" if self.result == "checkmate" else "STALEMATE!"
            sub_text = f"{winner} WINS" if self.result == "checkmate" else "IT'S A DRAW"

        prompt_text = "Press ENTER to restart"

        white = (255, 255, 255)
        light_gray = (200, 200, 200)  # Slightly darker for the prompt

        title_surf = self.font.render(main_text, True, white)
        detail_surf = self.sub_font.render(sub_text, True, white)
        prompt_surf = self.sub_font.render(prompt_text, True, light_gray)  # Render new text

        center_x = square_size * 4
        center_y = square_size * 4

        title_rect = title_surf.get_rect(center=(center_x, center_y - 40))
        detail_rect = detail_surf.get_rect(center=(center_x, center_y + 30))
        prompt_rect = prompt_surf.get_rect(center=(center_x, center_y + 100))  # Put this one lowest

        screen.blit(title_surf, title_rect)
        screen.blit(detail_surf, detail_rect)
        screen.blit(prompt_surf, prompt_rect)

