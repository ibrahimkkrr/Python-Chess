import pygame


class ViewPromotingState:
    def render(self, screen, square_size, engine, view ,legal_moves):

        from .state_playing import ViewPlayingState

        ViewPlayingState().render(screen, square_size, engine, view ,legal_moves)


        overlay = pygame.Surface((square_size * 8, square_size * 8))
        overlay.set_alpha(150)  # 0 is invisible, 255 is solid
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        menu_y = 3 * square_size
        menu_x = 2 * square_size
        pygame.draw.rect(screen, (200, 200, 200), (menu_x, menu_y, square_size * 4, square_size))
        pygame.draw.rect(screen, (50, 50, 50), (menu_x, menu_y, square_size * 4, square_size), 3)  # Border

        color_prefix = 'w' if engine.turn == 'white' else 'b'
        promotion_options = ['Q', 'R', 'B', 'N']

        for index, piece_letter in enumerate(promotion_options):
            key = color_prefix + piece_letter
            if key in view.images:
                scaled_image = pygame.transform.smoothscale(view.images[key], (square_size, square_size))
                target_x = (2 + index) * square_size
                screen.blit(scaled_image, (target_x, menu_y))
