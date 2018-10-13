=====
Usage
=====

The general flow for using pyPAHdb is shown below. See the tutorial series for detailed explanations of how to best use pyPAHdb for your purposes.

.. code-block:: python

    import pypahdb

    # Construct an observation object.
    observation = pyPAHdb.observation('NGC7023.fits')

    # Pass its spectrum to decomposer, which performs the fit.
    result = pyPAHdb.decomposer(observation.spectrum)

    # Write the results to disk (by default, both a .FITS and .PDF file).
    pyPAHdb.writer(result, header=observation.header)