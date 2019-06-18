.. sectnum::
   :start: 2

Design
============

pypahdb analyzes spectroscopic observations (including spectral maps)
and characterizes the PAH emission using a database-fitting approach,
providing the PAH ionization and size fractions.

The package is imported with the following statement:

.. code-block:: python

    import pypahdb

Flowchart
-----------------

.. figure:: figures/fig_flowchart.png
   :align: center

   pypahdb flowchart. (1) Astronomical spectroscopic data is loaded,
   whether loaded rom FITS or ASCII files. (2) An over-sampled
   pre-computed matrix of PAH spectra is loaded and interpolated onto
   the wavelength grid of the astronomical
   observations. Database-fitting is performed using non-negative
   least-squares (NNLS), which yields the contribution of an
   individual PAH molecule to the total fit. As a result, we obtain a
   breakdown of the model fit in terms of PAH charge and size. (3) The
   results are written to disk as a single FITS file and as a PDF
   summarizing the results (one page per pixel, if a spectral cube is
   provided as input).

The general program methodology is encapsulated in the flowchart
presented in the figure above and is as follows:

(1) Read-in a file containing spectroscopic PAH observations of an
    astronomical object. This functionality is provided by the class
    ``Observation``, which is implemented in ``observation.py``. It is
    the responsibility of the user to ensure all non-PAH emission
    components have been removed from the spectrum. The class uses a
    fall-through try-except chain to attempt to read the given
    filename using the facilities provided by ``astropy.io``. The
    spectroscopic data is stored as a ``specutils.Spectrum1D``
    object. The ``Spectrum1D`` class provides functionality to convert
    between different coordinate representations. Below is example
    Python code demonstrating the use of the class. The file
    ``sample_data_NGC7023.tbl`` in this demonstration can be
    found in the ``examples`` directory that is part of the pyPAHdb
    package. The output of the following code-block is shown in the
    flowchart.

.. code-block:: python

    import matplotlib.pyplot as plt
    from pypahdb.observation import Observation

    filename = 'sample_data_NGC7023.tbl'
    obs = Observation(filename)
    s = obs.spectrum
    plt.plot(s.spectral_axis, s.flux,0,0,:])
    plt.show()

(2) Decompose the observed PAH emission into contributions from
    different PAH subclasses, here charge and size. This functionality
    is provided by the class ``Decomposer``, which is implemented in
    ``decomposer.py``. The class takes as input a ``Spectrum1D`` object,
    of which it creates a deep copy and calls the
    ``Unit.to` method to convert the abscissa units
    to wavenumber. Subsequently, a pre-computed ``numpy`` matrix of
    highly oversampled PAH emission spectra stored as a ``pickle`` is
    loaded from file. Utilizing ``numpy.interp``, each of the PAH
    emission spectra, represented by a single column in the
    pre-computed matrix, is interpolated onto the frequency grid (in
    wavenumber) of the input spectrum. This process is parallelized
    using the ``multiprocessing`` package. ``optimize.nnls`` is used
    to perform a non-negative least-squares (NNLS) fit of the
    pre-computed spectra to the input spectra. NNLS is chosen because
    it is appropriate to the problem, fast, and always converges. The
    solution vector (weights) is stored as an attribute and considered
    private. Combining lazy instantiation and Python's @property, the
    results of the fit and the breakdown can be retrieved. In case the
    input spectrum represents a spectral cube and where possible, the
    calculations are parallelized across each pixel using, again, the
    ``multiprocessing`` package. Below is example code demonstrating
    the use of the class and extends the previous code-block. The
    output of the code-block is shown in the flowchart.

.. code-block:: python

    from pypahdb.decomposer import Decomposer

    result = Decomposer(obs.spectrum)
    s = result.spectrum
    plt.plot(s.spectral_axis, s.flux[0,0,:], 'x')
    plt.plot(s.spectral_axis, result.fit[:,0,0])
    plt.show()

(3) Produce output to file given a ``Decomposer`` object. Previously
    stored within the ``Writer`` class, this functionality is now
    contained within ``Decomposer`` itself. The output serves to
    summarize the results from the ``Decomposer`` class so that a user
    may assess the quality of the fit and store the PAH
    characteristics of their astronomical observations. The class uses
    ``astropy.fits`` to write the PAH characteristics to a FITS file
    and the ``matplotlib`` package to generate a PDF summarizing the
    results. The class will attempt to incorporate relevant
    information from any (FITS) header provided. Below is example code
    demonstrating the use of the class, which extends the previous
    code-block. The size breakdown part of the generated PDF output is
    shown in the flowchart.

.. code-block:: python

    result.save_pdf('NGC7023_pypahdb.pdf')
    result.save_fits('NGC7023_pypahdb.fits', header=obs.header)




Supported data formats
-----------------------

Presently, pypahdb supports IPAC tables and Spitzer FITS files.
