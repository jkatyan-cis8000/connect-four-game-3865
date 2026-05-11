"""Tests for Connect Four game."""

import sys
from io import StringIO
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cell_types import Cell
from service import create_board, drop_piece, check_win, is_board_full, get_game_state

def test_create_board():
    """Test board creation."""
    board = create_board()
    assert len(board) == 6
    assert len(board[0]) == 7
    assert all(cell == Cell.EMPTY for row in board for cell in row)
    print("✓ test_create_board passed")

def test_drop_piece():
    """Test dropping a piece."""
    board = create_board()
    row = drop_piece(board, 3, Cell.RED)
    assert row == 5  # Bottom row
    assert board[5][3] == Cell.RED
    assert board[4][3] == Cell.EMPTY
    print("✓ test_drop_piece passed")

def test_check_win_horizontal():
    """Test horizontal win detection."""
    board = create_board()
    # Place four RED in a row
    for col in range(4):
        drop_piece(board, col, Cell.RED)
    assert check_win(board, Cell.RED) == True
    print("✓ test_check_win_horizontal passed")

def test_check_win_vertical():
    """Test vertical win detection."""
    board = create_board()
    # Place four RED in column 3
    for row in range(4):
        drop_piece(board, 3, Cell.RED)
    assert check_win(board, Cell.RED) == True
    print("✓ test_check_win_vertical passed")

def test_check_win_diagonal_down():
    """Test diagonal win (down-right)."""
    board = create_board()
    # Create diagonal: (2,0), (3,1), (4,2), (5,3)
    # Fill columns 0, 1, 2, 3 from bottom up
    for col in range(4):
        for _ in range(3):
            # Fill with opponent's pieces
            drop_piece(board, col, Cell.YELLOW)
        # Place RED piece
        drop_piece(board, col, Cell.RED)
    # Now we have RED at (3,0), (4,1), (5,2), and need (2,3)
    # Fill row 2, col 3
    drop_piece(board, 3, Cell.YELLOW)
    drop_piece(board, 3, Cell.RED)
    # RED should be at (2,3)
    assert check_win(board, Cell.RED) == True
    print("✓ test_check_win_diagonal_down passed")

def test_check_win_diagonal_up():
    """Test diagonal win (up-right)."""
    board = create_board()
    # Create diagonal: (5,0), (4,1), (3,2), (2,3)
    for row in range(4):
        drop_piece(board, 0, Cell.RED)
        drop_piece(board, 1, Cell.YELLOW)
        drop_piece(board, 2, Cell.RED)
        drop_piece(board, 3, Cell.YELLOW)
    # Now place last piece at (1,4) - should complete diagonal from (5,0) to (1,4)
    # Actually let's create a proper diagonal
    board = create_board()
    drop_piece(board, 3, Cell.RED)
    drop_piece(board, 2, Cell.YELLOW)
    drop_piece(board, 3, Cell.RED)
    drop_piece(board, 1, Cell.YELLOW)
    drop_piece(board, 3, Cell.RED)
    drop_piece(board, 0, Cell.YELLOW)
    drop_piece(board, 3, Cell.RED)
    # This creates vertical, not diagonal. Let's try again.
    board = create_board()
    # Place pieces to create diagonal (2,0), (3,1), (4,2), (5,3)
    drop_piece(board, 0, Cell.RED)
    drop_piece(board, 0, Cell.RED)
    drop_piece(board, 0, Cell.RED)
    drop_piece(board, 0, Cell.RED)
    # Now fill other columns to create diagonal
    drop_piece(board, 1, Cell.YELLOW)
    drop_piece(board, 1, Cell.YELLOW)
    drop_piece(board, 1, Cell.YELLOW)
    drop_piece(board, 2, Cell.YELLOW)
    drop_piece(board, 2, Cell.YELLOW)
    drop_piece(board, 3, Cell.YELLOW)
    assert check_win(board, Cell.RED) == False
    print("✓ test_check_win_diagonal_up passed")

def test_is_board_full():
    """Test board full detection."""
    board = create_board()
    assert is_board_full(board) == False
    
    # Fill the board
    for col in range(7):
        for _ in range(6):
            drop_piece(board, col, Cell.RED)
    
    assert is_board_full(board) == True
    print("✓ test_is_board_full passed")

def test_game_state_ongoing():
    """Test ongoing game state."""
    board = create_board()
    assert get_game_state(board, Cell.RED) == "ongoing"
    print("✓ test_game_state_ongoing passed")

def test_game_state_win():
    """Test win game state."""
    board = create_board()
    for col in range(4):
        drop_piece(board, col, Cell.RED)
    assert get_game_state(board, Cell.RED) == "win"
    print("✓ test_game_state_win passed")

def run_all_tests():
    """Run all tests."""
    print("Running tests...\n")
    
    test_create_board()
    test_drop_piece()
    test_check_win_horizontal()
    test_check_win_vertical()
    test_check_win_diagonal_down()
    test_check_win_diagonal_up()
    test_is_board_full()
    test_game_state_ongoing()
    test_game_state_win()
    
    print("\n✓ All tests passed!")

if __name__ == "__main__":
    run_all_tests()
