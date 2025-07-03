.. sectnum::
   :start: 1

Background
============

Purpose
---------

PyPAHdb is used to characterize emission from one of the most
prevalent types of organic molecules in space, namely polycyclic
aromatic hydrocarbons (PAHs). It leverages the detailed studies of
organic molecules done at the NASA Ames Research Center. PyPAHdb is a
streamlined Python version of the NASA Ames PAH IR Spectroscopic
Database's (PAHdb; `www.astrochemistry.org/pahdb/
<https://www.astrochemistry.org/pahdb/>`_) suite of IDL and Python tools.
PAHdb has been extensively used to analyze and interpret the PAH signature
from a plethora of emission sources, ranging from solar-system objects to
entire galaxies. PyPAHdb decomposes astronomical PAH emission spectra
into contributing PAH sub-classes in terms of charge and size using a
database-fitting technique. The inputs for the fit are spectra
constructed using the spectroscopic libraries of PAHdb and take into
account the detailed photo-physics of the PAH excitation/emission
process.

Features
------------------

The purpose of pyPAHdb is to derive astronomical parameters directly
from *JWST* observations, but the tool is not limited to *JWST*
observations alone. PyPAHdb is the light version of a full suite of
Python software tools\ [#]_ that is an analog of the off-line IDL tools\ [#]_.
A feature comparison is presented in the table below. PyPAHdb will enable PAH
experts and non-experts alike to analyze and interpret astronomical PAH
emission spectra.

.. raw:: latex

   \setlength{\tablewidth}{0.7\textwidth}


.. table:: Feature comparison between pyPAHdb and the full suites of
           IDL/Python tools. Notes: NNLS=non-negative least-squares;
           NNLC=non-negative least-chi-squared; FWHM= full-width at
           half-maximum of a line profile; Uncertainties=handling
           observational spectroscopic uncertainties.

   +---------------------+----------+------------------+
   |                     | PyPAHdb  | IDL/Python Tools |
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
   | NNLC                |          | ✓                |
   +---------------------+----------+------------------+
   | Class breakdown     | ✓        | ✓                |
   +---------------------+----------+------------------+
   | Parallelization     | ✓        | ✓                |
   +---------------------+----------+------------------+
   | Uncertainties       |          | ✓                |
   +---------------------+----------+------------------+

.. PyPAHdb analyzes spectroscopic observations (including spectral maps)
.. and characterizes the PAH emission using a database-fitting approach,
.. providing the PAH ionization and small/large fractions.


Academic references
-------------------

You are kindly asked to consider the following references for citation
when using pyPAHdb:

  Shannon, M.J., Boersma, C., "ORGANIC MOLECULES IN SPACE: INSIGHTS
  FROM THE NASA AMES MOLECULAR DATABASE IN THE ERA OF THE JAMES WEBB
  SPACE TELESCOPE", 2018, *SciPy*, 99
  `https://doi.org/10.25080/majora-4af1f417-00f
  <https://dx.doi.org/10.25080/majora-4af1f417-00f>`__

  C.W. Bauschlicher, Jr., A. Ricca, C. Boersma, L.J. Allamandola, "THE
  NASA AMES PAH IR SPECTROSCOPIC DATABASE: COMPUTATIONAL VERSION 3.00
  WITH UPDATED CONTENT AND THE INTRODUCTION OF MULTIPLE SCALING
  FACTORS", *The Astrophysical Journal Supplement Series*, **234**,
  32, 2018, `https://doi.org/10.3847/1538-4365/aaa019
  <https://dx.doi.org/10.3847/1538-4365/aaa019>`__

  C. Boersma, C.W. Bauschlicher, Jr., A. Ricca,
  A.L. Mattioda, J. Cami, E. Peeters, F. S&#225;nchez de
  Armas, G. Puerta Saborido, D.M. Hudgins, and L.J. Allamandola, "THE
  NASA AMES PAH IR SPECTROSCOPIC DATABASE VERSION 2.00: UPDATED
  CONTENT, WEBSITE AND ON/OFFLINE TOOLS", *The Astrophysical Journal
  Supplement Series*, **211**, 8, 2014,
  `https://doi.org/10.1088/0067-0049/211/1/8
  <https://dx.doi.org/10.1088/0067-0049/211/1/8>`__

  C.W. Bauschlicher, Jr., C. Boersma, A. Ricca,
  A.L. Mattioda, J. Cami, E. Peeters, F. S&#225;nchez de
  Armas, G. Puerta Saborido, D.M. Hudgins, and L.J. Allamandola, "THE
  NASA AMES PAH IR SPECTROSCOPIC DATABASE: THE COMPUTED SPECTRA", *The
  Astrophysical Journal Supplement Series*, **189**, 341, 2010,
  `https://doi.org/10.1088/0067-0049/189/2/341
  <http://dx.doi.org/10.1088/0067-0049/189/2/341>`__

  Mattioda, A. L., Hudgins, D. M., Boersma, C., Ricca, A., Peeters,
  E., Cami, J., S&#225;nchez de Armas, F., Puerta Saborido, G.,
  Bauschlicher, C. W., J., and Allamandola, L. J. "THE NASA AMES PAH
  IR SPECTROSCOPIC DATABASE: THE LABORATORY SPECTRA", *The
  Astrophysical Journal Supplement Series*, 251, 22, 2020,
  `https://doi.org/10.3847/1538-4365/abc2c8
  <http://dx.doi.org/10.3847/1538-4365/abc2c8>`__


---------

.. [#] *AmesPAHdbPythonSuite*: `github.com/PAHdb/AmesPAHdbPythonSuite
       <https://github.com/PAHdb/AmesPAHdbPythonSuite>`_

.. [#] *AmesPAHdbIDLSuite*: `github.com/PAHdb/AmesPAHdbIDLSuite
       <https://github.com/PAHdb/AmesPAHdbIDLSuite>`_
