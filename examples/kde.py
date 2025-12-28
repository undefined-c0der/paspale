"""
Example: KDE Distribution Plot

KDE (Kernel Density Estimation) plots are useful for visualizing
distributions.

Follows unified interface: load_csv() / load_data() -> plot()
"""

import numpy as np
import pandas as pd

from paspale import KDEConfig, KDEPlotter

# === Method 1: From CSV file ===
# Each column in CSV becomes a distribution
# Column headers become legend labels

# Example CSV format:
#   Matrix_A,Matrix_B,Matrix_C
#   10,15,20
#   12,18,25
#   ...

# config = KDEConfig(
#     output="figures/distribution.pdf",
#     xlabel="Value",
#     ylabel="Density",
# )
# plotter = KDEPlotter(config)
# plotter.load_csv("example_data/distributions.csv")
# plotter.plot()


# === Method 2: From DataFrame ===

np.random.seed(42)
df = pd.DataFrame(
    {
        "Exponential": np.random.exponential(scale=50, size=1000),
        "Normal": np.abs(np.random.normal(loc=100, scale=30, size=1000)),
        "Uniform": np.random.uniform(low=20, high=150, size=1000),
    }
)

config = KDEConfig(
    output="figures/distribution.pdf",
    xlabel="Value",
    ylabel="Density",
    xlim=(0, 300),
)

plotter = KDEPlotter(config)
plotter.load_data(df)
plotter.plot()


# === Method 3: From list of arrays ===

data1 = np.random.exponential(scale=50, size=1000)
data2 = np.abs(np.random.normal(loc=100, scale=30, size=1000))

config = KDEConfig(
    output="figures/arrays.pdf",
    xlabel="Value",
    ylabel="Density",
)

plotter = KDEPlotter(config)
plotter.load_data([data1, data2], labels=["Exponential", "Normal"])
plotter.plot()


# === Method 4: Add individual distributions ===

plotter = KDEPlotter(KDEConfig(output="figures/manual.pdf"))
plotter.add(data1, "Series A")
plotter.add(data2, "Series B")
plotter.plot()
