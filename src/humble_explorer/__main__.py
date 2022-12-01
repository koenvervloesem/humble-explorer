"""
Main entry point for HumBLE Explorer.
"""

import sys
from argparse import ArgumentParser, Namespace
from typing import List

from humble_explorer import __version__
from humble_explorer.app import BLEScannerApp

__author__ = "Koen Vervloesem"
__copyright__ = "Koen Vervloesem"
__license__ = "MIT"


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args: List[str]) -> Namespace:
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = ArgumentParser(description="Human-friendly Bluetooth Low Energy Explorer")
    parser.add_argument(
        "--version",
        action="version",
        version="humble-explorer {ver}".format(ver=__version__),
    )
    parser.add_argument(
        "-a", "--adapter", help="Bluetooth adapter (e.g. hci1 on Linux)", type=str
    )
    parser.add_argument(
        "-s",
        "--scanning-mode",
        dest="scanning_mode",
        help="Scanning mode (default: active)",
        type=str,
        default="active",
        choices=("active", "passive"),
    )
    return parser.parse_args(args)


def main(args: List[str]) -> None:
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    cli_args = parse_args(args)
    app = BLEScannerApp(cli_args=cli_args)
    app.run()


def run() -> None:
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html
    run()
