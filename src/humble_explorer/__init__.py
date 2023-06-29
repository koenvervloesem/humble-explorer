"""HumBLE Explorer: Human-Friendly Bluetooth Low Energy Explorer.

This is a cross-platform (Windows, Linux, macOS) human-friendly program to scan for
Bluetooth Low Energy (BLE) advertisements on the command line.
"""
from importlib.metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError
