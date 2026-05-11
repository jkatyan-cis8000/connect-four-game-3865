"""Runtime layer for Connect Four game.

Game orchestration: manages game state, player turns, and game loop.
"""

from typing import List

from config import GAME_ROWS, GAME_COLS, RED_SYMBOL, YELLOW_SYMBOL
from cell_types import Cell, GameState
from service import create_board, drop_piece, check_win, is_board_full, get_game_state
from ui import display_board, get_player_input, announce_turn, display_result
from providers import log

class ConnectFourGame:
    """Main game class that orchestrates the Connect Four game."""
    
    def __init__(self):
        """Initialize the game."""
        # Internal board with Cell types
        self.board = create_board()
        # UI board with strings for display
        self.ui_board = [[" " for _ in range(GAME_COLS)] for _ in range(GAME_ROWS)]
        self.current_player = Cell.RED
        self.game_state = GameState.ONGOING
        self.players = [Cell.RED, Cell.YELLOW]
    
    def switch_player(self) -> None:
        """Switch to the next player."""
        self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]
    
    def play_turn(self) -> None:
        """Play a single turn."""
        announce_turn(self.current_player)
        display_board(self.ui_board)
        
        col = get_player_input(self.ui_board, self.current_player)
        
        # Update the service board
        row = drop_piece(self.board, col, self.current_player)
        # Update the UI board (convert Cell to string)
        self.ui_board[row][col] = self.current_player.value
        
        # Update game state
        if check_win(self.board, self.current_player):
            self.game_state = "win"
        elif is_board_full(self.board):
            self.game_state = "draw"
        else:
            self.game_state = "ongoing"
    
    def run(self) -> None:
        """Run the game loop."""
        log("Game started")
        
        print("Welcome to Connect Four!")
        print(f"Player {RED_SYMBOL} vs Player {YELLOW_SYMBOL}")
        print("Get four in a row to win!\n")
        
        while self.game_state == "ongoing":
            self.play_turn()
            
            if self.game_state != GameState.ONGOING:
                break
            
            self.switch_player()
        
        display_result(self.ui_board, self.game_state, self.current_player)
        print("Game over!")

def main() -> None:
    """Entry point for the game."""
    game = ConnectFourGame()
    game.run()

if __name__ == "__main__":
    main()
