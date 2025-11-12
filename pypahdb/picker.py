#!/usr/bin/env python3
"""
picker.py

Pick the precomputed matrix to use for decomposing an astronomical
spectrum.

This file is part of pypahdb - see the module docs for more
information.
"""
import json
import os
from glob import glob
from urllib.request import urlretrieve

import importlib_resources
from tqdm import tqdm

RELEASES_URL = "https://www.astrochemistry.org/pahdb/pypahdb/releases.json"


class Picker(object):
    """Pick the precomputed matrix to use for decomposing an astronomical
    spectrum.

    Attributes:
       _pkl_files: List of already downloaded precomputed matrices.
       _releases: List of available releases.
       _resources_dir: Path to the resources directory.
    """

    _pkl_files = []
    _releases = []
    _resources_dir = None

    def __init__(self):
        """Pick the precomputed matrix."""
        self._resources_dir = importlib_resources.files("pypahdb") / "resources"

        self._pkl_files = glob("*.pkl", root_dir=self._resources_dir)

    def pick(self, version=None):
        """Pick the precomputed matrix.

        Args:
            version (str): The version of the precomputed matrix to use or "picker" to show menu.

        Returns:
            pathlib.Path: The path to the precomputed matrix.
        """
        if self._pkl_files:
            if version is None:
                return self._resources_dir / next(reversed(sorted(self._pkl_files)))
            pkl_file = f"precomputed_v{version}.pkl"
            if pkl_file in self._pkl_files:
                return self._resources_dir / pkl_file

        json_file = self._resources_dir / "releases.json"
        print("downloading latests releases.json")

        self._download(RELEASES_URL, json_file)
        with open(json_file, "r") as f:
            self._releases = json.load(f)

        if (
            version is None
            or version == "picker"
            or version not in [r["version"] for r in self._releases]
        ):
            version = self._menu()

        pkl_file = f"precomputed_v{version}.pkl"
        if pkl_file in self._pkl_files:
            return self._resources_dir / pkl_file

        release = next(
            filter(lambda release: release["version"] == version, self._releases), None
        )

        print("downloading precomputed matrix")

        location = release["location"]
        if os.getenv("GITHUB_ACTIONS") == "true":
            location += "&github_actions=true"

        pkl_file = self._resources_dir / pkl_file

        self._download(location, pkl_file)

        return pkl_file

    def _download(self, url, filename):
        """Download url to filename."""

        def _report(t):
            last_b = [0]

            def inner(b=1, bsize=1, tsize=None):
                if tsize is not None:
                    t.total = tsize
                t.update((b - last_b[0]) * bsize)
                last_b[0] = b

            return inner

        with tqdm(
            unit="B",
            unit_scale=True,
            leave=False,
            miniters=1,
        ) as t:
            urlretrieve(url, filename=filename, reporthook=_report(t), data=None)

    def _menu(self):
        """Present the menu picker"""
        while True:
            print("-" * 80)
            print(
                "#  VERSION          DESCRIPTION                                  SIZE DOWNLOADED"
            )
            print("-" * 80)
            for i, release in enumerate(self._releases, start=1):
                downloaded = f"precomputed_v{release['version']}.pkl" in self._pkl_files
                print(
                    f"{i:<2} {release['version']:<16} {release['description']:41.41s} "
                    f"{release['size']:>7} {downloaded}"
                )
            print("-" * 80)
            print()
            select = input("select # : ")
            if select.isdigit():
                select = int(select)
                if select >= 1 and select <= len(self._releases):
                    return self._releases[select - 1]["version"]
