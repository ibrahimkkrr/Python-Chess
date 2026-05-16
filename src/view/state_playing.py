import pygame


class ViewPlayingState:

    def __init__(self):
        self.flip_progress = 0.0

    def render(self, screen, square_size, engine, view, legal_moves):
        target = 1.0 if engine.turn == 'black' else 0.0

        if getattr(engine, 'is_ai_game', False):
            target = 0.0

        self.flip_progress += (target - self.flip_progress)

        is_flipped = self.flip_progress >= 0.5

        board_w = square_size * 8
        board_surface = pygame.Surface((board_w, board_w), pygame.SRCALPHA)
        board_surface.fill((40, 40, 40))

        theme = view.themes[view.current_theme_index]
        for row in range(8):
            for col in range(8):
                draw_row = 7 - row if is_flipped else row
                draw_col = 7 - col if is_flipped else col
                pixel_x = draw_col * square_size
                pixel_y = draw_row * square_size

                color = theme["light"] if (row + col) % 2 == 0 else theme["dark"]
                pygame.draw.rect(board_surface, color, (pixel_x, pixel_y, square_size, square_size))

                if (row, col) in legal_moves:
                    target_piece = engine.board.get_piece(row, col)
                    if target_piece is not None:
                        capture_overlay = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
                        capture_overlay.fill((255, 0, 0, 100))
                        board_surface.blit(capture_overlay, (pixel_x, pixel_y))

        for m_row, m_col in legal_moves:
            if engine.board.get_piece(m_row, m_col) is None:
                d_row = 7 - m_row if is_flipped else m_row
                d_col = 7 - m_col if is_flipped else m_col
                dot_surf = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
                pygame.draw.circle(dot_surf, (0, 0, 0, 80), (square_size // 2, square_size // 2), square_size // 6)
                # CHANGE: Draw to board_surface
                board_surface.blit(dot_surf, (d_col * square_size, d_row * square_size))

        for row in range(8):
            for col in range(8):
                piece = engine.board.get_piece(row, col)
                if piece:
                    draw_row = 7 - row if is_flipped else row
                    draw_col = 7 - col if is_flipped else col
                    pixel_x = draw_col * square_size
                    pixel_y = draw_row * square_size

                    color_prefix = 'w' if piece.color == 'white' else 'b'
                    piece_letter = 'N' if piece.name == 'Knight' else piece.name[0]
                    key = color_prefix + piece_letter

                    if key in view.images:
                        scaled_image = pygame.transform.smoothscale(
                            view.images[key], (square_size, square_size)
                        )
                        # CHANGE: Draw to board_surface
                        board_surface.blit(scaled_image, (pixel_x, pixel_y))

        scale_y = abs(self.flip_progress - 0.5) * 2
        if scale_y < 0.01: scale_y = 0.01  # Prevent a Pygame math crash!

        animated_height = int(board_w * scale_y)

        squished_board = pygame.transform.smoothscale(board_surface, (board_w, animated_height))
        y_offset = (board_w - animated_height) // 2

        screen.fill((30, 30, 30))
        screen.blit(squished_board, (0, y_offset))

        if getattr(engine, 'is_timed_game', False):
            white_y = (square_size * 8) - 50 if not is_flipped else 10
            black_y = 10 if not is_flipped else (square_size * 8) - 50
            self.draw_timer(engine.white_time, screen, square_size, view, white_y, engine.turn == 'white')
            self.draw_timer(engine.black_time, screen, square_size, view, black_y, engine.turn == 'black')



    def draw_timer(self,time_val, screen, square_size, view, y_pos, is_active):
            minutes = int(time_val // 60)
            seconds = int(time_val % 60)
            time_str = f"{minutes:02d}:{seconds:02d}"

            text_color = (100, 255, 100) if is_active else (200, 200, 200)
            text_surf = view.timer_font.render(time_str, True, text_color)

            box_rect = pygame.Rect((square_size * 8) - 100, y_pos, 90, 40)

            bg_surf = pygame.Surface((box_rect.width, box_rect.height))
            bg_surf.set_alpha(200)
            bg_surf.fill((20, 20, 20))
            screen.blit(bg_surf, box_rect.topleft)
            pygame.draw.rect(screen, text_color, box_rect, 2)

            text_rect = text_surf.get_rect(center=box_rect.center)
            screen.blit(text_surf, text_rect)

