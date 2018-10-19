=====
Usage
=====

The general flow for using pyPAHdb is shown below. See the tutorial series for detailed explanations of how to best use pyPAHdb for your purposes.

.. code-block:: python

    import pkg_resources

    from pypahdb.decomposer import Decomposer
    from pypahdb.observation import Observation

    # The sample data file (in FITS format).
    file_path = 'data/sample_data_NGC7023.fits'
    data_file = pkg_resources.resource_filename('pypahdb', file_path)

    # Construct an Observation object.
    obs = Observation(data_file)

    # Pass the Observation's spectrum to Decomposer, which performs the fit.
    pahdb_fit = Decomposer(obs.spectrum)

    # Write the results to file.
    pahdb_fit.save_pdf('NGC7023_pypahdb.pdf')
    pahdb_fit.save_fits('NGC7023_pypahdb.fits', header=obs.header)