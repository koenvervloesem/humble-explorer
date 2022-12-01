.. image:: https://github.com/koenvervloesem/humble-explorer/workflows/Tests/badge.svg
    :alt: Continuous Integration
    :target: https://github.com/koenvervloesem/humble-explorer/actions
.. image:: https://img.shields.io/pypi/v/humble-explorer.svg
    :alt: Python package version
    :target: https://pypi.org/project/humble-explorer/
.. image:: https://img.shields.io/pypi/pyversions/humble-explorer.svg
    :alt: Supported Python versions
    :target: https://python.org/
.. image:: https://img.shields.io/github/license/koenvervloesem/humble-explorer.svg
    :alt: License
    :target: https://github.com/koenvervloesem/ble-explorer/blob/main/LICENSE.txt

|

===============
HumBLE Explorer
===============


    Human-friendly Bluetooth Low Energy Explorer


This is a cross-platform (Windows, Linux, macOS) human-friendly program to scan for Bluetooth Low Energy (BLE) advertisements on the command line. It's mostly useful for people who develop BLE software or want to debug problems with BLE devices.

.. image:: https://raw.githubusercontent.com/koenvervloesem/humble-explorer/main/docs/_static/screenshot.png
    :alt: Human-friendly Bluetooth Low Energy Explorer in action

Installation
============

You can install HumBLE Explorer as a pip package from PyPI::

    pip install humble-explorer

Usage
=====

HumBLE Explorer understands some command-line arguments, which you can see with the ``--help`` option::

    humble-explorer --help

.. _pyscaffold-notes:

Making Changes & Contributing
=============================

This project uses `pre-commit`_, please make sure to install it before making any
changes::

    pip install pre-commit
    cd humble-explorer
    pre-commit install

It is a good idea to update the hooks to the latest version::

    pre-commit autoupdate

Don't forget to tell your contributors to also install and use pre-commit.

.. _pre-commit: https://pre-commit.com/

Debugging code
==============

You can debug HumBLE Explorer with Textual's debug console.

To use the console, open up **two** terminal emulators. Run the following in one of the terminals::

    textual console

You should see the Textual devtools welcome message.

In the other console, run HumBLE Explorer with::

    TEXTUAL=devtools python3 src/humble_explorer/__main__.py

Learn more about Bluetooth Low Energy development
=================================================

If you want to learn more about Bluetooth Low Energy development, read my book `Develop your own Bluetooth Low Energy Applications for Raspberry Pi, ESP32 and nRF52 with Python, Arduino and Zephyr <https://koen.vervloesem.eu/books/develop-your-own-bluetooth-low-energy-applications/>`_ and the accompanying GitHub repository `koenvervloesem/bluetooth-low-energy-applications <https://github.com/koenvervloesem/bluetooth-low-energy-applications>`_.

Note
====

This project has been set up using PyScaffold 4.3.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.

License
=======

This project is provided by Koen Vervloesem as open source software with the MIT license. See the LICENSE file for more information.
