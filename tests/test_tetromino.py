import pytest

from src.tetromino import Tetromino


def test_tetromino_creation():
    piece = Tetromino()
    assert piece.shape is not None
    assert piece.color is not None
    assert hasattr(piece, "x")
    assert hasattr(piece, "y")


def test_tetromino_rotation():
    piece = Tetromino()
    original_shape = piece.shape.copy()
    piece.rotate()
    assert piece.shape != original_shape


def test_get_positions():
    tetromino = Tetromino()
    positions = [
        (tetromino.x + x, tetromino.y + y)
        for y, row in enumerate(tetromino.shape)
        for x, cell in enumerate(row)
        if cell
    ]
    assert len(positions) > 0
    assert all(isinstance(pos, tuple) and len(pos) == 2 for pos in positions)
    assert all(isinstance(coord, int) for pos in positions for coord in pos)
