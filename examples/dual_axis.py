"""
Example: Dual-Axis Plot

Dual-axis plots show two related metrics with different scales,
such as bandwidth (bars) and miss rate (line).
"""

from paspale import DualAxisPlotter, FigureSize, PlotConfig


class BandwidthMissratePlotter(DualAxisPlotter):
    """
    Bandwidth bar chart with miss rate overlay.
    """

    def configure(self) -> PlotConfig:
        return PlotConfig(
            output="figures/bandwidth_missrate.pdf",
            size=FigureSize.DOUBLE_WIDE,
            ylabel="Bandwidth (GB/s)",
            ylim=100,
            legend=["Baseline", "Cache", "Prefetch", "Ours"],
            colors="primary",
        )


# Usage
if __name__ == "__main__":
    plotter = BandwidthMissratePlotter()
    plotter.load_csv("example_data/bandwidth.csv")
    plotter.load_secondary(
        "example_data/missrate.csv",
        ylabel="Miss Rate",
        ylim=1.0,
    )
    plotter.plot()
