#!/usr/bin/env python3
"""
example.py

Example of using pypahdb to decompose an astronomical PAH spectrum.
"""

import importlib_resources
from pypahdb.decomposer import Decomposer
from pypahdb.observation import Observation

if __name__ == "__main__":
    # Sample data (in FITS format).
    file_path = importlib_resources.files("pypahdb")
    data_file = file_path / "resources/sample_data_NGC7023.fits"

    # Construct an Observation object.
    obs = Observation(data_file)

    # Pass the Observation's spectrum to Decomposer, which performs the fit.
    pahdb_fit = Decomposer(obs.spectrum)

    # Write the results to file.
    # doplots is disabled due to significant CPU overhead
    pahdb_fit.save_pdf(
        "NGC7023_pypahdb_fits_example.pdf", header=obs.header, doplots=False
    )
    pahdb_fit.save_fits("NGC7023_pypahdb_fits_example.fits", header=obs.header)
