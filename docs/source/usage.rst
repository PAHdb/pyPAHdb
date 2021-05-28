.. sectnum::
   :start: 4

=====
Usage
=====

Sample code for using pypahdb is shown below and is included in the pypahdb package
as ``examples/example_tbl.py``. The example uses the bundled  spectrum,
``sample_data_NGC7023.tbl``.

.. code-block:: python

    import pkg_resources

    from pypahdb.decomposer import Decomposer
    from pypahdb.observation import Observation

    # A provided sample data file (in FITS format).
    file_path = 'resources/sample_data_NGC7023.tbl'
    data_file = pkg_resources.resource_filename('pypahdb', file_path)

    # Construct an Observation object.
    obs = Observation(data_file)

    # Pass the Observation's spectrum to Decomposer, which performs the fit.
    pahdb_fit = Decomposer(obs.spectrum)

    # Write the fit to file.
    pahdb_fit.save_pdf('NGC7023_pypahdb.pdf')
    pahdb_fit.save_fits('NGC7023_pypahdb.fits', header=obs.header)


Details
---------

Let's briefly explore what the code presented above is doing.

We begin by importing the ``Decomposer`` and ``Observation`` classes from pypahdb. The
``pkg_resources`` package is used to dynamically load the sample data, since it's 
included in the package.

.. code-block:: python

    import pkg_resources

    from pypahdb.decomposer import Decomposer
    from pypahdb.observation import Observation

    # A provided sample data file (in FITS format).
    file_path = 'resources/sample_data_NGC7023.tbl'
    data_file = pkg_resources.resource_filename('pypahdb', file_path)

The included example IPAC table, ``sample_data_NGC7023.tbl``, contains an
astronomical spectrum, as shown below:

.. image:: figures/ngc7023_spectrum.png
   :align: center

The file is parsed into an ``Observation`` object by instantiating it, passing the path
to the file as its only argument:

.. code-block:: python

    # Construct an Observation object.
    obs = Observation(data_file)

Note that this file needn't necessarily be an IPAC table (.tbl), but could also be a
YAAR FITS file (.fits). The Observation construction above is the same in either case.

The actual decomposition is performed by creating the ``Decomposer`` instance. We pass ``obs.spectrum`` as its only positional argument, since the decomposition only requires the x-y (paired) data, and none of the associated metadata.

.. code-block:: python

    # Pass the Observation's spectrum to Decomposer, which performs the fit.
    pahdb_fit = Decomposer(obs.spectrum)

The ``Decomposer`` object has methods for producing output from the fitting process, namely ``save_pdf`` and ``save_fits``. They each require a positional argument containing the desired output filename.

.. code-block:: python

    # Write the fit to file.
    pahdb_fit.save_pdf('NGC7023_pypahdb.pdf')
    pahdb_fit.save_fits('NGC7023_pypahdb.fits', header=obs.header)

We explicitly pass ``header=obs.header`` into the ``save_fits`` method, but you can
choose an arbitrary header to be associated with this FITS file if needed (i.e., if you wanted to customize the header).
