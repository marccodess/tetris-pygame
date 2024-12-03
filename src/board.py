from typing import List, Optional, Tuple

from .constants import *
from .tetromino import Tetromino


class Board:
    """
    Represents the Tetris game board.

    Handles piece spawning, collision detection, piece locking,
    and line clearing mechanics.
    """

    def __init__(self) -> None:
        """
        Initialize an empty game board with dimensions defined in constants.
        """
        self.grid: List[List[Optional[Tuple[int, int, int]]]] = [
            [None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)
        ]
        self.current_piece: Optional[Tetromino] = None
        self.game_over: bool = False

    def spawn_piece(self) -> None:
        """
        Spawn a new Tetromino piece at the top of the board.

        Sets game_over to True if the new piece immediately collides.
        """
        self.current_piece = Tetromino()
        if self._check_collision():
            self.game_over = True

    def _check_collision(self) -> bool:
        """
        Check if the current piece collides with walls or other pieces.

        Returns:
            bool: True if collision detected, False otherwise
        """
        if not self.current_piece:
            return False

        shape = self.current_piece.shape
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    abs_x = self.current_piece.x + x
                    abs_y = self.current_piece.y + y
                    if (
                        abs_x < 0
                        or abs_x >= GRID_WIDTH
                        or abs_y >= GRID_HEIGHT
                        or (abs_y >= 0 and self.grid[abs_y][abs_x] is not None)
                    ):
                        return True
        return False

    def lock_piece(self) -> None:
        """
        Lock the current piece in place on the grid.
        """
        if not self.current_piece:
            return

        shape = self.current_piece.shape
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece.y + y][
                        self.current_piece.x + x
                    ] = self.current_piece.color

    def clear_lines(self) -> int:
        """
        Clear completed lines and return the number of lines cleared.

        Returns:
            int: Number of lines cleared
        """
        lines_cleared = 0
        y = GRID_HEIGHT - 1
        while y >= 0:
            if all(cell is not None for cell in self.grid[y]):
                del self.grid[y]
                self.grid.insert(0, [None] * GRID_WIDTH)
                lines_cleared += 1
            else:
                y -= 1
        return lines_cleared
