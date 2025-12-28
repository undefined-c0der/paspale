"""
Line chart plotter implementation.
"""

from typing import Optional

from ..base import BasePlotter
from ..colors import resolve_colors
from ..config import PlotConfig


class LinePlotter(BasePlotter):
    """
    Line chart plotter.

    Creates line charts with markers.

    Example:
        config = PlotConfig(
            output="trends.pdf",
            ylabel="Performance",
            legend=["Config A", "Config B"],
            colors="lines",
        )

        plotter = LinePlotter(config)
        plotter.load_csv("trends.csv")
        plotter.plot()
    """

    def draw(self) -> None:
        """Draw line chart."""
        if self.data is None:
            return

        # First column is x values, rest are y series
        x = self.data.iloc[:, 0].values
        y_data = self.data.iloc[:, 1:].values
        n_lines = y_data.shape[1]

        colors = resolve_colors(self.config.colors, n_lines)
        markers = ["o", "s", "^", "D", "v", "<", ">", "p", "h"]

        handles = []
        for i in range(n_lines):
            (line,) = self.ax.plot(
                x,
                y_data[:, i],
                marker=markers[i % len(markers)],
                color=colors[i],
                linewidth=2,
                markersize=8,
            )
            handles.append(line)

        self._handles = handles

    def add_legend(self) -> None:
        """Add legend for lines."""
        if self.config.legend and hasattr(self, "_handles"):
            self.fig.legend(
                self._handles,
                self.config.legend,
                loc=self.config.legend_loc,
                fontsize=self.config.font.legend,
                frameon=False,
            )
