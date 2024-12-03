from typing import Optional

import pygame

from .board import Board
from .constants import *


class Game:
    """
    Main game class that handles the game loop, rendering, and user input.

    This class manages the overall game state, including score tracking,
    level progression, and game loop execution.
    """

    def __init__(self) -> None:
        """
        Initialize a new game instance.
        """
        self.screen: pygame.Surface
        self.clock: pygame.time.Clock
        self.board: Board
        self.score: int
        self.level: int
        self.running: bool
        self.paused: bool
        self.move_counter: int
        self.fall_speed: float

        self.init_game()

    def init_game(self) -> None:
        """
        Initialize or reset all game variables to their starting values.

        Sets up the display, clock, board, and game state variables.
        """
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pygame Tetris")
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.score = 0
        self.level = 1
        self.running = True
        self.paused = False
        self.move_counter = 0
        self.fall_speed = INITIAL_FALL_SPEED
        self.board.spawn_piece()

    def restart_game(self) -> None:
        """
        Restart the game by reinitializing all game variables.
        """
        self.init_game()

    def handle_input(self) -> None:
        """
        Process all pending pygame events and handle user input.

        Handles game exit, pause, and delegates gameplay inputs when appropriate.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                elif not self.paused:
                    self._handle_game_input(event)

    def _handle_game_input(self, event: pygame.event.Event) -> None:
        """
        Handle gameplay-specific keyboard inputs.

        Args:
            event (pygame.event.Event): The keyboard event to process
        """
        if self.board.game_over:
            if event.key == pygame.K_r:
                self.restart_game()
                return

        if event.key == pygame.K_LEFT:
            self.board.current_piece.move(-1, 0)
            if self.board._check_collision():
                self.board.current_piece.move(1, 0)
        elif event.key == pygame.K_RIGHT:
            self.board.current_piece.move(1, 0)
            if self.board._check_collision():
                self.board.current_piece.move(-1, 0)
        elif event.key == pygame.K_DOWN:
            self.board.current_piece.move(0, 1)
            if self.board._check_collision():
                self.board.current_piece.move(0, -1)
        elif event.key == pygame.K_UP:
            self.board.current_piece.rotate()
            if self.board._check_collision():
                for _ in range(3):  # Rotate back
                    self.board.current_piece.rotate()

    def update(self) -> None:
        """
        Update game state, including piece movement and scoring.

        Handles piece falling, collision detection, and line clearing.
        """
        if self.paused or self.board.game_over:
            return

        if self.board.current_piece:
            self.move_counter += self.fall_speed
            if self.move_counter >= MOVE_DELAY:
                self.move_counter = 0
                self.board.current_piece.move(0, 1)
                if self.board._check_collision():
                    self.board.current_piece.move(0, -1)
                    self.board.lock_piece()
                    lines_cleared = self.board.clear_lines()
                    self.update_score(lines_cleared)
                    self.board.spawn_piece()

    def update_score(self, lines_cleared: int) -> None:
        """
        Update the score based on lines cleared and handle level progression.

        Args:
            lines_cleared (int): Number of lines cleared in one move
        """
        points = {
            1: POINTS_SINGLE,
            2: POINTS_DOUBLE,
            3: POINTS_TRIPLE,
            4: POINTS_TETRIS,
        }
        if lines_cleared in points:
            self.score += points[lines_cleared] * self.level
            if self.score >= self.level * 1000:
                self.level += 1
                self.fall_speed *= LEVEL_SPEEDUP

    def draw(self) -> None:
        """
        Render the current game state to the screen.

        Draws the grid, pieces, and UI elements.
        """
        self.screen.fill(BLACK)
        self._draw_grid()
        self._draw_pieces()
        self._draw_ui()
        pygame.display.flip()

    def _draw_grid(self) -> None:
        """
        Draw the game grid including walls and background.
        """
        # Draw the border walls
        wall_rect = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        pygame.draw.rect(self.screen, WALL_COLOR, wall_rect)

        # Draw the play area background
        play_area = pygame.Rect(
            WALL_SIZE, WALL_SIZE, GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE
        )
        pygame.draw.rect(self.screen, BLACK, play_area)

        # Draw wall blocks
        for y in range(GRID_HEIGHT + 2):
            for x in range(GRID_WIDTH + 2):
                if x == 0 or x == GRID_WIDTH + 1 or y == 0 or y == GRID_HEIGHT + 1:
                    pygame.draw.rect(
                        self.screen,
                        WALL_COLOR,
                        (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                        0,
                    )
                    pygame.draw.rect(
                        self.screen,
                        BLACK,
                        (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                        1,
                    )

    def _draw_pieces(self) -> None:
        """
        Draw all pieces on the board, including fallen pieces and the active piece.
        """
        # Draw fallen pieces
        for y, row in enumerate(self.board.grid):
            for x, color in enumerate(row):
                if color:
                    pygame.draw.rect(
                        self.screen,
                        color,
                        (
                            (x + 1) * BLOCK_SIZE,
                            (y + 1) * BLOCK_SIZE,
                            BLOCK_SIZE,
                            BLOCK_SIZE,
                        ),
                    )
                    pygame.draw.rect(
                        self.screen,
                        BLACK,
                        (
                            (x + 1) * BLOCK_SIZE,
                            (y + 1) * BLOCK_SIZE,
                            BLOCK_SIZE,
                            BLOCK_SIZE,
                        ),
                        1,
                    )

        # Draw current piece
        if self.board.current_piece:
            piece = self.board.current_piece
            for y, row in enumerate(piece.shape):
                for x, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(
                            self.screen,
                            piece.color,
                            (
                                (piece.x + x + 1) * BLOCK_SIZE,
                                (piece.y + y + 1) * BLOCK_SIZE,
                                BLOCK_SIZE,
                                BLOCK_SIZE,
                            ),
                        )
                        pygame.draw.rect(
                            self.screen,
                            BLACK,
                            (
                                (piece.x + x + 1) * BLOCK_SIZE,
                                (piece.y + y + 1) * BLOCK_SIZE,
                                BLOCK_SIZE,
                                BLOCK_SIZE,
                            ),
                            1,
                        )

    def _draw_ui(self) -> None:
        """
        Draw UI elements including score, level, and game over screen.
        """
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        level_text = font.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(score_text, (WINDOW_WIDTH - 200, 20))
        self.screen.blit(level_text, (WINDOW_WIDTH - 200, 60))

        if self.board.game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.fill(BLACK)
            overlay.set_alpha(128)
            self.screen.blit(overlay, (0, 0))

            game_over_text = font.render("GAME OVER", True, RED)
            restart_text = font.render("Press R to Restart", True, WHITE)

            game_over_rect = game_over_text.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30)
            )
            restart_rect = restart_text.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30)
            )

            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(restart_text, restart_rect)

    def run(self) -> None:
        """
        Main game loop that continues until the game is exited.

        Handles the game timing and calls update and draw methods.
        """
        while self.running:
            self.clock.tick(FPS)
            self.handle_input()
            self.update()
            self.draw()
