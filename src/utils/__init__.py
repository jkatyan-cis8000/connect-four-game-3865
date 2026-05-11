"""Utils layer for Connect Four game.

Pure helper functions with no internal imports.
"""

from typing import List

def clear_screen() -> None:
    """Clear the terminal screen."""
    print("\033[2J\033[H", end="")

def format_board(board: List[List[str]]) -> str:
    """Format the board for display."""
    lines = []
    lines.append("  1 2 3 4 5 6 7  ")
    lines.append("  ---------------")
    
    for row in board:
        line = "| " + " ".join(cell if cell != " " else " " for cell in row) + " |"
        lines.append(line)
    
    lines.append("  ---------------")
    lines.append("  1 2 3 4 5 6 7  ")
    
    return "\n".join(lines)
