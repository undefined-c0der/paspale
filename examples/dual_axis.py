"""
Example: Dual-Axis Plot

Dual-axis plots show two related metrics with different scales,
such as bandwidth (bars) and miss rate (line).
"""

from paspale import BarPlotter, DualAxisPlotter, FigureSize, LinePlotter, PlotConfig


def main():
    """Create a dual-axis plot with bars and lines."""
    # Config for the primary axis (left Y-axis)
    primary_config = PlotConfig(
        output="figures/bandwidth_missrate.pdf",
        size=FigureSize.DOUBLE_WIDE,
        ylabel="Bandwidth (GB/s)",
        ylim=100,
        legend=["Baseline", "Cache", "Prefetch", "Ours"],
        legend_ncol=5,
        legend_anchor=(0.5, -0.1),
        colors="primary",
    )

    # Config for the secondary axis (right Y-axis)
    secondary_config = PlotConfig(
        ylabel="Miss Rate",
        ylim=1.0,
        colors="lines",
        legend=["Miss Rate"],  # Line legend on second row
    )

    # Create sub-plotters
    bar_plotter = BarPlotter(primary_config)
    bar_plotter.load_csv("example_data/bandwidth.csv")

    line_plotter = LinePlotter(secondary_config)
    line_plotter.load_csv("example_data/missrate.csv")

    # Combine into dual-axis plotter
    plotter = DualAxisPlotter(
        primary=bar_plotter,
        secondary=line_plotter,
    )

    plotter.plot()


# For subclassing pattern (alternative approach)
class BandwidthMissratePlotter(DualAxisPlotter):
    """
    Bandwidth bar chart with miss rate overlay.

    This shows how to create a reusable dual-axis plotter by subclassing.
    """

    def __init__(self):
        primary_config = PlotConfig(
            output="figures/bandwidth_missrate.pdf",
            size=FigureSize.DOUBLE_WIDE,
            ylabel="Bandwidth (GB/s)",
            ylim=100,
            legend=["Baseline", "Cache", "Prefetch", "Ours"],
            colors="primary",
        )

        secondary_config = PlotConfig(
            ylabel="Miss Rate",
            ylim=1.0,
            colors="lines",
        )

        super().__init__(
            primary=BarPlotter(primary_config),
            secondary=LinePlotter(secondary_config),
        )

    def load_data_files(
        self, primary_path: str, secondary_path: str
    ) -> "BandwidthMissratePlotter":
        """Load data for both axes."""
        self.primary.load_csv(primary_path)
        self.secondary.load_csv(secondary_path)
        return self


# Usage
if __name__ == "__main__":
    # Method 1: Direct composition (recommended for one-off plots)
    main()

    # Method 2: Subclassing (recommended for reusable patterns)
    # plotter = BandwidthMissratePlotter()
    # plotter.load_data_files(
    #     "example_data/bandwidth.csv",
    #     "example_data/missrate.csv",
    # )
    # plotter.plot()
