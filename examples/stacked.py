"""
Example: Stacked Bar Chart

Stacked bar charts show composition, such as energy breakdown.
"""

import matplotlib.pyplot as plt

from paspale import PlotConfig, StackedBarPlotter


class EnergyBreakdownPlotter(StackedBarPlotter):
    """
    Energy breakdown visualization.
    """

    def configure(self) -> PlotConfig:
        return PlotConfig(
            output="figures/energy_breakdown.pdf",
            size=(14, 4.5),
            ylabel="Energy",
            ylim=1.0,
            legend=["Compute", "Memory", "Communication"],
            colors="breakdown",  # 3-color scheme for breakdowns
            label_rotation=-15,
        )

    def customize(self):
        """Add efficiency annotations."""
        # Example: Add text annotations
        self.ax.text(
            0.98,
            0.98,
            "Lower is better",
            transform=self.ax.transAxes,
            ha="right",
            va="top",
            fontsize=21,
            style="italic",
        )


# Usage
if __name__ == "__main__":
    plotter = EnergyBreakdownPlotter()
    plotter.load_csv("example_data/energy.csv")
    plotter.plot()
