"""
PasPale - A unified plotting framework for academic papers.

Usage:
    from paspale import paspale, BarPlotter, PlotConfig

    # Quick plot
    paspale(data="results.csv", output="figure.pdf", ylabel="Speedup")

    # Using plotter class
    plotter = BarPlotter(PlotConfig(output="figure.pdf", ylabel="Speedup"))
    plotter.load_csv("results.csv")
    plotter.plot()
"""

from paspale.colors import ColorScheme, colors
from paspale.config import FigureSize, FontConfig, KDEConfig, PlotConfig
from paspale.paspale import paspale
from paspale.plotters import (
    BarPlotter,
    DualAxisPlotter,
    KDEPlotter,
    LinePlotter,
    StackedBarPlotter,
)

__version__ = "0.1.0"
__all__ = [
    # Main function
    "paspale",
    # Configuration
    "PlotConfig",
    "KDEConfig",
    "FontConfig",
    "FigureSize",
    # Colors
    "ColorScheme",
    "colors",
    # Plotters
    "BarPlotter",
    "StackedBarPlotter",
    "DualAxisPlotter",
    "LinePlotter",
    "KDEPlotter",
]
