import random
from dataclasses import dataclass
from typing import List, Tuple

from .constants import *


@dataclass
class TetrominoData:
    """
    Data class representing the shape and color of a Tetromino piece.

    Attributes:
        shape (List[List[int]]): 2D array representing the piece's shape using 1s and 0s
        color (Tuple[int, int, int]): RGB color tuple for the piece
    """

    shape: List[List[int]]
    color: Tuple[int, int, int]


class Tetromino:
    """
    Represents a Tetris piece with its shape, color, and position.

    The class handles piece creation, rotation, and movement.
    """

    SHAPES: dict[str, TetrominoData] = {
        "I": TetrominoData([[1, 1, 1, 1]], CYAN),
        "O": TetrominoData([[1, 1], [1, 1]], YELLOW),
        "T": TetrominoData([[0, 1, 0], [1, 1, 1]], PURPLE),
        "L": TetrominoData([[1, 0], [1, 0], [1, 1]], ORANGE),
        "J": TetrominoData([[0, 1], [0, 1], [1, 1]], BLUE),
        "S": TetrominoData([[0, 1, 1], [1, 1, 0]], GREEN),
        "Z": TetrominoData([[1, 1, 0], [0, 1, 1]], RED),
    }

    def __init__(self) -> None:
        """
        Initialize a random Tetromino piece with a random shape and starting position.
        """
        self.shape_name: str = random.choice(list(self.SHAPES.keys()))
        self.data: TetrominoData = self.SHAPES[self.shape_name]
        self.shape: List[List[int]] = self.data.shape
        self.color: Tuple[int, int, int] = self.data.color
        self.x: int = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y: int = 0

    def rotate(self) -> None:
        """
        Rotate the piece 90 degrees clockwise.
        """
        self.shape = list(zip(*self.shape[::-1]))

    def move(self, dx: int, dy: int) -> None:
        """
        Move the piece by the specified delta values.

        Args:
            dx (int): Horizontal movement (-1 for left, 1 for right)
            dy (int): Vertical movement (typically 1 for down)
        """
        self.x += dx
        self.y += dy
