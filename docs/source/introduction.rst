Introduction
============

pyPAHdb is used to characterize emission from one of the most prevalent types of organic molecules in space, namely polycyclic aromatic hydrocarbons (PAHs). It leverages the detailed studies of organic molecules done at the NASA Ames Research Center. pyPAHdb is a streamlined Python version of the NASA Ames PAH IR Spectroscopic Database (PAHdb; `www.astrochemistry.org/pahdb <http://www.astrochemistry.org/pahdb>`_) suite of IDL tools. PAHdb has been extensively used to analyze and interpret the PAH signature from a plethora of emission sources, ranging from solar-system objects to entire galaxies. pyPAHdb decomposes astronomical PAH emission spectra into contributing PAH sub-classes in terms of charge and size using a database-fitting technique. The inputs for the fit are spectra constructed using the spectroscopic libraries of PAHdb and take into account the detailed photo-physics of the PAH excitation/emission process.

Academic reference
------------------

A white paper for pyPAHdb was presented at the Scipy 2018 conference as a conference proceeding. Please see `https://doi.org/10.25080/Majora-4af1f417-00f <https://doi.org/10.25080/Majora-4af1f417-00f>`_ for the full article in PDF form.

pyPAHdb details
---------------

The purpose of pyPAHdb is to derive astronomical parameters directly
from *JWST* observations, but the tool is not limited to *JWST*
observations alone. pyPAHdb is the light version of a full suite of
Python software tools\ [#]_ that is currently being developed, which
is an analog of the off-line IDL tools\ [#]_. A feature comparison is
presented in the table below. pyPAHdb will enable PAH experts and non-experts
alike to analyze and interpret astronomical PAH emission spectra.

.. [#] *AmesPAHdbPythonSuite*: `github.com/PAHdb/AmesPAHdbPythonSuite <https://github.com/PAHdb/AmesPAHdbPythonSuite>`_

.. [#] *AmesPAHdbIDLSuite*: `github.com/PAHdb/AmesPAHdbIDLSuite <https://github.com/PAHdb/AmesPAHdbIDLSuite>`_

.. raw:: latex

   \setlength{\tablewidth}{0.7\textwidth}


.. table:: Feature comparison between pyPAHdb and the full suites of
           off-line IDL/Python tools. Note: NNLS is non-negative
           least squares; FWHM is full-width at half-maximum of an
           emission profile; "uncertainties" in this context
           refers to handling observational spectroscopic uncertainties.

   +---------------------+----------+------------------+
   |                     | pyPAHdb  | IDL/Python tools |
   +=====================+==========+==================+
   | Included molecules. | Fixed    | User defined     |
   +---------------------+----------+------------------+
   | Excitation energy   | Fixed    | User defined     |
   +---------------------+----------+------------------+
   | Emission profile    | Fixed    | Selectable       |
   +---------------------+----------+------------------+
   | FWHM                | Fixed    | User defined     |
   +---------------------+----------+------------------+
   | Band redshift       | Fixed    | User defined     |
   +---------------------+----------+------------------+
   | Emission model      | Fixed    | Selectable       |
   +---------------------+----------+------------------+
   | NNLS                | ✓        | ✓                |
   +---------------------+----------+------------------+
   | Class breakdown     | ✓        | ✓                |
   +---------------------+----------+------------------+
   | Parallelization     | ✓        | ✓                |
   +---------------------+----------+------------------+
   | Handle uncertainties|          | ✓                |
   +---------------------+----------+------------------+

pyPAHdb analyzes spectroscopic observations (including spectral maps)
and characterizes the PAH emission using a database-fitting approach,
providing the PAH ionization and size fractions.

The package is imported using the following statement:

.. code-block:: python

    import pypahdb

.. figure:: figures/fig_flowchart.png
   :align: center

   pyPAHdb flowchart. (1) Astronomical spectroscopic data is loaded,
   whether represented in FITS or ASCII files. (2) An over-sampled
   pre-computed matrix of PAH spectra is loaded and interpolated onto
   the wavelength grid of the astronomical
   observations. Database-fitting is performed using non-negative
   least-squares (NNLS), which yields the contribution of an
   individual PAH molecule to the total fit. As a result, we obtain a
   breakdown of the model fit in terms of PAH charge and size. (3) The
   results are written to disk as a single FITS file and a PDF
   summarizing the model fit (one page per pixel, if a spectral cube
   is provided as input).

The general program methodology is encapsulated in the flowchart
presented in the figure above and is as follows:

(1) Read-in a file containing spectroscopic PAH observations of an
    astronomical object. This functionality is provided by the class
    ``observation``, which is implemented in ``observation.py``. It is the
    responsibility of the user to ensure all non-PAH emission
    components have been removed from the spectrum. The class uses a
    fall-through try-except chain to attempt to read the given
    filename using the facilities provided by ``astropy.io``. The
    spectroscopic data is stored as a class attribute as a
    ``spectrum`` object, which holds the data in terms of abscissa and
    ordinate values using ``numpy`` arrays. The units associated with
    the abscissa and ordinate values are, in the case of a FITS file,
    determined from the accompanying header, which itself is also
    stored as a class attribute. The spectral coordinate system is
    interpreted from FITS header keywords. The ``spectrum`` class is
    implemented in ``spectrum.py`` and provides functionality to convert
    between different coordinate representations. Below is example
    Python code demonstrating the use of the class. The file
    ``NGC7023-NW-BRIGHT.txt_pahs.txt`` in this demonstration can be
    found in the ``examples`` directory that is part of the
    pyPAHdb package. The output of the following code-block is shown in the flowchart.

.. code-block:: python

    import pypahdb as pah
    import matplotlib.pyplot as plt
    file = 'NGC7023-NW-BRIGHT.txt_pahs.txt'
    obs = pah.observation(file)
    s = obs.spectrum
    plt.plot(s.abscissa, s.ordinate[:,0,0])
    plt.ylabel(s.units['ordinate']['str']);
    plt.xlabel(s.units['abscissa']['str']);
    plt.show()

(2) Decompose the observed PAH emission into contributions from
    different PAH subclasses, here charge and size. This functionality
    is provided by the class ``decomposer``, which is implemented in
    ``decomposer.py``. The class takes as input a ``spectrum`` object, of
    which it creates a deep copy and calls its
    ``spectrum.convertunitsto`` method to convert the abscissa units
    to wavenumber. Subsequently, a pre-computed ``numpy`` matrix of
    highly oversampled PAH emission spectra stored as a ``pickle``
    is loaded from file. Utilizing ``numpy.interp``, each of
    the PAH emission spectra, represented by a single column in the
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

    result = pah.decomposer(obs.spectrum)
    s = result.spectrum
    plt.plot(s.abscissa, s.ordinate[:,0,0], 'x')
    plt.ylabel(s.units['ordinate']['str']);
    plt.xlabel(s.units['abscissa']['str']);
    plt.plot(s.abscissa, result.fit[:,0,0])
    plt.show()

(3) Produce output to file given a ``decomposer`` object. This
    functionality is provided by the class ``writer``, which is
    implemented in ``writer.py``, and serves to summarize the results from
    the ``decomposer`` class so that a user may assess the quality of
    the fit and store the PAH characteristics of their astronomical
    observations. The class uses ``astropy.fits`` to write the PAH
    characteristics to a FITS file and the ``matplotlib`` package to
    generate a PDF summarizing the results. The class will attempt to
    incorporate relevant information from any (FITS) header
    provided. Below is example code demonstrating the use of the
    class, which extends the previous code-block. The size breakdown
    part of the generated PDF output is shown in the flowchart.

.. code-block:: python

   pah.writer(result, header=obs.header)