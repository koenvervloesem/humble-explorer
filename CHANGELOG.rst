=========
Changelog
=========

Version 0.4.1: Switch to switches (203-02-16)
=============================================

This is a bugfix release for a breaking change in Textual 0.11.0.

* Add GitHub profile to authors page by @koenvervloesem in https://github.com/koenvervloesem/humble-explorer/pull/40
* Update pyscaffold v4.4 by @koenvervloesem in https://github.com/koenvervloesem/humble-explorer/pull/45
* Use furo theme for documentation by @koenvervloesem in https://github.com/koenvervloesem/humble-explorer/pull/46
* Autoupdate pre-commit by @koenvervloesem in https://github.com/koenvervloesem/humble-explorer/pull/47
* Change Checkbox to Switch for Textual 0.11.0 by @koenvervloesem in https://github.com/koenvervloesem/humble-explorer/pull/48

Version 0.4.0: Minor user interface improvements (2022-12-28)
=============================================================

This release adds some minor user interface improvements. The description **Unknown** for unknown company IDs and UUIDs is now shown in red. If the Bluetooth address has a known OUI, the vendor name is shown. And the number of filtered and received advertisements is now shown in the title.

The documentation now also tells what to do if you want to contribute descriptions for unknown UUIDs. You can contribute these to the `bluetooth-numbers <https://github.com/koenvervloesem/bluetooth-numbers>`_ project.

New features
------------

* Color "Unknown" in red for company IDs and UUIDs by @koenvervloesem in https://github.com/koenvervloesem/humble-explorer/pull/35
* Put the number of shown (filtered) and received advertisements in title by @koenvervloesem in https://github.com/koenvervloesem/humble-explorer/pull/36
* Show vendor of Bluetooth address if it has a known OUI by @koenvervloesem in https://github.com/koenvervloesem/humble-explorer/pull/37

Miscellaneous
-------------

* Adds and updates pre-commit hooks by @koenvervloesem in https://github.com/koenvervloesem/humble-explorer/pull/34
* Add documentation about contributing data such as UUID descriptions by @koenvervloesem in https://github.com/koenvervloesem/humble-explorer/pull/38

Version 0.3.3: Python 3.7 works! (2022-12-25)
=============================================

This is a bugfix release. The most visible fix is for a bug that let HumBLE Explorer fail on Python 3.7.

Fixes
-----

* Minor code style fixes by @koenvervloesem in https://github.com/koenvervloesem/humble-explorer/pull/30
* Run tests with the correct Python version in CI by @koenvervloesem in https://github.com/koenvervloesem/humble-explorer/pull/31
* Fix byte separator in RichHexData by @koenvervloesem in https://github.com/koenvervloesem/humble-explorer/pull/32

Version 0.3.2: macOS works! (2022-12-23)
========================================

This is a bugfix release. The most important fix is that HumBLE Explorer now finally works on macOS too.

Fixes
-----

* Fix typing for optional argument in SettingsWidget constructor by @koenvervloesem in https://github.com/koenvervloesem/humble-explorer/pull/26
* Create BleakScanner object on mount by @koenvervloesem in https://github.com/koenvervloesem/humble-explorer/pull/27
* Disable duplicate detection of advertisement data on Linux by @koenvervloesem in https://github.com/koenvervloesem/humble-explorer/pull/28

Version 0.3.1 (2022-12-22)
==========================

This is a maintenance release with some fixes under the hood.

* Improve documentation by @koenvervloesem in https://github.com/koenvervloesem/humble-explorer/pull/19
* Add module and method docstrings by @koenvervloesem in https://github.com/koenvervloesem/humble-explorer/pull/20
* Typing fixes by @koenvervloesem in https://github.com/koenvervloesem/humble-explorer/pull/21
* More typing fixes by @koenvervloesem in https://github.com/koenvervloesem/humble-explorer/pull/22
* Use bluetooth-numbers package to translate UUIDs to names by @koenvervloesem in https://github.com/koenvervloesem/humble-explorer/pull/23
* Upgrade to bluetooth-numbers 1.0 API by @koenvervloesem in https://github.com/koenvervloesem/humble-explorer/pull/24

Version 0.3.0 (2022-12-14)
==========================

This version adds a lot of user interface improvements. You can filter advertisements on device addresses, you can choose which advertisement data types are shown, you can enable or disable autoscrolling and you can clear the list of received advertisements.

New features
------------

* Add address filter by @koenvervloesem in https://github.com/koenvervloesem/humble-explorer/pull/12
* Automatically hide and focus filter widget by @koenvervloesem in https://github.com/koenvervloesem/humble-explorer/pull/14
* Add sidebar to select data to show by @koenvervloesem in https://github.com/koenvervloesem/humble-explorer/pull/15
* UI improvements by @koenvervloesem in https://github.com/koenvervloesem/humble-explorer/pull/18

Miscellaneous
-------------

* Add unit tests for renderables by @koenvervloesem in https://github.com/koenvervloesem/humble-explorer/pull/11
* Set 5% threshold for codecov by @koenvervloesem in https://github.com/koenvervloesem/humble-explorer/pull/13
* Add usage docs by @koenvervloesem in https://github.com/koenvervloesem/humble-explorer/pull/16
* Make address filter a reactive attribute by @koenvervloesem in https://github.com/koenvervloesem/humble-explorer/pull/17

**Full Changelog**: https://github.com/koenvervloesem/humble-explorer/compare/v0.2.0...v0.3.0

Version 0.2.0 (2022-12-02)
==========================

* Timestamps within the same second are rendered with the same color.
* Each Bluetooth address is rendered with its own color for easier recognition of devices.

Version 0.1.1 (2022-12-01)
==========================

Fixes a ModuleNotFoundError.

Version 0.1.0 (2022-12-01)
==========================

Initial version of HumBLE Explorer.
