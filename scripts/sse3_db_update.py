#!/usr/bin/env python3

"""
This script download the latest SteelSeries Engin 3 (SSE3) and extract the list
of all supported mice.

Requirements:

* 7zip
* wget
* natsort (pypi)
"""


import os
import sys
import csv
import glob
import json
import sqlite3
import tempfile
import subprocess


URL_LATEST_SSGG = "https://fr.steelseries.com/gg/downloads/gg/latest/windows"

SQL_LIST_MICE = """
SELECT "1038" AS vendor_id,
       PRINTF("%04x", product_id & 0x0000FFFF) AS product_id,
       name,
       full_name,
       settings
FROM devices
WHERE type = 1 AND name != "generic_bootloader";
"""


def download_sse3(url, filename):
    print("\n* Downloading SSE3...")
    subprocess.check_output(["wget", "-O", filename, url])
    if not os.path.isfile(filename):
        print("  -> Unable to downlod SSE3. Abort.")
        sys.exit(1)
    print("  -> Done.")


def extract_sse3(filename):
    print("\n* Extracting SSE3 files...")
    subprocess.check_output(["7z", "x", "-y", "--", filename])
    print("  -> Done.")


def find_sql_migration_scripts():
    print("\n* Searching SQL micration scripts...")
    sql_files = sorted(
        glob.glob("**/*.sql", recursive=True), key=lambda path: os.path.basename(path)
    )
    if len(sql_files) == 0:
        print("  -> No SQL file found. Abort.")
        sys.exit(1)
    print("  -> %i files found." % len(sql_files))
    return sql_files


def build_database(sql_files):
    print("\n* Building the database...")
    db_conn = sqlite3.connect(":memory:")
    cur = db_conn.cursor()
    for sql_file in sql_files:
        if "migratedTables" in sql_file:
            print("  * Skipping %s..." % sql_file)
            continue
        print("  * Running %s..." % sql_file)
        with open(sql_file, "r") as f:
            sql = f.read()
            for sql_part in sql.split("\n\n"):
                try:
                    cur.executescript(sql_part)
                except sqlite3.OperationalError as e:
                    print("    -> Error: %s" % str(e))
    print("  -> Done.")
    return db_conn


def list_devices(db_conn):
    print("\n* Listing device...")
    cur = db_conn.cursor()
    cur.execute(SQL_LIST_MICE)
    print("  -> Done.")
    return cur.fetchall()


def write_csv(data, filename):
    print("\n* Writingg output CSV: %s..." % filename)
    with open(filename, "w") as f:
        csvfile = csv.writer(f)
        csvfile.writerow(
            [
                "vendor_id",
                "product_id",
                "name",
                "full_name",
                "default_settings",
            ]
        )
        for pid, vid, name, full_name, settings in data:
            csvfile.writerow(
                [
                    pid,
                    vid,
                    name,
                    full_name,
                    json.dumps(json.loads(settings)),
                ]
            )
    print("  -> Done.")


def print_result(data):
    _table = "| %-4s | %-4s | %-30s | %-29s |"
    print("\n* Found mice:")

    print("-" * 80)
    print(_table % ("VID", "PID", "NAME", "FULL NAME"))
    print("-" * 80)

    for pid, vid, name, full_name, _ in data:
        print(_table % (pid, vid, name, full_name))

    print("-" * 80)

    print("\n==> %i mice found!\n" % len(data))


def main():
    output_csv = None
    if len(sys.argv) == 2:
        output_csv = os.path.abspath(sys.argv[1])

    tmpdir = tempfile.TemporaryDirectory()
    os.chdir(tmpdir.name)

    download_sse3(URL_LATEST_SSGG, "./sse3.exe")
    extract_sse3("./sse3.exe")
    sql_files = find_sql_migration_scripts()
    db_conn = build_database(sql_files)
    data = list_devices(db_conn)
    if output_csv:
        write_csv(data, output_csv)
    print_result(data)

    tmpdir.cleanup()


if __name__ == "__main__":
    main()
