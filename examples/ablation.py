"""
Example: Ablation Study

Ablation studies typically show incremental improvements.
This example uses gradient colors to visualize the progression.
"""

from paspale import BarPlotter, FigureSize, PlotConfig


class AblationPlotter(BarPlotter):
    """
    Ablation study plotter with gradient colors.

    Colors progress from light to dark, showing incremental additions.
    """

    def configure(self) -> PlotConfig:
        return PlotConfig(
            output="figures/ablation.pdf",
            size=FigureSize.DOUBLE_WIDE,  # (28, 4.5) - double width for many bars
            ylabel="Speedup",
            ylim=3.0,
            legend=[
                "Base",
                "+Optimization A",
                "+Optimization B",
                "+Optimization C",
                "+Optimization D",
                "Full (Ours)",
            ],
            colors="gradient",  # Uses gradient color scheme
            legend_anchor=(0.5, -0.1),  # Move legend down
        )


# Usage
if __name__ == "__main__":
    plotter = AblationPlotter()
    plotter.load_csv("example_data/ablation.csv")
    plotter.plot()
