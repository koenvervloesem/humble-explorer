"""Main entry point for HumBLE Explorer."""
from __future__ import annotations

import sys
from argparse import ArgumentParser, Namespace

from humble_explorer import __version__
from humble_explorer.app import BLEScannerApp

__author__ = "Koen Vervloesem"
__copyright__ = "Koen Vervloesem"
__license__ = "MIT"


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def run() -> None:
    """Calls :func:`main` passing the CLI arguments extracted from `sys.argv`.

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


def main(args: list[str]) -> None:
    """Wrapper allowing the BLE scanner app to be called on the command line.

    This wrapper accepts string arguments.

    Args:
      args (list[str]): command line parameters as list of strings
          (for example  ``["--scanning-mode", "passive"]``).
    """
    cli_args = parse_args(args)
    app = BLEScannerApp(cli_args=cli_args)
    app.run()


def parse_args(args: list[str]) -> Namespace:
    """Parse command line parameters.

    Args:
      args (list[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      `argparse.Namespace`: command line parameters namespace
    """
    parser = ArgumentParser(description="Human-friendly Bluetooth Low Energy Explorer")
    parser.add_argument(
        "--version",
        action="version",
        version=f"humble-explorer {__version__}",
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


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html
    run()
