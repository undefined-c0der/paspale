"""
Base plotter class and common plotting utilities.
"""

import os
from abc import ABC, abstractmethod
from typing import Any, List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import rc

from .colors import resolve_colors
from .config import FontConfig, PlotConfig


def setup_font(family: str = "Times New Roman"):
    """Set up matplotlib font configuration."""
    rc("font", family=family)
    plt.rcParams["font.serif"] = [family]


class BasePlotter(ABC):
    """
    Abstract base class for all plotters.

    Subclasses must implement:
        - draw(): The main drawing logic

    Workflow:
        1. Create plotter with config
        2. Load data via load_csv() or load_data()
        3. Call plot() to generate figure

    Example:
        class MyPlotter(BasePlotter):
            def draw(self):
                self.ax.bar(self.x, self.y)

        plotter = MyPlotter(config)
        plotter.load_csv("data.csv")
        plotter.plot()
    """

    def __init__(self, config: Optional[PlotConfig] = None):
        """
        Initialize plotter.

        Args:
            config: Plot configuration. If None, uses configure() method.
        """
        self.config = config or self.configure()
        setup_font(self.config.font.family)

        self.fig: Optional[plt.Figure] = None
        self.ax: Optional[plt.Axes] = None
        self.data: Optional[pd.DataFrame] = None
        self._data_matrix: List = []

    def configure(self) -> PlotConfig:
        """
        Override this method to provide default configuration.

        Returns:
            PlotConfig instance
        """
        return PlotConfig()

    def load_csv(self, path: str, **kwargs) -> "BasePlotter":
        """
        Load data from CSV file.

        Args:
            path: Path to CSV file
            **kwargs: Additional arguments for pd.read_csv

        Returns:
            self for chaining
        """
        self.data = pd.read_csv(path, **kwargs)
        self._process_data()
        return self

    def load_data(self, data: pd.DataFrame) -> "BasePlotter":
        """
        Load data from DataFrame.

        Args:
            data: pandas DataFrame

        Returns:
            self for chaining
        """
        self.data = data
        self._process_data()
        return self

    def _process_data(self) -> None:
        """Process loaded data into internal format."""
        if self.data is not None:
            self._data_matrix = [
                [[v] for v in row] for row in self.data.values.tolist()
            ]

    def setup_figure(self) -> Tuple[plt.Figure, plt.Axes]:
        """Create figure and axes."""
        self.fig, self.ax = plt.subplots(figsize=self.config.size)
        return self.fig, self.ax

    def setup_axes(self) -> None:
        """Configure axes based on config."""
        if self.config.xlabel:
            self.ax.set_xlabel(self.config.xlabel, fontsize=self.config.font.label)

        if self.config.ylabel:
            self.ax.set_ylabel(self.config.ylabel, fontsize=self.config.font.label)

        # Y-axis limits
        if self.config.ylim is not None:
            self.ax.set_ylim(self.config.ylim_min, self.config.ylim)

        # X-axis limits
        if self.config.xlim is not None:
            self.ax.set_xlim(self.config.xlim)

        # Log scale
        if self.config.log_scale:
            self.ax.set_yscale("log")

        # Y ticks
        if self.config.yticks and self.config.ylim:
            if self.config.log_scale:
                ticks = np.logspace(
                    np.log10(max(self.config.ylim_min, 1e-10)),
                    np.log10(self.config.ylim),
                    num=self.config.yticks,
                )
            else:
                ticks = np.linspace(
                    self.config.ylim_min,
                    self.config.ylim,
                    num=self.config.yticks,
                )

            # Format labels
            if "{:.0%}" in self.config.ytick_format:
                labels = [f"{int(t * 100)}%" for t in ticks]
            else:
                labels = [self.config.ytick_format.format(t) for t in ticks]

            self.ax.set_yticks(ticks)
            self.ax.set_yticklabels(labels, fontsize=self.config.font.tick)

        self.ax.tick_params(axis="both", labelsize=self.config.font.tick)
        self.ax.yaxis.grid(True)

    def add_legend(self) -> None:
        """Add legend to figure."""
        if self.config.legend:
            self.fig.legend(
                self.config.legend,
                loc=self.config.legend_loc,
                ncol=self.config.legend_ncol,
                bbox_to_anchor=self.config.legend_anchor,
                frameon=False,
                fontsize=self.config.font.legend,
            )

    @abstractmethod
    def draw(self) -> None:
        """
        Main drawing logic. Must be implemented by subclasses.

        This method should use self.ax to draw the plot.
        """
        pass

    def customize(self) -> None:
        """
        Hook for adding custom elements after drawing.

        Override this method to add annotations, highlights, etc.
        """
        pass

    def save(self, path: Optional[str] = None) -> None:
        """
        Save figure to file.

        Args:
            path: Output path. If None, uses config.output
        """
        output = path or self.config.output
        if not output:
            raise ValueError("No output path specified")

        # Create directory if needed
        os.makedirs(os.path.dirname(output) or ".", exist_ok=True)

        self.fig.savefig(output, bbox_inches="tight")
        print(f"Saved: {output}")

    def plot(self, save: bool = True) -> Tuple[plt.Figure, plt.Axes]:
        """
        Execute the complete plotting workflow.

        Args:
            save: Whether to save the figure

        Returns:
            Tuple of (figure, axes)
        """
        self.setup_figure()
        self.draw()
        self.setup_axes()

        plt.tight_layout(rect=self.config.tight_rect)

        self.customize()
        self.add_legend()

        if save and self.config.output:
            self.save()

        return self.fig, self.ax

    def show(self) -> None:
        """Display the figure interactively."""
        if self.fig is None:
            self.plot(save=False)
        plt.show()
