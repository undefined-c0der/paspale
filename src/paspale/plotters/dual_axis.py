"""
Dual-axis plotter implementation.
"""

from typing import List, Optional, Tuple, Type

import matplotlib.pyplot as plt

from ..base import BasePlotter
from ..config import PlotConfig


class DualAxisPlotter(BasePlotter):
    """
    Dual Y-axis plotter using composition of two sub-plotters.

    Creates plots with two Y-axes by combining any two plotter types.
    The primary plotter draws on the left axis, and the secondary plotter
    draws on the right axis.

    Example:
        from paspale import DualAxisPlotter, BarPlotter, LinePlotter, PlotConfig

        # Define configs for each axis
        primary_config = PlotConfig(
            output="dual_plot.pdf",
            ylabel="Bandwidth (GB/s)",
            ylim=100,
            legend=["Method A", "Method B"],
        )

        secondary_config = PlotConfig(
            ylabel="Miss Rate",
            ylim=1.0,
        )

        # Create dual-axis plotter with two sub-plotters
        plotter = DualAxisPlotter(
            primary=BarPlotter(primary_config),
            secondary=LinePlotter(secondary_config),
        )

        # Load data for each plotter
        plotter.primary.load_csv("bandwidth.csv")
        plotter.secondary.load_csv("missrate.csv")

        # Plot
        plotter.plot()
    """

    def __init__(
        self,
        primary: BasePlotter,
        secondary: BasePlotter,
        config: Optional[PlotConfig] = None,
    ):
        """
        Initialize dual-axis plotter with two sub-plotters.

        Args:
            primary: Plotter for the left Y-axis
            secondary: Plotter for the right Y-axis
            config: Optional override config (uses primary's config if None)
        """
        # Use primary's config as the main config
        super().__init__(config or primary.config)
        self.primary = primary
        self.secondary = secondary
        self.ax2: Optional[plt.Axes] = None
        self._primary_x_centers: List[float] = []

    def setup_figure(self) -> Tuple[plt.Figure, plt.Axes]:
        """Create figure with dual axes and share with sub-plotters."""
        self.fig, self.ax = plt.subplots(figsize=self.config.size)
        self.ax2 = self.ax.twinx()

        # Share figure and axes with sub-plotters
        self.primary.fig = self.fig
        self.primary.ax = self.ax

        self.secondary.fig = self.fig
        self.secondary.ax = self.ax2

        return self.fig, self.ax

    def _compute_bar_centers(self) -> List[float]:
        """
        Compute the center x positions of bar groups from primary plotter.

        This is used to align secondary plotter (e.g., lines) with bar centers.
        """
        centers = []

        # Check if primary is a BarPlotter with _all_xticks
        if hasattr(self.primary, "_all_xticks") and self.primary._all_xticks:
            # Get bar configuration
            n_bars = 1
            if self.primary.data is not None and self.primary.data.shape[1] > 1:
                n_bars = self.primary.data.shape[1] - 1

            bar_width = self.primary.config.bar_width
            single_width = bar_width / n_bars

            for xticks in self.primary._all_xticks:
                # Center of the group: first bar position + offset to center
                # First bar is at xticks[0], last bar is at xticks[0] + (n_bars-1)*single_width
                # Center is at xticks[0] + (n_bars-1)*single_width/2
                center = xticks[0] + (n_bars - 1) * single_width / 2
                centers.append(center)

        return centers

    def draw(self) -> None:
        """Draw both sub-plotters on their respective axes."""
        # Draw primary plotter on left axis
        self.primary.draw()

        # Compute bar centers after primary draw
        self._primary_x_centers = self._compute_bar_centers()

        # Draw secondary plotter on right axis, with x-coordinate alignment
        self._draw_secondary_aligned()

    def _draw_secondary_aligned(self) -> None:
        """
        Draw secondary plotter with x-coordinates aligned to primary bar centers.
        """
        # If we have bar centers and secondary has data, override x coordinates
        if self._primary_x_centers and self.secondary.data is not None:
            import numpy as np

            # Get y data from secondary (skip first column which is usually x or labels)
            y_data = self.secondary.data.iloc[:, 1:].values
            n_lines = y_data.shape[1]

            # Use bar centers as x coordinates
            x = np.array(self._primary_x_centers[: len(y_data)])

            from ..colors import resolve_colors

            colors = resolve_colors(self.secondary.config.colors, n_lines)
            markers = ["o", "s", "^", "D", "v", "<", ">", "p", "h"]

            handles = []
            for i in range(n_lines):
                (line,) = self.secondary.ax.plot(
                    x,
                    y_data[:, i],
                    marker=markers[i % len(markers)],
                    color=colors[i],
                    linewidth=2,
                    markersize=8,
                )
                handles.append(line)

            self.secondary._handles = handles
        else:
            # Fallback to default draw
            self.secondary.draw()

    def setup_axes(self) -> None:
        """Configure both axes using their respective configs."""
        # Setup primary axis
        self.primary.setup_axes()

        # Setup secondary axis
        if self.ax2 is not None:
            secondary_config = self.secondary.config

            if secondary_config.ylabel:
                self.ax2.set_ylabel(
                    secondary_config.ylabel,
                    fontsize=secondary_config.font.label,
                )

            if secondary_config.ylim is not None:
                self.ax2.set_ylim(secondary_config.ylim_min, secondary_config.ylim)

            self.ax2.tick_params(axis="y", labelsize=secondary_config.font.tick)

    def add_legend(self) -> None:
        """Add combined legend from both plotters."""
        # Collect handles from both plotters
        handles1 = []
        handles2 = []

        # Get handles from primary plotter (e.g., BarPlotter)
        if hasattr(self.primary, "_handles") and self.primary._handles:
            handles1 = self.primary._handles

        # Get handles from secondary plotter (e.g., LinePlotter)
        if hasattr(self.secondary, "_handles") and self.secondary._handles:
            handles2 = self.secondary._handles

        all_handles = handles1 + handles2

        # Combine legends from both configs
        labels1 = self.primary.config.legend or []
        labels2 = self.secondary.config.legend or []
        all_labels = list(labels1) + list(labels2)

        # Draw legend if we have handles and labels
        if all_handles and all_labels:
            self.fig.legend(
                all_handles,
                all_labels,
                loc=self.config.legend_loc,
                ncol=self.config.legend_ncol,
                bbox_to_anchor=self.config.legend_anchor,
                frameon=False,
                fontsize=self.config.font.legend,
            )
        elif self.config.legend:
            # Fallback to primary config legend only
            self.fig.legend(
                self.config.legend,
                loc=self.config.legend_loc,
                ncol=self.config.legend_ncol,
                bbox_to_anchor=self.config.legend_anchor,
                frameon=False,
                fontsize=self.config.font.legend,
            )

    def customize(self) -> None:
        """Run customize hooks for both sub-plotters."""
        self.primary.customize()
        self.secondary.customize()
