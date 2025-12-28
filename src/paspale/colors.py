"""
Color schemes for paspale.

Provides predefined color palettes suitable for academic papers.
"""

from dataclasses import dataclass
from typing import List, Union


@dataclass(frozen=True)
class ColorScheme:
    """
    Predefined color schemes.

    Attributes:
        PRIMARY: 6-color pastel palette for general use
        EXTENDED: 11-color palette for more categories
        GRADIENT: Blue gradient for sequential data (e.g., ablations)
        BREAKDOWN: 3-color palette for breakdowns
        LINES: Colors optimized for line charts
    """

    PRIMARY: tuple = (
        "#fbb4ae",  # Light red
        "#b3e2cd",  # Light green
        "#fdcdac",  # Light orange
        "#cbd5e8",  # Light blue
        "#bdbdbd",  # Gray
        "#e5d8bd",  # Light brown
    )

    EXTENDED: tuple = PRIMARY + (
        "#a6cee3",  # Soft blue
        "#ffb3c6",  # Soft pink
        "#b2df8a",  # Soft green
        "#ffe6a7",  # Soft yellow
        "#cab2d6",  # Soft purple
    )

    GRADIENT: tuple = (
        "#b3e2cd",  # Base
        "#efedf8",
        "#e3e5f6",
        "#d7ddef",
        "#cbd5e8",
        "#bdbdbd",
    )

    BREAKDOWN: tuple = (
        "#fbb4ae",
        "#b3e2cd",
        "#fdcdac",
    )

    LINES: tuple = (
        "#000000",  # Black
        "#007700",  # Dark green
        "#666666",  # Dark gray
        "#0077bb",  # Blue
        "#cc3311",  # Red
        "#ee7733",  # Orange
    )


# Global instance for convenience
colors = ColorScheme()


def get_colors(n: int, scheme: str = "primary") -> List[str]:
    """
    Get n colors from the specified scheme.

    Args:
        n: Number of colors needed
        scheme: Color scheme name ("primary", "extended", "gradient", "breakdown", "lines")

    Returns:
        List of color hex codes

    Example:
        >>> get_colors(3)
        ['#fbb4ae', '#b3e2cd', '#fdcdac']
        >>> get_colors(2, "lines")
        ['#000000', '#007700']
    """
    schemes = {
        "primary": colors.PRIMARY,
        "extended": colors.EXTENDED,
        "gradient": colors.GRADIENT,
        "breakdown": colors.BREAKDOWN,
        "lines": colors.LINES,
    }

    palette = schemes.get(scheme.lower(), colors.PRIMARY)

    # Cycle colors if n > len(palette)
    return [palette[i % len(palette)] for i in range(n)]


def resolve_colors(spec: Union[str, List[str]], n: int) -> List[str]:
    """
    Resolve color specification to a list of colors.

    Args:
        spec: Either a scheme name or a list of colors
        n: Number of colors needed

    Returns:
        List of color hex codes
    """
    if isinstance(spec, str):
        return get_colors(n, spec)
    elif isinstance(spec, (list, tuple)):
        return [spec[i % len(spec)] for i in range(n)]
    else:
        return get_colors(n, "primary")
