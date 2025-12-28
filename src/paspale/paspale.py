"""
Main entry point function for quick plotting.
"""

from typing import List, Optional, Tuple, Union

import pandas as pd

from .config import PlotConfig
from .plotters.bar import BarPlotter


def paspale(
    data: Union[str, pd.DataFrame],
    output: str,
    ylabel: str = "",
    legend: Optional[List[str]] = None,
    ylim: Optional[float] = None,
    colors: Union[str, List[str]] = "primary",
    size: Tuple[float, float] = (14, 4.5),
    **kwargs,
):
    """
    Quick bar chart plotting function.

    This is the simplest way to create a plot with paspale.
    For more control, use the plotter classes directly.

    Args:
        data: Path to CSV file or pandas DataFrame
        output: Output file path
        ylabel: Y-axis label
        legend: List of legend labels
        ylim: Y-axis upper limit
        colors: Color scheme name or list of colors
        size: Figure size (width, height)
        **kwargs: Additional PlotConfig options

    Returns:
        Tuple of (figure, axes)

    Example:
        # From CSV
        paspale(
            data="results.csv",
            output="comparison.pdf",
            ylabel="Speedup",
            legend=["Baseline", "Optimized", "Ours"],
            ylim=6.0,
        )

        # From DataFrame
        import pandas as pd
        df = pd.read_csv("results.csv")
        paspale(
            data=df,
            output="comparison.pdf",
            ylabel="Speedup",
            legend=["A", "B", "C"],
        )
    """
    config = PlotConfig(
        output=output,
        ylabel=ylabel,
        legend=legend or [],
        ylim=ylim,
        colors=colors,
        size=size,
        **kwargs,
    )

    plotter = BarPlotter(config)

    if isinstance(data, str):
        plotter.load_csv(data)
    else:
        plotter.load_data(data)

    return plotter.plot()
