#!/usr/bin/env python3
"""
example.py

Example of using pypahdb to decompose an astronomical PAH spectrum.
"""

import importlib_resources
from pypahdb.decomposer import Decomposer
from pypahdb.observation import Observation

if __name__ == "__main__":
    # JWST sample data (in IPAC format).
    file_path = importlib_resources.files("pypahdb")
    data_file = file_path / "resources/sample_data_VV114E.tbl"

    # Construct an Observation object.
    obs = Observation(data_file)

    # Pass the Observation's spectrum to Decomposer, which performs the fit.
    pahdb_fit = Decomposer(obs.spectrum)

    # Save the fit to disk, both as a PDF and FITS file.
    pahdb_fit.save_pdf("VV114E_pypahdb_tbl_example.pdf", domaps=False)
    pahdb_fit.save_fits("VV114E_pypahdb_tbl_example.fits", header=obs.header)
