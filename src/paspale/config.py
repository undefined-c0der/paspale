"""
Configuration classes for paspale.

All configuration is done through dataclasses with sensible defaults.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Union


@dataclass
class FontConfig:
    """
    Font size configuration.

    All sizes are in points (pt).
    """

    label: int = 32  # Axis labels
    tick: int = 21  # Tick labels
    legend: int = 32  # Legend text
    title: int = 32  # Title text
    annotation: int = 26  # Annotations

    # Font family
    family: str = "Times New Roman"


@dataclass
class PlotConfig:
    """
    Configuration for bar charts and similar plots.

    Example:
        config = PlotConfig(
            output="figures/comparison.pdf",
            ylabel="Speedup",
            ylim=6.0,
            legend=["Method A", "Method B"],
        )
    """

    # === Required ===
    output: str = ""  # Output file path

    # === Figure Size ===
    size: Tuple[float, float] = (14, 4.5)  # (width, height) in inches

    # === Axis Configuration ===
    xlabel: str = ""
    ylabel: str = ""
    ylim: Optional[float] = None  # Y-axis upper limit
    ylim_min: float = 0.0  # Y-axis lower limit
    xlim: Optional[Tuple[float, float]] = None

    # === Scale ===
    log_scale: bool = False

    # === Ticks ===
    yticks: Optional[int] = 7  # Number of Y ticks
    ytick_format: str = "{:.1f}"  # Format string for Y tick labels
    # Special formats: "{:.0%}" for percentage

    # === Legend ===
    legend: List[str] = field(default_factory=list)
    legend_loc: str = "lower center"
    legend_ncol: Optional[int] = None  # None = auto (same as legend count)
    legend_anchor: Tuple[float, float] = (0.5, -0.1)

    # === Labels (for grouped bar charts) ===
    labels: List[str] = field(default_factory=list)  # X-axis group labels
    label_rotation: float = -15

    # === Colors ===
    colors: Union[str, List[str]] = "primary"  # Scheme name or list

    # === Bar Chart Specific ===
    bar_width: float = 1.3

    # === Font ===
    font: FontConfig = field(default_factory=FontConfig)

    # === Layout ===
    tight_rect: Tuple[float, float, float, float] = (-0.005, 0.05, 1.005, 1.005)

    def __post_init__(self):
        """Validate configuration."""
        if self.legend_ncol is None and self.legend:
            self.legend_ncol = len(self.legend)


@dataclass
class KDEConfig:
    """
    Configuration for KDE (Kernel Density Estimation) plots.

    Example:
        config = KDEConfig(
            output="figures/distribution.pdf",
            xlabel="Value",
            ylabel="Density",
        )
    """

    # === Required ===
    output: str = ""

    # === Figure Size ===
    size: Tuple[float, float] = (12, 7)

    # === Axis Configuration ===
    xlabel: str = "Value"
    ylabel: str = "Density"
    xlim: Optional[Tuple[float, float]] = None

    # === Style ===
    fill: bool = True
    alpha: float = 0.4
    use_percentage: bool = False  # Format Y as percentage

    # === Legend ===
    legend: List[str] = field(default_factory=list)
    legend_loc: str = "upper right"

    # === Colors ===
    colors: Union[str, List[str]] = "extended"

    # === Font ===
    font: FontConfig = field(default_factory=FontConfig)

    # === Layout ===
    tight_rect: Tuple[float, float, float, float] = (0, 0, 1, 1)

    # === Output ===
    format: str = "pdf"  # Output format
    dpi: int = 300


# === Preset Sizes ===


class FigureSize:
    """Common figure sizes for academic papers."""

    FULL_WIDTH = (14, 4.5)  # Full column width
    HALF_WIDTH = (7, 4.5)  # Half column width
    DOUBLE_WIDE = (28, 4.5)  # Double width
    TALL = (14, 6)  # Taller figure
    SQUARE = (8, 8)  # Square figure

    @classmethod
    def full(cls, height: float = 4.5) -> Tuple[float, float]:
        """Full width with custom height."""
        return (14, height)

    @classmethod
    def double(cls, height: float = 4.5) -> Tuple[float, float]:
        """Double width with custom height."""
        return (28, height)
