"""
KDE (Kernel Density Estimation) plotter implementation.
"""

from typing import List, Optional, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.ticker import PercentFormatter

from ..base import BasePlotter
from ..colors import resolve_colors
from ..config import KDEConfig


class KDEPlotter(BasePlotter):
    """
    Kernel Density Estimation plotter.

    Creates KDE plots for visualizing distributions.

    Follows the unified interface:
        - load_csv(): Load from CSV file
        - load_data(): Load from DataFrame or arrays
        - plot(): Generate the plot

    Example:
        # From CSV (each column is a distribution)
        plotter = KDEPlotter(KDEConfig(output="dist.pdf"))
        plotter.load_csv("distributions.csv")
        plotter.plot()

        # From arrays
        plotter = KDEPlotter(KDEConfig(output="dist.pdf"))
        plotter.load_data([array1, array2], labels=["A", "B"])
        plotter.plot()

        # From DataFrame
        plotter = KDEPlotter(KDEConfig(output="dist.pdf"))
        plotter.load_data(df)  # Each column becomes a distribution
        plotter.plot()
    """

    def __init__(self, config: Optional[KDEConfig] = None):
        """
        Initialize KDE plotter.

        Args:
            config: KDE configuration
        """
        super().__init__(config or KDEConfig())
        self._distributions: List[tuple] = []  # (data, label)
        self._handles: List = []

    def load_csv(self, path: str, **kwargs) -> "KDEPlotter":
        """
        Load distributions from CSV file.

        CSV format:
            - Each column represents a distribution
            - Column headers become legend labels
            - NaN values are automatically filtered

        Args:
            path: Path to CSV file
            **kwargs: Additional arguments for pd.read_csv

        Returns:
            self for chaining

        Example CSV:
            Matrix_A,Matrix_B,Matrix_C
            10,15,20
            12,18,25
            ...
        """
        df = pd.read_csv(path, **kwargs)
        return self._load_from_dataframe(df)

    def load_data(
        self,
        data: Union[pd.DataFrame, List[np.ndarray], np.ndarray],
        labels: Optional[List[str]] = None,
    ) -> "KDEPlotter":
        """
        Load distributions from DataFrame or arrays.

        Args:
            data: One of:
                - DataFrame: each column is a distribution
                - List of arrays: each array is a distribution
                - 2D array: each column is a distribution
            labels: Optional labels for each distribution

        Returns:
            self for chaining
        """
        if isinstance(data, pd.DataFrame):
            return self._load_from_dataframe(data)
        elif isinstance(data, np.ndarray):
            if data.ndim == 1:
                # Single distribution
                label = labels[0] if labels else ""
                self._distributions.append((data[~np.isnan(data)], label))
            else:
                # 2D array, each column is a distribution
                for i in range(data.shape[1]):
                    label = labels[i] if labels and i < len(labels) else f"Series {i+1}"
                    col_data = data[:, i]
                    col_data = col_data[~np.isnan(col_data)]
                    self._distributions.append((col_data, label))
        elif isinstance(data, list):
            for i, arr in enumerate(data):
                label = labels[i] if labels and i < len(labels) else f"Series {i+1}"
                arr = np.asarray(arr)
                arr = arr[~np.isnan(arr)]
                self._distributions.append((arr, label))
        return self

    def _load_from_dataframe(self, df: pd.DataFrame) -> "KDEPlotter":
        """Load distributions from DataFrame columns."""
        for col in df.columns:
            data = df[col].dropna().values
            self._distributions.append((data, str(col)))
        return self

    def add(
        self,
        data: np.ndarray,
        label: str = "",
    ) -> "KDEPlotter":
        """
        Add a single distribution.

        Args:
            data: 1D array of values
            label: Label for legend

        Returns:
            self for chaining
        """
        data = np.asarray(data)
        data = data[~np.isnan(data)]
        self._distributions.append((data, label))
        return self

    def setup_figure(self) -> None:
        """Create figure and axes with seaborn styling."""
        super().setup_figure()
        # Set seaborn theme with font configuration
        sns.set_theme(
            style="ticks",
            font=self.config.font.family,
            rc={
                "font.family": self.config.font.family,
                "font.serif": [self.config.font.family],
            },
        )

    def draw(self) -> None:
        """Draw all KDE curves."""
        n = len(self._distributions)
        colors = resolve_colors(self.config.colors, n)

        for (data, label), color in zip(self._distributions, colors):
            line = sns.kdeplot(
                data,
                color=color,
                fill=self.config.fill,
                alpha=self.config.alpha,
                ax=self.ax,
                label=label,
            )
            if line:
                self._handles.append(line)

    def setup_axes(self) -> None:
        """Configure axes."""
        self.ax.set_xlabel(
            self.config.xlabel,
            fontsize=self.config.font.label,
        )
        self.ax.set_ylabel(
            self.config.ylabel,
            fontsize=self.config.font.label,
        )

        if self.config.use_percentage:
            self.ax.yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=0))

        if self.config.xlim:
            self.ax.set_xlim(self.config.xlim)

        self.ax.tick_params(axis="both", labelsize=self.config.font.tick)

        # Style spines
        sns.despine(top=True, right=True)
        self.ax.spines["left"].set_linewidth(1.5)
        self.ax.spines["bottom"].set_linewidth(1.5)

    def add_legend(self) -> None:
        """Add legend if there are labels."""
        labels = [label for _, label in self._distributions if label]
        if labels:
            # For KDE, use ax.legend for better positioning (no bbox_to_anchor)
            # This respects the legend_loc parameter properly
            self.ax.legend(
                loc=self.config.legend_loc,
                fontsize=self.config.font.legend,
            )

    def customize(self) -> None:
        """Hook for custom modifications. Override in subclass."""
        pass
