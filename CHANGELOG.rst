Rivalcfg Changelog
==================


Rivalcfg v4.x
-------------

The changelog of Rivalcfg v4.x is in `the README <./README.rst>`_.


Rivalcfg v3.x
-------------

* **3.12.0:**

  * Experimental support of the Rival 310 PUBG Edition (#109)
  * Experimental support of the Sensei RAW (thx @cbergqvist, #106)
  * Experimental support of the Sensei Ten (thx @beardstorm, #94)

* **3.11.0:** Adds support of a later version if the Rival 300 CS:GO Fade Edition (thx @platyple, #105)
* **3.10.0:** Initial experimental support of the Rival 700 (thx @nixtux, #101)
* **3.9.0:**

  * Experimental support of the Rival 95 (thx @LAKostis, #97)
  * Experimental support of the Rival 105 (thx @vonsowic, #98)
  * Fixes an issue with colorshift (rgbuniversal handler) on Python 3 (thx @uglynewt, #96)

* **3.8.0:**

  * Experimental support of Sensei 310 (thx @tobozo #82, @FFY00 #43)
  * Improved support of Rival 310 (still experimental)

* **3.7.0:** Initial support of the Rival 710 (#91, thanks @mobaradev)
* **3.6.1:** Removes the call of a deprecated function that have been removed from Python 3.8 (#86)
* **3.6.0:** Improved error handeling when sending commands to mice (thanks @Demon000, #76)
* **3.5.0:** Support of the Rival 100 Dota 2 Edition (#75)
* **3.4.0:** Support of the Kana V2 mouse (thanks @pqlaz, #74)
* **3.3.0:** Support of the Acer Predator Gaming Mouse (a rebranded Rival 300) (#72)
* **3.2.0:**

  * Support of the Rival 300 Dota 2 Edition (#67, @virrim)
  * Fixes case issue in udev rule file (#68, @hungarian-notation)

* **3.1.0:**

  * Support of sensitivity commands for Rival 500 (#65, @hungarian-notation)
  * Fix of the reset command on Rival 600 (#66, @ergor)

* **3.0.0**:

  * Adds support of the Rival 300 HP Omen Edition (#52, @FadedCoder)
  * Adds experimental support of the Rival 600 (#60, @ergor)
  * Varous fixes

* **3.0.0-beta1:**

  * Support of the Rival 110
  * Support of the Heroes of the Storm (Sensei Raw)
  * Partial support of the Rival 310
  * Partial support of the Rival 500
  * Microsoft Windows (and MacOS X?) support
  * rivalcfg now uses the ``hidapi`` lib instead of manipulating udev directly
  * Code refactored (almost all API changed)
  * Various bug fixes


Rivalcfg v2.x
-------------

* **2.6.0:** Add CS:GO Hyperbeast Edition support (thanks @chriscoyfish, #33)
* **2.5.3:** Minor typo fixes for cli (thanks @chriscoyfish, #31)
* **2.5.2:** Fixes Rival 300 with updated firmware not working (#5, #25, #28, special thanks to @Thiblizz)
* **2.5.1:** Fixes mouse not recognized on system with more than 10 USB busses (#21)
* **2.5.0:** Rival 300 CS:GO Fade Edition support (thanks @Percinnamon, #20)
* **2.4.4:** Improves debug options
* **2.4.3:** Fixes an issue with Python 3 (#8)
* **2.4.2:** Fixes a TypeError with Python 3 (#7)
* **2.4.1:** Help improved
* **2.4.0:** Python 3 support (#4)
* **2.3.0:**

  * Rival and Rival 300 support is no more experimental
  * Improves the device listing (--list)
  * Fixes bug with color parsing in CLI (#1)
  * Fixes unrecognized devices path on old kernel (#2)

* **2.2.0:** Experimental Rival 300 support
* **2.1.1:** Includes udev rules in the package and automatically install the rules (if possible)
* **2.1.0:** Experimental original Rival support
* **2.0.0:** Refactored to support multiple mice


Rivalcfg v1.x
-------------

* **1.0.1:** Fixes the PyPI package
* **1.0.0:** Initial release
