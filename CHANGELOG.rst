=========
Changelog
=========

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
