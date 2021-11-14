# SteelSeries Mouse Database

This folder contains databases listing all known SteelSeries mice.


## Databases

There is 3 databases:

* `other.db.csv` lists old SteelSeries mice that are not supported by the SteelSeries Engine 2/3.
* `sse2.db.csv` was extracted from the SteelSeries Engine 2 and lists mice supported by it.
* `sse3.db.csv` is extracted from the SteelSeries Engine 3 / GG Engine and lists mice supported by it. This database can be updated with a script, see below.

**NOTE:** some device can be listed in both sse2 and sse3 databases.


## Updating the SSE3 database

To update the `sse3.db.csv` database, you will have to install nox:

    pip3 install nox

You will also need 7zip and wget. You can install them with the following command on Dabian and Ubuntu:

    sudo apt install wget p7zip

Then just run the following command to update the db:

    nox --session update_ssdb
