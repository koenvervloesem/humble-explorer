"""HumBLE Explorer

This is a cross-platform (Windows, Linux, macOS) human-friendly program to scan for
Bluetooth Low Energy (BLE) advertisements on the command line.
"""
from sys import version_info

if version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:  # pragma: no cover
    from importlib_metadata import PackageNotFoundError, version  # type: ignore

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError
