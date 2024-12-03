# Window Settings
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
BORDER_WIDTH = 1  # Width of block borders
WALL_SIZE = BLOCK_SIZE  # Size of the border walls

# Calculate window size including walls
WINDOW_WIDTH = (GRID_WIDTH + 2) * BLOCK_SIZE  # +2 for walls
WINDOW_HEIGHT = (GRID_HEIGHT + 2) * BLOCK_SIZE  # +2 for walls

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
WALL_COLOR = (169, 169, 169)  # Light gray for walls

# Piece Colors - Adjusted to match the image
CYAN = (0, 255, 255)  # I piece - Light Blue
RED = (255, 0, 0)  # Z piece
GREEN = (0, 255, 0)  # S piece
YELLOW = (255, 255, 0)  # O piece
BLUE = (0, 0, 255)  # J piece
ORANGE = (255, 165, 0)  # L piece
PURPLE = (128, 0, 128)  # T piece

# Game Settings
FPS = 60
MOVE_DELAY = 30  # Frames between each downward movement
INITIAL_FALL_SPEED = 0.5  # Reduced from 1.0
LEVEL_SPEEDUP = 0.9  # Changed from 0.8 for slower progression

# Scoring
POINTS_SINGLE = 100
POINTS_DOUBLE = 300
POINTS_TRIPLE = 500
POINTS_TETRIS = 800
