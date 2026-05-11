"""UI layer for Connect Four game.

User-facing surfaces: CLI interface for displaying board and getting input.
"""

from typing import List

from config import RED_SYMBOL, YELLOW_SYMBOL
from cell_types import Cell, GameState
from service import check_win, is_board_full, get_game_state
from providers import log, log_error

def display_board(board: List[List[str]]) -> None:
    """Display the current board state."""
    print()
    print("  1 2 3 4 5 6 7  ")
    print("  ---------------")
    for row in board:
        line = "| " + " ".join(cell if cell != " " else " " for cell in row) + " |"
        print(line)
    print("  ---------------")
    print("  1 2 3 4 5 6 7  ")
    print()

def get_player_input(board: List[List[str]], current_player: Cell) -> int:
    """Get a valid column choice from the player."""
    player_name = RED_SYMBOL if current_player == Cell.RED else YELLOW_SYMBOL
    
    while True:
        try:
            col_input = input(f"Player {player_name}, choose a column (1-7): ").strip()
            col = int(col_input) - 1
            
            if col < 0 or col >= 7:
                log_error("Column must be between 1 and 7.")
                continue
            
            if board[0][col] != " ":
                log_error("Column is full. Choose another column.")
                continue
            
            return col
            
        except ValueError:
            log_error("Invalid input. Please enter a number between 1 and 7.")

def display_result(board: List[List[str]], game_state: str, current_player: Cell) -> None:
    """Display the game result."""
    display_board(board)
    
    if game_state == "win":
        player_name = RED_SYMBOL if current_player == Cell.RED else YELLOW_SYMBOL
        print(f"Player {player_name} wins!")
    elif game_state == "draw":
        print("It's a draw!")
    else:
        print("Game ongoing.")

def announce_turn(current_player: Cell) -> None:
    """Announce whose turn it is."""
    player_name = RED_SYMBOL if current_player == Cell.RED else YELLOW_SYMBOL
    print(f"\n--- Player {player_name}'s turn ---")
