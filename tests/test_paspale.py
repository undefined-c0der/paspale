"""
Basic tests for paspale.
"""

import os
import tempfile

import numpy as np
import pandas as pd
import pytest

from paspale import BarPlotter, KDEConfig, KDEPlotter, PlotConfig
from paspale.colors import ColorScheme, get_colors, resolve_colors


class TestColors:
    """Test color utilities."""

    def test_get_colors_primary(self):
        colors = get_colors(3, "primary")
        assert len(colors) == 3
        assert all(c.startswith("#") for c in colors)

    def test_get_colors_extended(self):
        colors = get_colors(10, "extended")
        assert len(colors) == 10

    def test_get_colors_cycles(self):
        """Colors should cycle when n > palette size."""
        colors = get_colors(12, "primary")
        assert len(colors) == 12
        assert colors[0] == colors[6]  # Should cycle

    def test_resolve_colors_scheme(self):
        colors = resolve_colors("primary", 3)
        assert len(colors) == 3

    def test_resolve_colors_list(self):
        custom = ["#ff0000", "#00ff00"]
        colors = resolve_colors(custom, 4)
        assert len(colors) == 4
        assert colors[0] == "#ff0000"
        assert colors[2] == "#ff0000"  # Cycled


class TestPlotConfig:
    """Test configuration classes."""

    def test_default_config(self):
        config = PlotConfig()
        assert config.output == ""
        assert config.size == (14, 4.5)
        assert config.ylim_min == 0.0

    def test_custom_config(self):
        config = PlotConfig(
            output="test.pdf",
            ylabel="Speedup",
            ylim=10.0,
        )
        assert config.output == "test.pdf"
        assert config.ylabel == "Speedup"
        assert config.ylim == 10.0

    def test_legend_ncol_auto(self):
        config = PlotConfig(legend=["A", "B", "C"])
        assert config.legend_ncol == 3


class TestBarPlotter:
    """Test bar plotter."""

    def test_load_csv(self):
        # Create temp CSV
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("label,a,b,c\n")
            f.write("W1,1.0,2.0,3.0\n")
            f.write("W2,1.5,2.5,3.5\n")
            temp_path = f.name

        try:
            config = PlotConfig(output="test.pdf")
            plotter = BarPlotter(config)
            plotter.load_csv(temp_path)

            assert plotter.data is not None
            assert len(plotter.data) == 2
        finally:
            os.unlink(temp_path)

    def test_load_dataframe(self):
        df = pd.DataFrame(
            {
                "label": ["W1", "W2"],
                "a": [1.0, 1.5],
                "b": [2.0, 2.5],
            }
        )

        config = PlotConfig(output="test.pdf")
        plotter = BarPlotter(config)
        plotter.load_data(df)

        assert plotter.data is not None
        assert len(plotter._data_matrix) == 2


class TestKDEPlotter:
    """Test KDE plotter."""

    def test_add_distribution(self):
        config = KDEConfig(output="test.pdf")
        plotter = KDEPlotter(config)

        data = np.random.normal(0, 1, 100)
        plotter.add(data, "Test")

        assert len(plotter._distributions) == 1
        assert plotter._distributions[0][1] == "Test"

    def test_multiple_distributions(self):
        config = KDEConfig(output="test.pdf")
        plotter = KDEPlotter(config)

        plotter.add(np.random.normal(0, 1, 100), "A")
        plotter.add(np.random.normal(5, 1, 100), "B")

        assert len(plotter._distributions) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
