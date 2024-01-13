Things to do when releasing a new version
=========================================

This file is a memo for the maintainer.


0. Checks
---------

* Check the device list is up to date in the README (``./scripts/update_readme_devices.py``)
* Check SSDB is up to date (``nox -s update_ssdb``)
* Check copyright years in ``doc/conf.py``


1. Release
----------

* Update version number in ``setup.py``
* Update version number in ``rivalcfg/version.py``
* Edit / update changelog in ``README.rst``
* Commit / tag (``git commit -m vX.Y.Z && git tag vX.Y.Z && git push && git push --tags``)


2. Publish PyPI package
-----------------------

Publish source dist and wheels on PyPI.

→ Automated :)


3. Publish Github Release
-------------------------

* Make a release on Github
* Add changelog
