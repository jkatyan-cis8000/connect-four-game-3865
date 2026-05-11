"""Repo layer for Connect Four game.

Data access layer - currently minimal as the game stores state in memory.
"""

from typing import List

from config import GAME_ROWS, GAME_COLS

# Board representation (internal to repo)
BoardRow = List[str]
Board = List[BoardRow]

def create_board() -> Board:
    """Create an empty board."""
    return [[" " for _ in range(GAME_COLS)] for _ in range(GAME_ROWS)]

def get_cell(board: Board, row: int, col: int) -> str:
    """Get the value of a cell."""
    return board[row][col]

def set_cell(board: Board, row: int, col: int, value: str) -> None:
    """Set the value of a cell."""
    board[row][col] = value

def copy_board(board: Board) -> Board:
    """Create a deep copy of the board."""
    return [row[:] for row in board]
