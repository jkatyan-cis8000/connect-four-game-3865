"""Providers layer for Connect Four game.

Cross-cutting concerns: logging, telemetry, external connectors.
"""

import sys

def log(message: str) -> None:
    """Log a message to stdout."""
    print(f"[LOG] {message}")

def log_error(message: str) -> None:
    """Log an error message to stderr."""
    print(f"[ERROR] {message}", file=sys.stderr)
