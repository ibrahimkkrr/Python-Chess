import pygame

class ViewPauseState:
    def __init__(self):
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 64)
        self.title_font.set_bold(True)

        self.button_font = pygame.font.Font(None, 32)
        self.button_font.set_bold(True)
        self.blurred_background = None

    def render(self, screen, square_size, engine, view, legal_moves):
        screen_w, screen_h = square_size * 8, square_size * 8

        if self.blurred_background is None:
            temp_surface = pygame.Surface((screen_w, screen_h))
            from .state_playing import ViewPlayingState

            ViewPlayingState().render(temp_surface, square_size, engine, view, [])

            try:
                self.blurred_background = pygame.transform.box_blur(temp_surface, 10)
            except AttributeError:
                snapshot = pygame.transform.smoothscale(temp_surface, (screen_w // 4, screen_h // 4))
                self.blurred_background = pygame.transform.smoothscale(snapshot, (screen_w, screen_h))

        # 2. Draw the blurred background and dim it
        screen.blit(self.blurred_background, (0, 0))
        overlay = pygame.Surface((screen_w, screen_h))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        title_surf = self.title_font.render("PAUSED", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(screen_w // 2, square_size * 2))
        screen.blit(title_surf, title_rect)

        center_x = screen_w // 2
        self.buttons = {
            "Resume": pygame.Rect(center_x - 100, square_size * 3.5, 200, 60),
            "Restart": pygame.Rect(center_x - 100, square_size * 4.5, 200, 60),
            "Main Menu": pygame.Rect(center_x - 125, square_size * 5.5, 250, 60)
        }

        mouse_pos = pygame.mouse.get_pos()
        for text, rect in self.buttons.items():
            color = (100, 200, 100) if rect.collidepoint(mouse_pos) else (50, 50, 50)

            pygame.draw.rect(screen, color, rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), rect, 3, border_radius=10)

            text_surf = self.button_font.render(text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)