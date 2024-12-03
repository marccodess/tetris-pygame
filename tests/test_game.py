from unittest.mock import Mock, patch

import pygame
import pytest

from src.constants import POINTS_DOUBLE, POINTS_SINGLE, POINTS_TETRIS
from src.game import Game


@pytest.fixture
def game() -> Game:
    """Fixture providing a fresh Game instance for each test."""
    pygame.init()
    game = Game()
    yield game
    pygame.quit()


def test_game_initialization(game: Game) -> None:
    """Test initial game state."""
    assert game.score == 0
    assert game.level == 1
    assert game.running is True
    assert game.paused is False
    assert game.move_counter == 0
    assert hasattr(game, "board")
    assert hasattr(game, "screen")
    assert hasattr(game, "clock")


def test_game_restart(game: Game) -> None:
    """Test game restart functionality."""
    # Modify game state
    game.score = 1000
    game.level = 5
    game.paused = True

    # Restart game
    game.restart_game()

    # Verify reset state
    assert game.score == 0
    assert game.level == 1
    assert game.paused is False


@pytest.mark.parametrize(
    "lines_cleared,expected_score",
    [
        (1, POINTS_SINGLE),
        (2, POINTS_DOUBLE),
        (4, POINTS_TETRIS),
    ],
)
def test_score_calculation(game: Game, lines_cleared: int, expected_score: int) -> None:
    """Test score calculation for different numbers of lines cleared."""
    initial_level = game.level
    game.update_score(lines_cleared)
    assert game.score == expected_score * initial_level


@patch("pygame.event.get")
def test_game_pause(mock_event_get: Mock, game: Game) -> None:
    """Test game pause functionality."""
    # Mock pygame event for pressing pause key
    mock_event = Mock()
    mock_event.type = pygame.KEYDOWN
    mock_event.key = pygame.K_p
    mock_event_get.return_value = [mock_event]

    initial_pause_state = game.paused
    game.handle_input()
    assert game.paused != initial_pause_state


def test_level_progression(game: Game) -> None:
    """Test level progression based on score."""
    initial_fall_speed = game.fall_speed

    # Score enough points to trigger level up
    game.score = 1000
    game.update_score(4)  # Clear tetris to trigger level check

    assert game.level == 2
    assert game.fall_speed != initial_fall_speed
