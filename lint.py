#!/usr/bin/env python3
"""Linter for Connect Four game architecture.

Enforces:
- All source files live inside a layer directory
- Imports respect the forward dependency direction in src/README.md
- No file exceeds 300 lines
- Uses Python's ast module for parsing
"""

import ast
import os
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Layer order: cell_types, config, repo, service, runtime, ui, providers, utils
# Imports must flow forward only (can't import from later layers)
LAYERS = ["cell_types", "config", "repo", "service", "runtime", "ui", "providers", "utils"]

# Legal import dependencies per layer
LEGAL_IMPORTS = {
    "cell_types": [],
    "config": [],
    "repo": ["cell_types"],
    "service": ["cell_types", "config", "repo"],
    "runtime": ["cell_types", "config", "service", "ui", "providers"],
    "ui": ["cell_types", "config", "service", "providers"],
    "providers": [],
    "utils": [],
}


def get_layer(filepath: str) -> str:
    """Get the layer name from a file path."""
    parts = filepath.split(os.sep)
    if len(parts) >= 2 and parts[0] == "src":
        return parts[1]
    return ""


def check_file_structure(root: Path) -> List[Tuple[str, int, str]]:
    """Check that all source files are inside a layer directory."""
    violations = []
    
    for py_file in root.glob("src/**/*.py"):
        rel_path = str(py_file.relative_to(root))
        if rel_path in ("src/main.py", "src/__init__.py"):
            continue  # Allow main.py at src root
        
        parts = rel_path.split(os.sep)
        if len(parts) < 3:
            violations.append((rel_path, 1, "Source file must be inside a layer directory"))
            continue
        
        layer = parts[1]
        if layer not in LAYERS:
            violations.append((rel_path, 1, f"File is in '{layer}' which is not a valid layer"))
    
    return violations


def check_imports(root: Path) -> List[Tuple[str, int, str]]:
    """Check that imports respect layer dependency rules."""
    violations = []
    
    for py_file in root.glob("src/**/*.py"):
        if py_file.name == "__init__.py" and py_file.parent == root / "src":
            continue  # Skip src/__init__.py
        
        rel_path = str(py_file.relative_to(root))
        file_layer = get_layer(rel_path)
        
        if not file_layer or file_layer not in LEGAL_IMPORTS:
            continue
        
        try:
            with open(py_file, "r") as f:
                tree = ast.parse(f.read(), filename=str(py_file))
        except SyntaxError as e:
            violations.append((rel_path, e.lineno or 1, f"Syntax error: {e}"))
            continue
        
        legal_layers = LEGAL_IMPORTS.get(file_layer, [])
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module:
                    module_parts = node.module.split(".")
                    if module_parts[0] == "src" and len(module_parts) >= 2:
                        imported_layer = module_parts[1]
                        if imported_layer not in legal_layers:
                            violations.append((
                                rel_path,
                                node.lineno,
                                f"Import from '{imported_layer}' layer is not allowed from '{file_layer}' layer"
                            ))
    return violations


def check_line_counts(root: Path) -> List[Tuple[str, int, str]]:
    """Check that no file exceeds 300 lines."""
    violations = []
    
    for py_file in root.glob("src/**/*.py"):
        rel_path = str(py_file.relative_to(root))
        
        with open(py_file, "r") as f:
            lines = f.readlines()
        
        if len(lines) > 300:
            violations.append((rel_path, len(lines), f"File has {len(lines)} lines, max is 300"))
    
    return violations


def main() -> int:
    """Run linter checks and return exit code."""
    root = Path(__file__).parent
    
    all_violations = []
    all_violations.extend(check_file_structure(root))
    all_violations.extend(check_imports(root))
    all_violations.extend(check_line_counts(root))
    
    if not all_violations:
        print("All checks passed!")
        return 0
    
    # Sort by file, then line
    all_violations.sort(key=lambda x: (x[0], x[1]))
    
    print("Lint violations found:")
    for file_path, line_num, message in all_violations:
        print(f"  {file_path}:{line_num}: {message}")
    
    return 1


if __name__ == "__main__":
    sys.exit(main())
