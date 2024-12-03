import pytest

from src.game import Game


def test_game_initialization():
    game = Game()
    assert game.score == 0
    assert game.level == 1
    assert game.running == True
    assert game.paused == False
