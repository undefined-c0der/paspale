"""
Dual-axis plotter implementation.
"""

from typing import Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ..base import BasePlotter
from ..colors import resolve_colors
from ..config import PlotConfig


class DualAxisPlotter(BasePlotter):
    """
    Dual Y-axis plotter.

    Creates plots with two Y-axes, typically bars on left and lines on right.

    Requires two DataFrames:
        - Primary data: loaded via load_csv()
        - Secondary data: loaded via load_secondary()

    Example:
        config = PlotConfig(
            output="bandwidth_missrate.pdf",
            ylabel="Bandwidth (GB/s)",
            ylim=100,
        )

        plotter = DualAxisPlotter(config)
        plotter.load_csv("bandwidth.csv")
        plotter.load_secondary("missrate.csv", ylabel="Miss Rate", ylim=1.0)
        plotter.plot()
    """

    def __init__(self, config: Optional[PlotConfig] = None):
        super().__init__(config)
        self.ax2: Optional[plt.Axes] = None
        self.secondary_data: Optional[np.ndarray] = None
        self.secondary_ylabel: str = ""
        self.secondary_ylim: float = 1.0

    def load_secondary(
        self,
        path: str,
        ylabel: str = "",
        ylim: float = 1.0,
    ) -> "DualAxisPlotter":
        """
        Load secondary axis data.

        Args:
            path: Path to CSV file
            ylabel: Label for secondary Y-axis
            ylim: Upper limit for secondary Y-axis

        Returns:
            self for chaining
        """
        data = pd.read_csv(path)
        self.secondary_data = data.iloc[:, 1:].values
        self.secondary_ylabel = ylabel
        self.secondary_ylim = ylim
        return self

    def setup_figure(self) -> Tuple[plt.Figure, plt.Axes]:
        """Create figure with dual axes."""
        self.fig, self.ax = plt.subplots(figsize=self.config.size)
        self.ax2 = self.ax.twinx()
        return self.fig, self.ax

    def draw(self) -> None:
        """Draw bars on primary axis, lines on secondary."""
        # Draw bars (similar to BarPlotter)
        if self.data is not None:
            labels = self.data.iloc[:, 0].tolist()
            values = self.data.iloc[:, 1:].values

            x = np.arange(len(labels))
            n_bars = values.shape[1]
            width = 0.8 / n_bars

            colors = resolve_colors(self.config.colors, n_bars)

            for i in range(n_bars):
                self.ax.bar(
                    x + i * width - 0.4 + width / 2,
                    values[:, i],
                    width,
                    color=colors[i],
                    edgecolor="black",
                    linewidth=0.5,
                )

            # Hide x-axis ticks
            self.ax.set_xticks([])
            self.ax.xaxis.set_ticks_position("none")

            # Add labels using ax.text (consistent with BarPlotter)
            for i, label in enumerate(labels):
                x_pos = x[i] - 0.4
                self.ax.text(
                    x_pos,
                    self.config.ylim_min,
                    str(label),
                    ha="left",
                    va="top",
                    fontsize=self.config.font.annotation,
                    rotation=self.config.label_rotation,
                )

        # Draw lines on secondary axis
        if self.secondary_data is not None and self.ax2 is not None:
            x = np.arange(self.secondary_data.shape[0])
            line_colors = resolve_colors("lines", self.secondary_data.shape[1])

            for i in range(self.secondary_data.shape[1]):
                self.ax2.plot(
                    x,
                    self.secondary_data[:, i],
                    marker="o",
                    color=line_colors[i],
                    linewidth=2,
                    markersize=6,
                )

    def setup_axes(self) -> None:
        """Configure both axes."""
        super().setup_axes()

        if self.ax2 is not None:
            self.ax2.set_ylabel(
                self.secondary_ylabel,
                fontsize=self.config.font.label,
            )
            self.ax2.set_ylim(0, self.secondary_ylim)
            self.ax2.tick_params(axis="y", labelsize=self.config.font.tick)
