rivalcfg: Configure SteelSeries gaming mice
===========================================

|Lint and Tests| |PYPI Version| |License| |Gitter|

rivalcfg is a **Python library** and a **CLI utility program** that allows you
to configure SteelSeries gaming mice on Linux and Windows (probably works on
BSD and Mac OS too, but not tested).

I first created this program to configure my Rival 100 and the original Rival
mice, then I added support for other Rival devices thanks to contributors.
Today this project aims to support any SteelSeries gaming mice (Rival,
Sensei,...).

   **NOTE:** This is an unofficial software. It was made by reverse engineering
   devices and is not supported nor approved by SteelSeries.

If you have any trouble running this software, please open an issue on Github:

* https://github.com/flozz/rivalcfg/issues


Changelog
---------

* **4.0.0:** ``[WORK IN PROGRESS]``

  * Full rewrite of most parts of the software
  * Mice are now grouped by family to reduce code duplication
  * Improved udev support on Linux:

    * Dynamically generate udev rules instead of maintaining a static file
    * Automatically check that the rules file is up to date
    * Adds a command to update udev rules

  * Improved testing:

    * Better coverage
    * Test the device output to avoid regressions

  * Improved documentation:

    * A Sphinx documentation was added instead of stacking everything in the
      README
    * Each device family now have its own documentation page to make it easier
      to understand
    * Python APIs are now documented
    * A document was added to help contributing
    * Installation instructions were updated to recommend using Python 3

  * New devices support was added:

    * Support of the Rival 100 Dota 2 Edition (retail version) (#17)
    * Support of the Rival 300 Fallout 4 Edition (#44)
    * Support of the Rival 310 CS:GO Howl Edition (#113)
    * Support of the Rival 3 (#111)
    * Support of the Rival 300 Evil Geniuses Edition
    * Support of the Rival 95 MSI Edition
    * Support of the Rival 95 PC Bang
    * Support of the Rival 100 PC Bang
    * Support of the Rival 100 (Dell China)
    * Support of the Rival 100 Dota 2 Edition (retail version)
    * Support of the Rival 600 Dota 2 Edition

  * Some devices gained a better support:

    * Rival 300 / Original Rival family (support of buttons mapping)

  * A generic support of mouse buttons mapping was added (rewriting of what was
    originally done for the Sensei [RAW]). The following devices now support
    it:

    * Rival 300 / Original Rival family
    * Sensei [RAW] family

Older changelog entries were moved in the `CHANGELOG.rst <./CHANGELOG.rst>`_ file.


.. |Lint and Tests| image:: https://github.com/flozz/rivalcfg/workflows/Lint%20and%20Tests/badge.svg?branch=master
   :target: https://github.com/flozz/rivalcfg/actions
.. |PYPI Version| image:: https://img.shields.io/pypi/v/rivalcfg.svg
   :target: https://pypi.python.org/pypi/rivalcfg
.. |License| image:: https://img.shields.io/pypi/l/rivalcfg.svg
   :target: https://github.com/flozz/rivalcfg/blob/master/LICENSE
.. |Gitter| image:: https://badges.gitter.im/gitter.svg
   :target: https://gitter.im/rivalcfg/Lobby
