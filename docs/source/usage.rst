=====
Usage
=====

The general flow for using pyPAHdb is shown below. See the tutorial series for detailed explanations of how to best use pyPAHdb for your purposes.

.. code-block:: python

    from pypahdb.decomposer import Decomposer
    from pypahdb.observation import Observation

    # Construct an Observation object.
    obs = Observation('NGC7023.fits')

    # Pass the Observation's spectrum to Decomposer, which performs the fit.
    pahdb_fit = Decomposer(obs.spectrum)

    # Write the results to file
	pahdb_fit.save_pdf(filename='NGC7023_pypahdb.pdf')
	pahdb_fit.save_fits(filename='NGC7023_pypahdb.fits', header=obs.header)