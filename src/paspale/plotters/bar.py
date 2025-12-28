"""
Bar chart plotter implementation.
"""

from typing import List, Optional

from ..base import BasePlotter
from ..colors import resolve_colors
from ..config import PlotConfig


class BarPlotter(BasePlotter):
    """
    Grouped bar chart plotter.

    Creates grouped bar charts from CSV data where:
        - First column: group labels (e.g., workload names)
        - Remaining columns: values for each bar in the group

    Example:
        config = PlotConfig(
            output="comparison.pdf",
            ylabel="Speedup",
            legend=["Method A", "Method B", "Method C"],
        )

        plotter = BarPlotter(config)
        plotter.load_csv("results.csv")
        plotter.plot()
    """

    def __init__(self, config: Optional[PlotConfig] = None):
        super().__init__(config)
        self._all_xticks: List[List[int]] = []
        self._handles: List = []

    def draw(self) -> None:
        """Draw grouped bar chart."""
        xtick_beg = 0

        for idx, row in enumerate(self._data_matrix):
            # Skip first column (label), extract values
            values = [[v[0] for v in row[1:]]]
            n_bars = len(values[0])

            # Generate x positions
            xticks = list(range(xtick_beg, xtick_beg + len(values)))
            self._all_xticks.append(xticks)
            xtick_beg += len(values) + 1

            # Get colors
            colors = resolve_colors(self.config.colors, n_bars)

            # Draw bars
            for i, (val, color) in enumerate(zip(values[0], colors)):
                bar = self.ax.bar(
                    xticks[0] + i * self.config.bar_width / n_bars,
                    val,
                    width=self.config.bar_width / n_bars,
                    color=color,
                    edgecolor="black",
                    linewidth=0.5,
                )
                if idx == 0:
                    self._handles.append(bar[0])

        # Configure x-axis
        self.ax.set_xticks([])
        self.ax.xaxis.set_ticks_position("none")

        # Add group labels
        self._add_group_labels()

        # Remove box
        for spine in ["top", "right"]:
            self.ax.spines[spine].set_visible(False)

    def _add_group_labels(self) -> None:
        """Add group labels below bars."""
        if not self.config.labels and self.data is not None:
            # Use first column as labels
            labels = self.data.iloc[:, 0].tolist()
        else:
            labels = self.config.labels

        # Number of bars per group (columns - 1 for label column)
        n_bars = 1
        if self.data is not None and self.data.shape[1] > 1:
            n_bars = max(1, self.data.shape[1] - 1)

        single_width = self.config.bar_width / n_bars

        for xticks, label in zip(self._all_xticks, labels):
            # Place label at the left edge of the first bar in the group
            x = xticks[0] - single_width / 2
            self.ax.text(
                x,
                self.config.ylim_min,
                str(label),
                ha="left",
                va="top",
                fontsize=self.config.font.annotation,
                rotation=self.config.label_rotation,
            )

    def add_legend(self) -> None:
        """Add legend using bar handles."""
        if self.config.legend and self._handles:
            self.fig.legend(
                self._handles,
                self.config.legend,
                loc=self.config.legend_loc,
                ncol=self.config.legend_ncol,
                bbox_to_anchor=self.config.legend_anchor,
                frameon=False,
                fontsize=self.config.font.legend,
            )
