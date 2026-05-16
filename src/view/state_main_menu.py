import pygame


class ViewMainMenuState:
    def __init__(self):
            pygame.font.init()
            self.title_font = pygame.font.Font(None, 64)
            self.title_font.set_bold(True)

            self.button_font = pygame.font.Font(None, 32)
            self.button_font.set_bold(True)

            self.blurred_background = None

    def render(self, screen, square_size, engine, view, legal_moves):
        screen_w, screen_h = square_size * 8, square_size * 8

        screen.fill((30, 30, 30))

        # --- 1. BLURRED BACKGROUND ---
        if self.blurred_background is None:
            temp_surface = pygame.Surface((screen_w, screen_h))

            from .state_playing import ViewPlayingState

            ViewPlayingState().render(temp_surface, square_size, engine, view, [])

            try:
                self.blurred_background = pygame.transform.box_blur(temp_surface, 10)
            except AttributeError:
                snapshot = pygame.transform.smoothscale(temp_surface, (screen_w // 4, screen_h // 4))
                self.blurred_background = pygame.transform.smoothscale(snapshot, (screen_w, screen_h))

        screen.blit(self.blurred_background, (0, 0))

        overlay = pygame.Surface((screen_w, screen_h))
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        center_x = screen_w // 2

        # --- 2. TITLE & SUBTITLE ---
        # Moved the title up slightly to square_size * 1.5
        title_surf = self.title_font.render("PYTHON CHESS", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(center_x, square_size * 1.5))
        screen.blit(title_surf, title_rect)

        # Added your "Made by" subtitle right below the title!
        subtitle_surf = self.button_font.render("Made by Ibrahim Abdoulgader", True, (200, 200, 200))
        subtitle_rect = subtitle_surf.get_rect(center=(center_x, square_size * 2.2))
        screen.blit(subtitle_surf, subtitle_rect)

        # --- 3. REORGANIZED BUTTONS ---
        # Perfectly spaced at 3.5, 4.5, 5.5, and 6.5
        self.buttons = {
            "Play": pygame.Rect(center_x - 100, square_size * 3.5, 200, 50),
            "Play with Timer": pygame.Rect(center_x - 125, square_size * 4.5, 250, 50),
            "Play vs CPU": pygame.Rect(center_x - 100, square_size * 5.5, 200, 50),
            "Exit": pygame.Rect(center_x - 100, square_size * 6.5, 200, 50)
        }

        mouse_pos = pygame.mouse.get_pos()

        for text, rect in self.buttons.items():
            color = (100, 200, 100) if rect.collidepoint(mouse_pos) else (50, 50, 50)

            pygame.draw.rect(screen, color, rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), rect, 3, border_radius=10)

            text_surf = self.button_font.render(text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

        # --- 4. THEME PREVIEW BUTTON ---
        # (Cleaned up the duplicate code that was causing double rendering)
        theme = view.themes[view.current_theme_index]
        preview_size = 10

        self.theme_button = pygame.Rect(screen.get_width() - 75, 15, 60, 60)
        pygame.draw.rect(screen, (45, 45, 45), self.theme_button, border_radius=5)
        pygame.draw.rect(screen, (200, 200, 200), self.theme_button, 1, border_radius=5)

        start_x = self.theme_button.x + 10
        start_y = self.theme_button.y + 10

        for r in range(4):
            for c in range(4):
                color = theme["light"] if (r + c) % 2 == 0 else theme["dark"]

                rect_x = start_x + (c * preview_size)
                rect_y = start_y + (r * preview_size)

                pygame.draw.rect(screen, color, (rect_x, rect_y, preview_size, preview_size))