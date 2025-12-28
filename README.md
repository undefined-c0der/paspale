# PasPale

PasPale provides a consistent, configurable interface for creating publication-ready figures with minimal boilerplate code.

## Features

- 🎨 **Unified Style** - Consistent colors, fonts, and layouts across all plots
- ⚙️ **Configurable** - Dataclass-based configuration with sensible defaults
- 📊 **Multiple Plot Types** - Bar charts, stacked bars, dual-axis, KDE, and more
- 📄 **Publication Ready** - PDF output with proper fonts and sizing
- 🔧 **Extensible** - Easy to create custom plotters by inheritance

## Installation

```bash
git clone https://github.com/undefined-c0der/paspale.git
cd paspale
pip install -e .
```

## Quick Start

### 1. Simple Bar Chart

```python
from paspale import paspale

paspale(
    data="data/results.csv",
    output="figures/comparison.pdf",
    ylabel="Speedup",
    legend=["Method A", "Method B", "Method C"],
)
```

### 2. Using Configuration

```python
from paspale import BarPlotter, PlotConfig

config = PlotConfig(
    output="figures/performance.pdf",
    ylabel="Speedup",
    ylim=6.0,
    legend=["Baseline", "Optimized", "Ours"],
    colors="primary",
)

plotter = BarPlotter(config)
plotter.load_csv("data/results.csv")
plotter.plot()
```

### 3. KDE Distribution Plot

```python
from paspale import KDEPlotter, KDEConfig

config = KDEConfig(
    output="figures/distribution.pdf",
    xlabel="Value",
    ylabel="Density",
)

# From CSV (each column is a distribution)
plotter = KDEPlotter(config)
plotter.load_csv("data/distributions.csv")
plotter.plot()

# Or from arrays
import numpy as np
plotter = KDEPlotter(config)
plotter.load_data([arr1, arr2], labels=["A", "B"])
plotter.plot()
```

### 4. Custom Plotter

```python
from paspale import BarPlotter, PlotConfig

class MyPlotter(BarPlotter):
    def configure(self) -> PlotConfig:
        return PlotConfig(
            output="figures/my_plot.pdf",
            ylabel="Performance",
            ylim=10.0,
            legend=["A", "B", "C"],
        )
    
    def customize(self):
        self.ax.axhline(y=1.0, color='red', linestyle='--')

plotter = MyPlotter()
plotter.load_csv("data/my_data.csv")
plotter.plot()
```

## Unified Interface

All plotters follow the same pattern:

```python
plotter = SomePlotter(config)
plotter.load_csv("data.csv")   # or load_data(df)
plotter.plot()
```

| Plotter | Config | Description |
|---------|--------|-------------|
| `BarPlotter` | `PlotConfig` | Grouped bar charts |
| `StackedBarPlotter` | `PlotConfig` | Stacked bar charts |
| `DualAxisPlotter` | `PlotConfig` | Dual Y-axis plots |
| `LinePlotter` | `PlotConfig` | Line charts |
| `KDEPlotter` | `KDEConfig` | Kernel density estimation |

## Configuration

### PlotConfig Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `output` | str | Required | Output file path |
| `size` | tuple | (14, 4.5) | Figure size (width, height) |
| `ylabel` | str | "" | Y-axis label |
| `xlabel` | str | "" | X-axis label |
| `ylim` | float | None | Y-axis upper limit |
| `ylim_min` | float | 0.0 | Y-axis lower limit |
| `legend` | list | [] | Legend labels |
| `colors` | str/list | "primary" | Color scheme or list |
| `log_scale` | bool | False | Use log scale for Y-axis |

### KDEConfig Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `output` | str | "" | Output file path |
| `size` | tuple | (8, 5) | Figure size |
| `xlabel` | str | "" | X-axis label |
| `ylabel` | str | "Density" | Y-axis label |
| `xlim` | tuple | None | X-axis limits |
| `fill` | bool | True | Fill under curve |
| `alpha` | float | 0.3 | Fill transparency |
| `use_percentage` | bool | False | Show Y as percentage |

### Color Schemes

```python
from paspale import colors

colors.PRIMARY    # 6 pastel colors
colors.EXTENDED   # 11 colors
colors.GRADIENT   # Blue gradient for ablations
colors.BREAKDOWN  # Component colors
colors.LINES      # Line plot colors
```

## Examples

See [examples/](examples/) directory:

- `examples/bar.py` - Basic bar chart
- `examples/ablation.py` - Ablation study with gradient colors
- `examples/dual_axis.py` - Bandwidth with miss rate overlay
- `examples/kde.py` - Distribution visualization

## License
Paspale is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
