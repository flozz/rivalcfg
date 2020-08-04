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


Installing Rivalcfg
-------------------

* https://flozz.github.io/rivalcfg/install.html


Documentation
-------------

* https://flozz.github.io/rivalcfg/


Supported Devices
-----------------

.. devices-list-start

SteelSeries Kana v2:

+--------------------------------------------------------------+-----------+
| SteelSeries Kana v2                                          | 1038:137a |
+--------------------------------------------------------------+-----------+

SteelSeries Kinzu v2:

+--------------------------------------------------------------+-----------+
| SteelSeries Kinzu v2                                         | 1038:1366 |
+--------------------------------------------------------------+-----------+
| SteelSeries Kinzu v2                                         | 1038:1378 |
+--------------------------------------------------------------+-----------+

SteelSeries Rival 100 / SteelSeries Rival 105:

+--------------------------------------------------------------+-----------+
| SteelSeries Rival 100                                        | 1038:1702 |
+--------------------------------------------------------------+-----------+
| SteelSeries Rival 100 (Dell China)                           | 1038:170a |
+--------------------------------------------------------------+-----------+
| SteelSeries Rival 100 Dota 2 Edition (retail)                | 1038:170b |
+--------------------------------------------------------------+-----------+
| SteelSeries Rival 100 Dota 2 Edition (Lenovo)                | 1038:170c |
+--------------------------------------------------------------+-----------+
| SteelSeries Rival 105                                        | 1038:1814 |
+--------------------------------------------------------------+-----------+

SteelSeries Rival 110 / SteelSeries Rival 106:

+--------------------------------------------------------------+-----------+
| SteelSeries Rival 110                                        | 1038:1729 |
+--------------------------------------------------------------+-----------+
| SteelSeries Rival 106                                        | 1038:1816 |
+--------------------------------------------------------------+-----------+

SteelSeries Rival 3:

+--------------------------------------------------------------+-----------+
| SteelSeries Rival 3                                          | 1038:1824 |
+--------------------------------------------------------------+-----------+

SteelSeries Rival 300 / SteelSeries Rival:

+--------------------------------------------------------------+-----------+
| SteelSeries Rival                                            | 1038:1384 |
+--------------------------------------------------------------+-----------+
| SteelSeries Rival Dota 2 Edition                             | 1038:1392 |
+--------------------------------------------------------------+-----------+
| SteelSeries Rival 300                                        | 1038:1710 |
+--------------------------------------------------------------+-----------+
| SteelSeries Rival 300 Fallout 4 Edition                      | 1038:1712 |
+--------------------------------------------------------------+-----------+
| SteelSeries Rival 300 Evil Geniuses Edition                  | 1038:171c |
+--------------------------------------------------------------+-----------+
| SteelSeries Rival 300 CS:GO Fade Edition                     | 1038:1394 |
+--------------------------------------------------------------+-----------+
| SteelSeries Rival 300 CS:GO Hyper Beast Edition              | 1038:171a |
+--------------------------------------------------------------+-----------+
| SteelSeries Rival 300 CS:GO Fade Edition (stm32)             | 1038:1716 |
+--------------------------------------------------------------+-----------+
| SteelSeries Rival 300 Acer Predator Edition                  | 1038:1714 |
+--------------------------------------------------------------+-----------+
| SteelSeries Rival 300 HP OMEN Edition                        | 1038:1718 |
+--------------------------------------------------------------+-----------+

SteelSeries Rival 310:

+--------------------------------------------------------------+-----------+
| SteelSeries Rival 310                                        | 1038:1720 |
+--------------------------------------------------------------+-----------+
| SteelSeries Rival 310 CS:GO Howl Edition                     | 1038:171e |
+--------------------------------------------------------------+-----------+
| SteelSeries Rival 310 PUBG Edition                           | 1038:1736 |
+--------------------------------------------------------------+-----------+

SteelSeries Rival 600:

+--------------------------------------------------------------+-----------+
| SteelSeries Rival 600                                        | 1038:1724 |
+--------------------------------------------------------------+-----------+
| SteelSeries Rival 600 Dota 2 Edition                         | 1038:172e |
+--------------------------------------------------------------+-----------+

SteelSeries Rival 700 / SteelSeries Rival 710:

+--------------------------------------------------------------+-----------+
| SteelSeries Rival 700                                        | 1038:1700 |
+--------------------------------------------------------------+-----------+
| SteelSeries Rival 710                                        | 1038:1730 |
+--------------------------------------------------------------+-----------+

SteelSeries Rival 95 / SteelSeries Rival 100 PC Bang:

+--------------------------------------------------------------+-----------+
| SteelSeries Rival 95                                         | 1038:1706 |
+--------------------------------------------------------------+-----------+
| SteelSeries Rival 95 MSI Edition                             | 1038:1707 |
+--------------------------------------------------------------+-----------+
| SteelSeries Rival 95 PC Bang                                 | 1038:1704 |
+--------------------------------------------------------------+-----------+
| SteelSeries Rival 100 PC Bang                                | 1038:1708 |
+--------------------------------------------------------------+-----------+

SteelSeries Sensei 310:

+--------------------------------------------------------------+-----------+
| SteelSeries Sensei 310                                       | 1038:1722 |
+--------------------------------------------------------------+-----------+

SteelSeries Sensei [RAW]:

+--------------------------------------------------------------+-----------+
| SteelSeries Sensei [RAW]                                     | 1038:1369 |
+--------------------------------------------------------------+-----------+
| SteelSeries Sensei [RAW] Diablo III Edition                  | 1038:1362 |
+--------------------------------------------------------------+-----------+
| SteelSeries Sensei [RAW] Guild Wars 2 Edition                | 1038:136d |
+--------------------------------------------------------------+-----------+
| SteelSeries Sensei [RAW] CoD Black Ops II Edition            | 1038:136f |
+--------------------------------------------------------------+-----------+
| SteelSeries Sensei [RAW] World of Tanks Edition              | 1038:1380 |
+--------------------------------------------------------------+-----------+
| SteelSeries Sensei [RAW] Heroes of the Storm Edition         | 1038:1390 |
+--------------------------------------------------------------+-----------+

.. devices-list-end


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
    * Support of the Rival 106 (#84, @SethDusek)

  * Some devices gained a better support:

    * Rival 300 / Original Rival family

      * Support of buttons mapping

    * Rival 700 / 710

      * Support of gradients / Color shift (#129, @nixtux)

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
