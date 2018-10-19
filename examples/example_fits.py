#!/usr/bin/env python3
"""
example.py

Example of using pypahdb to decompose an astronomical PAH spectrum.
"""

import pkg_resources
import time

from pypahdb.decomposer import Decomposer
from pypahdb.observation import Observation


if __name__ == '__main__':

    # A warning since this example is somewhat CPU intensive,
    # requests user input to continue.
    print('Note, this FITS cube contains 210 pixels; this example may take '
          'some time to run (for reference, approximately 3 minutes on a '
          'dual core Haswell CPU).')
    user_input = input('Do you wish to continue? y/[n]: ')
    if user_input.lower() not in ['y', 'yes']:
        print('Aborting.')
        raise SystemExit()

    # Track the time elapsed.
    start = time.perf_counter()

    # The sample data (in FITS format).
    file_path = 'data/sample_data_NGC7023.fits'
    data_file = pkg_resources.resource_filename('pypahdb', file_path)

    # Construct an Observation object.
    obs = Observation(data_file)

    # Pass the Observation's spectrum to Decomposer, which performs the fit.
    pahdb_fit = Decomposer(obs.spectrum)

    # Write the results to file.
    pahdb_fit.save_pdf('NGC7023_pypahdb_fits_example.pdf')
    pahdb_fit.save_fits('NGC7023_pypahdb_fits_example.fits', header=obs.header)

    # Print the time elapsed.
    end = time.perf_counter()
    print('Time elapsed: ', end - start, 'seconds.')
