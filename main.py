import pygame

from src.game import Game


def main() -> None:
    """
    Main entry point for the Tetris game.

    Initializes pygame, creates a game instance, runs the game loop,
    and performs cleanup when the game exits.
    """
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()


if __name__ == "__main__":
    main()
