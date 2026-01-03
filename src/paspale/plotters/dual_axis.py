"""
Dual-axis plotter implementation.
"""

from typing import Optional, Tuple, Type

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

    def draw(self) -> None:
        """Draw both sub-plotters on their respective axes."""
        # Draw primary plotter on left axis
        self.primary.draw()

        # Draw secondary plotter on right axis
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
        # Collect handles and labels from both axes
        handles1, labels1 = self.ax.get_legend_handles_labels()
        handles2, labels2 = (
            self.ax2.get_legend_handles_labels() if self.ax2 else ([], [])
        )

        all_handles = handles1 + handles2
        all_labels = labels1 + labels2

        # Use explicit legend from config if provided
        if self.config.legend:
            self.fig.legend(
                self.config.legend,
                loc=self.config.legend_loc,
                ncol=self.config.legend_ncol,
                bbox_to_anchor=self.config.legend_anchor,
                frameon=False,
                fontsize=self.config.font.legend,
            )
        elif all_handles:
            self.fig.legend(
                all_handles,
                all_labels,
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
