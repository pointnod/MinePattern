"""Utilities for MinePattern v1.0.0 - Color conversion and validation.

All functions are type-annotated for clarity and IDE support.
"""

from typing import Tuple
import re

RGBColor = Tuple[int, int, int]

def hex_to_rgb(hex_color: str) -> RGBColor:
    """Convert hex color string to RGB tuple.

    Args:
        hex_color: Hex string like '#RRGGBB' or 'RRGGBB'.

    Returns:
        RGB tuple (R, G, B).

    Raises:
        ValueError: Invalid hex format.
    """
    hex_color = hex_color.lstrip('#')
    if not re.match(r'^[0-9A-Fa-f]{6}$', hex_color):
        raise ValueError(f"Invalid hex color: {hex_color}")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb: RGBColor) -> str:
    """Convert RGB tuple to hex string.

    Args:
        rgb: RGB tuple.

    Returns: 
        Hex string '#RRGGBB'.
    """
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}".upper()

def clamp(value: int, min_val: int = 0, max_val: int = 255) -> int:
    """Clamp value between min and max.

    Args:
        value: Value to clamp.
        min_val: Minimum value.
        max_val: Maximum value.

    Returns:
        Clamped value.
    """
    return max(min_val, min(max_val, value))

