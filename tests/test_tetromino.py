from typing import List, Tuple

import pytest

from src.constants import BLUE, CYAN, GREEN, ORANGE, PURPLE, RED, YELLOW
from src.tetromino import Tetromino


@pytest.fixture
def tetromino() -> Tetromino:
    """Fixture providing a fresh Tetromino instance for each test."""
    return Tetromino()


# Test all possible shapes
@pytest.mark.parametrize(
    "shape_name,expected_color",
    [
        ("I", CYAN),
        ("O", YELLOW),
        ("T", PURPLE),
        ("L", ORANGE),
        ("J", BLUE),
        ("S", GREEN),
        ("Z", RED),
    ],
)
def test_tetromino_shapes(
    shape_name: str, expected_color: Tuple[int, int, int]
) -> None:
    """Test creation of specific Tetromino shapes."""
    piece = Tetromino()
    piece.shape_name = shape_name
    piece.data = piece.SHAPES[shape_name]
    piece.shape = piece.data.shape
    piece.color = piece.data.color

    assert piece.color == expected_color
    assert len(piece.shape) > 0


def test_tetromino_creation(tetromino: Tetromino) -> None:
    """Test basic Tetromino initialization."""
    assert tetromino.shape is not None
    assert tetromino.color is not None
    assert isinstance(tetromino.x, int)
    assert isinstance(tetromino.y, int)
    assert tetromino.shape_name in Tetromino.SHAPES


@pytest.mark.parametrize("rotations", [1, 2, 3, 4])
def test_tetromino_rotation(tetromino: Tetromino, rotations: int) -> None:
    """Test Tetromino rotation for different numbers of turns."""
    original_shape = [tuple(row) for row in tetromino.shape]  # Deep copy

    # Perform rotations
    for _ in range(rotations):
        tetromino.rotate()

    # After 4 rotations, shape should be back to original
    if rotations == 4:
        assert tetromino.shape == original_shape
    else:
        assert tetromino.shape != original_shape


def test_tetromino_move(tetromino: Tetromino) -> None:
    """Test Tetromino movement."""
    original_x = tetromino.x
    original_y = tetromino.y

    # Test horizontal movement
    tetromino.move(1, 0)
    assert tetromino.x == original_x + 1
    assert tetromino.y == original_y

    # Test vertical movement
    tetromino.move(0, 1)
    assert tetromino.x == original_x + 1
    assert tetromino.y == original_y + 1


def test_get_positions(tetromino: Tetromino) -> None:
    """Test position calculations for Tetromino blocks."""
    positions = [
        (tetromino.x + x, tetromino.y + y)
        for y, row in enumerate(tetromino.shape)
        for x, cell in enumerate(row)
        if cell
    ]

    assert len(positions) > 0
    assert all(isinstance(pos, tuple) and len(pos) == 2 for pos in positions)
    assert all(isinstance(coord, int) for pos in positions for coord in pos)

    # Test that positions are within reasonable bounds
    for x, y in positions:
        assert -5 <= x <= 15  # Assuming standard Tetris board width
        assert -2 <= y <= 20  # Assuming standard Tetris board height
