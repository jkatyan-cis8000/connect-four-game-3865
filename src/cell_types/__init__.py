"""Cell types layer for Connect Four game.

Pure type definitions for the game.
"""

from enum import Enum
from typing import Tuple, List

# Player identifier
class Player(Enum):
    """Player identifier."""
    RED = "R"
    YELLOW = "Y"

# Cell state on the board
class Cell(Enum):
    """Cell state - EMPTY, RED, or YELLOW."""
    EMPTY = " "
    RED = "R"
    YELLOW = "Y"

# Board types
BoardRow = List[Cell]
Board = List[BoardRow]

# Position type for board coordinates
Position = Tuple[int, int]  # (row, col)

# Game state
class GameState(Enum):
    """Game state: win, draw, or ongoing."""
    WIN = "win"
    DRAW = "draw"
    ONGOING = "ongoing"
