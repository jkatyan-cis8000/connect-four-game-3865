"""Service layer for Connect Four game.

Contains business logic: win detection, valid moves, game state.
"""

from typing import List

from config import GAME_ROWS, GAME_COLS, WIN_LENGTH
from cell_types import Cell, Board, BoardRow

def create_board() -> Board:
    """Create an empty game board."""
    return [[Cell.EMPTY for _ in range(GAME_COLS)] for _ in range(GAME_ROWS)]

def is_valid_move(board: Board, col: int) -> bool:
    """Check if a move is valid (column is not full)."""
    if col < 0 or col >= GAME_COLS:
        return False
    return board[0][col] == Cell.EMPTY

def get_next_open_row(board: Board, col: int) -> int:
    """Get the next open row in a column."""
    for row in range(GAME_ROWS - 1, -1, -1):
        if board[row][col] == Cell.EMPTY:
            return row
    raise ValueError("Column is full")

def drop_piece(board: Board, col: int, player: Cell) -> int:
    """Drop a piece into the board. Returns the row where it landed."""
    if not is_valid_move(board, col):
        raise ValueError("Invalid move")
    row = get_next_open_row(board, col)
    board[row][col] = player
    return row

def check_win(board: Board, player: Cell) -> bool:
    """Check if the given player has won."""
    # Check horizontal
    for row in range(GAME_ROWS):
        for col in range(GAME_COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == player for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for row in range(GAME_ROWS - WIN_LENGTH + 1):
        for col in range(GAME_COLS):
            if all(board[row + i][col] == player for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (down-right)
    for row in range(GAME_ROWS - WIN_LENGTH + 1):
        for col in range(GAME_COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == player for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (up-right)
    for row in range(WIN_LENGTH - 1, GAME_ROWS):
        for col in range(GAME_COLS - WIN_LENGTH + 1):
            if all(board[row - i][col + i] == player for i in range(WIN_LENGTH)):
                return True
    
    return False

def is_board_full(board: Board) -> bool:
    """Check if the board is full (draw condition)."""
    return all(board[0][col] != Cell.EMPTY for col in range(GAME_COLS))

def get_game_state(board: Board, current_player: Cell) -> str:
    """Get the current game state (win, draw, or ongoing)."""
    if check_win(board, current_player):
        return "win"
    if is_board_full(board):
        return "draw"
    return "ongoing"
