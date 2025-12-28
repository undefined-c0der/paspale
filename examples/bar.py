"""
Example: Basic Bar Chart

This example shows how to create a simple grouped bar chart.
"""

from paspale import BarPlotter, PlotConfig, paspale

# === Method 1: Quick plot ===
# The simplest way to create a bar chart

paspale(
    data="example_data/basic.csv",
    output="figures/basic.pdf",
    ylabel="Speedup",
    legend=["Baseline", "Method A", "Method B"],
    ylim=3.0,
)


# === Method 2: Using PlotConfig ===
# More control over configuration

# config = PlotConfig(
#     output="figures/comparison.pdf",
#     ylabel="Speedup",
#     ylim=6.0,
#     legend=["Baseline", "Method A", "Method B"],
#     colors="primary",
#     label_rotation=-30,  # Rotate x-axis labels
# )

# plotter = BarPlotter(config)
# plotter.load_csv("example_data/example.csv")
# plotter.plot()


# === Method 3: Custom Plotter Class ===
# For reusable configurations


# class PerformancePlotter(BarPlotter):
#     """Reusable performance comparison plotter."""

#     def configure(self) -> PlotConfig:
#         return PlotConfig(
#             output="figures/performance.pdf",
#             ylabel="Normalized Performance",
#             ylim=2.0,
#             legend=["Config A", "Config B", "Config C"],
#             colors="extended",
#         )

#     def customize(self):
#         """Add a baseline reference line."""
#         self.ax.axhline(y=1.0, color="red", linestyle="--", linewidth=1)
#         self.ax.text(
#             0.02,
#             1.05,
#             "Baseline",
#             transform=self.ax.get_yaxis_transform(),
#             fontsize=12,
#             color="red",
#         )


# Usage:
# plotter = PerformancePlotter()
# plotter.load_csv("example_data/performance.csv")
# plotter.plot()
