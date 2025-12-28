"""
Stacked bar chart plotter implementation.
"""

from typing import Optional

import numpy as np

from ..base import BasePlotter
from ..colors import resolve_colors
from ..config import PlotConfig


class StackedBarPlotter(BasePlotter):
    """
    Stacked bar chart plotter.

    Creates stacked bar charts where values are stacked on top of each other.

    Example:
        config = PlotConfig(
            output="breakdown.pdf",
            ylabel="Energy",
            legend=["Compute", "Memory", "IO"],
            colors="breakdown",
        )

        plotter = StackedBarPlotter(config)
        plotter.load_csv("energy.csv")
        plotter.plot()
    """

    def draw(self) -> None:
        """Draw stacked bar chart."""
        if self.data is None:
            return

        # First column is labels, rest are values
        labels = self.data.iloc[:, 0].tolist()
        values = self.data.iloc[:, 1:].values
        n_categories = values.shape[1]

        x = np.arange(len(labels))
        width = 0.6

        colors = resolve_colors(self.config.colors, n_categories)

        bottom = np.zeros(len(labels))
        handles = []

        for i in range(n_categories):
            bar = self.ax.bar(
                x,
                values[:, i],
                width,
                bottom=bottom,
                color=colors[i],
                edgecolor="black",
                linewidth=0.5,
            )
            handles.append(bar[0])
            bottom += values[:, i]

        # Hide x-axis ticks
        self.ax.set_xticks([])
        self.ax.xaxis.set_ticks_position("none")

        # Add labels using ax.text (consistent with BarPlotter)
        for i, label in enumerate(labels):
            x_pos = x[i] - width / 2
            self.ax.text(
                x_pos,
                self.config.ylim_min,
                str(label),
                ha="left",
                va="top",
                fontsize=self.config.font.annotation,
                rotation=self.config.label_rotation,
            )

        self._handles = handles

    def add_legend(self) -> None:
        """Add legend for stacked bars."""
        if self.config.legend and hasattr(self, "_handles"):
            self.fig.legend(
                self._handles,
                self.config.legend,
                loc=self.config.legend_loc,
                ncol=self.config.legend_ncol,
                bbox_to_anchor=self.config.legend_anchor,
                fontsize=self.config.font.legend,
                frameon=False,
            )
