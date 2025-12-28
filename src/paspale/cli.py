"""
Command-line interface for paspale.
"""

import argparse
import sys


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="PasPale - Academic paper plotting tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
        Examples:
            # Plot a CSV file
            paspale data.csv -o figure.pdf -y "Speedup" -l "A" "B" "C"
            
            # With custom settings
            paspale data.csv -o fig.pdf -y "Performance" --ylim 10 --colors extended
            
        For more control, use the Python API:
            from paspale import paspale, BarPlotter, PlotConfig
        """,
    )

    parser.add_argument(
        "data",
        nargs="?",
        help="Input CSV file",
    )

    parser.add_argument(
        "-o",
        "--output",
        default="output.pdf",
        help="Output file path (default: output.pdf)",
    )

    parser.add_argument(
        "-y",
        "--ylabel",
        default="",
        help="Y-axis label",
    )

    parser.add_argument(
        "-l",
        "--legend",
        nargs="+",
        help="Legend labels",
    )

    parser.add_argument(
        "--ylim",
        type=float,
        help="Y-axis upper limit",
    )

    parser.add_argument(
        "--colors",
        default="primary",
        help="Color scheme (primary, extended, gradient, lines)",
    )

    parser.add_argument(
        "--size",
        nargs=2,
        type=float,
        default=[14, 4.5],
        metavar=("W", "H"),
        help="Figure size in inches (default: 14 4.5)",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="paspale 0.1.0",
    )

    args = parser.parse_args()

    if args.data is None:
        parser.print_help()
        return 0

    # Import here to avoid slow startup
    from .paspale import paspale

    try:
        paspale(
            data=args.data,
            output=args.output,
            ylabel=args.ylabel,
            legend=args.legend,
            ylim=args.ylim,
            colors=args.colors,
            size=tuple(args.size),
        )
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
