rivalcfg: Configure SteelSeries gaming mice
===========================================

|Github| |Discord| |PYPI Version| |Github Actions| |Black| |License|

Rivalcfg is a **Python library** and a **CLI utility program** that allows you
to configure SteelSeries gaming mice on Linux and Windows (probably works on
BSD and Mac OS too, but not tested).

I first created this program to configure my Rival 100 and the original Rival
mice, then I added support for other Rival devices thanks to contributors.
Today this project aims to support any SteelSeries gaming mice (Rival,
Sensei,...).

   **IMPORTANT:** This is an unofficial software. It was made by reverse
   engineering devices and is not supported nor approved by SteelSeries.

.. figure:: https://flozz.github.io/rivalcfg/_images/steelseries_mice.jpg
   :alt: SteelSeries Gaming Mice

If you have any trouble running this software, please open an issue on Github:

* https://github.com/flozz/rivalcfg/issues


Documentation
-------------

Main topics:

* `Requirements <https://flozz.github.io/rivalcfg/requirements.html>`_
* `Installing Rivalcfg <https://flozz.github.io/rivalcfg/install.html>`_
* `Documentation of supported devices <https://flozz.github.io/rivalcfg/devices/index.html>`_
* `FAQ <https://flozz.github.io/rivalcfg/faq.html>`_
* `Contributing <https://flozz.github.io/rivalcfg/contributing.html>`_ (please read before opening issues and PRs 😀️)

... and more at:

* https://flozz.github.io/rivalcfg/


Supported Devices
-----------------

.. devices-list-start

SteelSeries Aerox 3:

+--------------------------------------------------------------+-----------+
| SteelSeries Aerox 3                                          | 1038:1836 |
+--------------------------------------------------------------+-----------+

SteelSeries Aerox 3 Wireless:

+--------------------------------------------------------------+-----------+
| SteelSeries Aerox 3 Wireless (wired mode)                    | 1038:183a |
+--------------------------------------------------------------+-----------+
| SteelSeries Aerox 3 Wireless (2.4 GHz wireless mode)         | 1038:1838 |
+--------------------------------------------------------------+-----------+

SteelSeries Aerox 5 Wireless:

+--------------------------------------------------------------+-----------+
| SteelSeries Aerox 5 Wireless (wired mode)                    | 1038:1854 |
+--------------------------------------------------------------+-----------+
| SteelSeries Aerox 5 Wireless (2.4 GHz wireless mode)         | 1038:1852 |
+--------------------------------------------------------------+-----------+

SteelSeries Aerox 9 Wireless:

+--------------------------------------------------------------+-----------+
| SteelSeries Aerox 9 Wireless (wired mode)                    | 1038:185a |
+--------------------------------------------------------------+-----------+
| SteelSeries Aerox 9 Wireless (2.4 GHz wireless mode)         | 1038:1858 |
+--------------------------------------------------------------+-----------+

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

SteelSeries Prime:

+--------------------------------------------------------------+-----------+
| SteelSeries Prime                                            | 1038:182e |
+--------------------------------------------------------------+-----------+
| SteelSeries Prime Rainbow 6 Siege Black Ice Edition          | 1038:182a |
+--------------------------------------------------------------+-----------+
| SteelSeries Prime CS:GO Neo Noir Edition                     | 1038:1856 |
+--------------------------------------------------------------+-----------+

SteelSeries Prime Wireless:

+--------------------------------------------------------------+-----------+
| SteelSeries Prime Wireless (wired mode)                      | 1038:1842 |
+--------------------------------------------------------------+-----------+

SteelSeries Prime Wireless:

+--------------------------------------------------------------+-----------+
| SteelSeries Prime Wireless (2.4 GHz wireless mode)           | 1038:1840 |
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
| SteelSeries Rival 3 (firmware v0.37.0.0)                     | 1038:184c |
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

SteelSeries Rival 300S:

+--------------------------------------------------------------+-----------+
| SteelSeries Rival 300S                                       | 1038:1810 |
+--------------------------------------------------------------+-----------+

SteelSeries Rival 310:

+--------------------------------------------------------------+-----------+
| SteelSeries Rival 310                                        | 1038:1720 |
+--------------------------------------------------------------+-----------+
| SteelSeries Rival 310 CS:GO Howl Edition                     | 1038:171e |
+--------------------------------------------------------------+-----------+
| SteelSeries Rival 310 PUBG Edition                           | 1038:1736 |
+--------------------------------------------------------------+-----------+

SteelSeries Rival 3 Wireless:

+--------------------------------------------------------------+-----------+
| SteelSeries Rival 3 Wireless (2.4 GHz mode)                  | 1038:1830 |
+--------------------------------------------------------------+-----------+

SteelSeries Rival 500:

+--------------------------------------------------------------+-----------+
| SteelSeries Rival 500                                        | 1038:170e |
+--------------------------------------------------------------+-----------+

SteelSeries Rival 600:

+--------------------------------------------------------------+-----------+
| SteelSeries Rival 600                                        | 1038:1724 |
+--------------------------------------------------------------+-----------+
| SteelSeries Rival 600 Dota 2 Edition                         | 1038:172e |
+--------------------------------------------------------------+-----------+

SteelSeries Rival 650 Wireless:

+--------------------------------------------------------------+-----------+
| SteelSeries Rival 650 Wireless (wired mode)                  | 1038:172b |
+--------------------------------------------------------------+-----------+
| SteelSeries Rival 650 Wireless (2.4 GHz wireless mode)       | 1038:1726 |
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

SteelSeries Sensei TEN:

+--------------------------------------------------------------+-----------+
| SteelSeries Sensei TEN                                       | 1038:1832 |
+--------------------------------------------------------------+-----------+
| SteelSeries Sensei TEN CS:GO Neon Rider Edition              | 1038:1834 |
+--------------------------------------------------------------+-----------+

.. devices-list-end


Supporting this project
-----------------------

Wanna support this project?

* `☕️ Buy me a coffee <https://www.buymeacoffee.com/flozz>`__,
* `❤️ sponsor me on Github <https://github.com/sponsors/flozz>`__,
* `💵️ or give me a tip on PayPal <https://www.paypal.me/0xflozz>`__.


Changelog
---------

* **Rivalcfg NEXT:** [4.8.0]

  Features that are implemented on ``master`` and that will be released in the
  next Rivalcfg version:

  * Added Python 3.11 support

* **4.7.0:**

  * Add initial Aerox 9 Wireless support (#188)
  * Add Aerox 5 Wireless support (#184)
  * Fix inverted firmware version minor and major digits
  * Fix crash when reading battry level of a device in sleep mode
  * Improve udev rules reloading
  * Rival 100: Rivalcfg is now able to read the firmware version of this device
    (#179, @staticssleever668)

* **4.6.0:**

  * Add support for the Prime Wireless mouse (#172)
  * Aerox 3 Wireless support improved:

    * Sleep timer support implemented
    * Dim timer support implemented
    * Brightness removed to support Dim timer (it is still possible to dim the
      LED by setting darker colors)

  * Fix a crash when printing debug information with udev rules not installed
  * Remove Python 2.7 compatibility code

* **4.5.0:**

  * Do not try to open devices when not needed (#170)
  * Add support for SteelSeries Prime Rainbow 6 Siege Black Ice Edition
    (1038:182A)
  * Add support for SteelSeries Prime CS:GO Neo Noir Edition (1038:1856)
  * Add initial support for the Rival 3 Wireless mouse (#146)
  * Add initial support for the Rival 650 mouse (#112)

* **4.4.0:**

  * Add Prime support (#169, @sephiroth99)
  * Add Aerox 3 (non wireless version) support (#156)
  * Add Aerox 3 Wireless support (#167)
  * Save devices settings on disk
  * Add Black (code formatter)
  * Drop Python 3.5 support
  * **WARNING:** This version will be the last one to support Python 2.7

* **4.3.0:**

  * Fixes Sensei TEN default config (#158)
  * Adds the ``--print-udev`` to generate udev rules and print them to ``stdout`` (#157)
  * CLI: Displays a usage message when no argument was given (#152)
  * CLI: Write udev warning message to ``stderr`` instead of ``stdout``
  * Adds a ``--print-debug`` option to display various information
  * Adds a ``--firmware-version`` option to display the firmware version of some devices
  * Rivalcfg can now read the firmware version of the following devices:

    * Rival 3
    * Rival 300
    * Rival 310
    * Rival 500
    * Rival 700 / 710
    * Sensei 310
    * Sensei TEN

* **4.2.0:**

  * Rival 3: support of firmware v0.37.0.0 (#147)
  * Support of the Sensei TEN (1038:1832)
  * Support of the Sensei TEN CS:GO Neon Rider Edition (1038:1834)
  * Rival 500:

    * Handles color shift
    * Handles button mapping

* **4.1.0:**

  * Support of the Rival 300S

  * Rival 310 support improved:

    * Support of button mapping

  * Sensei 310 support improved:

    * Support of button mapping

  * Rival 3 support improved:

    * Colors can now be defined separately
    * Button mapping support implemented
    * Light effects support implemented

* **4.0.0:**

  * Full rewrite of most parts of the software
  * Mice are now grouped by families to reduce code duplication
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
    * A document was added to help contribute
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

  * Regressions:

    The following things were removed for this release:

    * Sensei Ten: this mouse needs more work to be added back.
    * Colorshift of the Rival 500: this feature needs more work to be added back.

Older changelog entries were moved to the `CHANGELOG.rst
<https://github.com/flozz/rivalcfg/blob/master/CHANGELOG.rst>`_ file.


.. |Github| image:: https://img.shields.io/github/stars/flozz/rivalcfg?label=Github&logo=github
   :target: https://github.com/flozz/rivalcfg

.. |Discord| image:: https://img.shields.io/badge/chat-Discord-8c9eff?logo=discord&logoColor=ffffff
   :target: https://discord.gg/P77sWhuSs4

.. |PYPI Version| image:: https://img.shields.io/pypi/v/rivalcfg?logo=python&logoColor=f1f1f1
   :target: https://pypi.org/project/rivalcfg/

.. |Github Actions| image:: https://img.shields.io/github/workflow/status/flozz/rivalcfg/Lint%20and%20Tests/master
   :target: https://github.com/flozz/rivalcfg/actions

.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://black.readthedocs.io/en/stable/

.. |License| image:: https://img.shields.io/github/license/flozz/rivalcfg
   :target: https://github.com/flozz/rivalcfg/blob/master/LICENSE
