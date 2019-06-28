[![Travis Status](https://img.shields.io/travis/PAHdb/pyPAHdb.svg)](https://travis-ci.org/PAHdb/pyPAHdb) [![Coverage Status]( https://codecov.io/gh/PAHdb/pyPAHdb/graph/badge.svg)](https://codecov.io/gh/PAHdb/pyPAHdb) [![Documentation](https://img.shields.io/badge/docs-available-brightgreen.svg)](https://pahdb.github.io/pyPAHdb/)


# pypahdb

pypahdb is a Python package to fit and decompose astronomical PAH
emission spectra into contributing PAH subclasses, i.e., charge and
size.

A paper describing pypahdb was presented at
[SciPy2018](https://scipy2018.scipy.org) and can be found using
[https://doi.org/10.25080/Majora-4af1f417-00f](https://doi.org/10.25080/Majora-4af1f417-00f).

## Requirements

This software requires:

``python3``
``specutils``
``scipy``
``astropy``

## Installation

pypahdb can be directly installed from the
[repository](https://github.com/PAHdb/pyPAHdb) using pip:

``pip install git+git://github.com/PAHdb/pyPAHdb.git``

## Examples

```python
# import the pypahdb package
import pypahdb
# read-in a fits-file containing an astronomical observation
observation = pypahdb.Observation('/path/to/observation.fits')
# run the decomposer on the spectral data in observation.fits
result = pypahdb.Decomposer(observation.spectrum)
# Save result to fits-file
result.save_fits("/path/to/myresult.fits", header=observation.header)
```
More examples can be found in the
[examples](examples)-directory.

## Documentation

Documentation can be found at
[www.astrochemistry.org/pahdb/pypahdb](https://www.astrochemistry.org/pahdb/pypahdb).

Briefly, the methodology of pyPAHdb can be summarized in the following flowchart, consisting of three steps:
(1) Astronomical spectroscopic data is loaded, whether loaded rom FITS or ASCII files. (2) An over-sampled pre-computed matrix of PAH spectra is loaded and interpolated onto the wavelength grid of the astronomical observations. Database-fitting is performed using non-negative least-squares (NNLS), which yields the contribution of an individual PAH molecule to the total fit. As a result, we obtain a breakdown of the model fit in terms of PAH charge and size. (3) The results are written to disk as a single FITS file and as a PDF summarizing the results (one page per pixel, if a spectral cube is provided as input)

![Flowchart](docs/source/figures/fig_flowchart.png)

## Background

The pypahdb Python package is being developed as part of the awarded
[James Webb Space Telescope](https://www.jwst.nasa.gov/) (*JWST*)
Early Release Science (ERS) program "Radiative Feedback from Massive
Stars as Traced by Multiband Imaging and Spectroscopic Mosaics"
([program website](http://jwst-ism.org/); ID: 1288). The program is
coordinated by an international "Core team" of 19 scientists and
supported by 119 "science collaborators". pypahdb is developed by the
[NASA Ames PAH IR Spectroscopic
Database](https://www.astrochemistry.org/pahdb/) team, asscociated
with the [Astrophysics & Astrochemistry
Laboratory](https://www.astrochemistry.org) at [NASA Ames Research
Center](https://www.nasa.gov/centers/ames).

The NASA Ames PAH IR Spectroscopic Database and pypahdb are being
supported through a directed Work Package at NASA Ames titled:
*"Laboratory Astrophysics – The NASA Ames PAH IR Spectroscopic
Database"*.

pypahdb uses a precomputed matrix of theoretically calculated PAH
emission spectra from version 3.00 of the library of computed
spectra. This matrix has been constructed from a collection of
*"astronomical"* PAHs, which meet the following critera and include
the fullerenes C<sub>60</sub> and C<sub>70</sub>:

       'magnesium=0 oxygen=0 iron=0 silicium=0 chx=0 ch2=0 c>20 hydrogen>0'

The PAH emission spectra have been calculated employing a PAH emission
model using the following parameters:

* A calculated vibrational temperature upon the absorption of a 7 eV
  photon
* A calculated integrated band intensity after following the entire
  emission cascade
* A redshift of 15 /cm to mimic *some* anharmonic effect
* A Gaussian emission profile with a FWHM of 15 /cm

Additional information can be found at the NASA Ames PAH IR
Spectroscopic Database website, which is located at
[www.astrochemistry.org/pahdb](https://www.astrochemistry.org/pahdb/pypahdb).

You are kindly asked to consider the following references for citation
when using pypahdb:

    * M.J. Shannon, and C. Boersma, "ORGANIC MOLECULES IN SPACE:
      INSIGHTS FROM THE NASA AMES MOLECULAR DATABASE IN THE ERA OF THE
      JAMES WEBB SPACE TELESCOPE" in Proceedings of the 17th Python in
      Science Conference, eds. F. Akici, D. Lippa, D. Niederhut, and
      M. Pacer, 99, 2018, https://doi.org/10.25080/Majora-4af1f417-00f

    * C.W. Bauschlicher, Jr., A. Ricca, C. Boersma, and
      L.J. Allamandola, "THE NASA AMES PAH IR SPECTROSCOPIC DATABASE:
      COMPUTATIONAL VERSION 3.00 WITH UPDATED CONTENT AND THE
      INTRODUCTION OF MULTIPLE SCALING FACTORS", The Astrophysical
      Journal Supplement Series, 234, 32, 2018
      https://doi.org/10.3847/1538-4365/aaa019

    * C. Boersma, C.W. Bauschlicher, Jr., A. Ricca, A.L. Mattioda,
      J. Cami, E. Peeters, F. Sanchez de Armas, G. Puerta Saborido,
      D.M. Hudgins, and L.J. Allamandola, "THE NASA AMES PAH IR
      SPECTROSCOPIC DATABASE VERSION 2.00: UPDATED CONTENT, WEBSITE AND
      ON/OFFLINE TOOLS", The Astrophysical Journal Supplement Series,
      https://doi.org/211, 8, 2014 10.1088/0067-0049/211/1/8

    * Mattioda, A. L., Hudgins, D. M., Boersma, C., Ricca, A.,
      Peeters, E., Cami, J., Sanchez de Armas, F., Puerta Saborido,
      G., Bauschlicher, C. W., J., and Allamandola, L. J. "THE NASA
      AMES PAH IR SPECTROSCOPIC DATABASE: THE LABORATORY SPECTRA", The
      Astrophysical Journal Supplement Series, XXX, 201X (in
      preparation)

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on the code
of conduct, and the process for submitting pull requests.

## Versioning

For the versions available, see the [tags on this
repository](https://github.com/pahdb/pypahdb/tags).

## Authors

* **Christiaan Boersma** - *Initial work* - [PAHdb](https://github.com/pahdb)
* **Matthew J. Shannon** - *Initial work* - [PAHdb](https://github.com/pahdb)

See also the list of [contributors](CONTRIBUTORS) who participated
in this project.

## License

This project is licensed under the BSD 3-Clause License - see the
[LICENSE](LICENSE) file for details

## Acknowledgments

* The NASA Ames PAH IR Spectroscopic Database Team -
  [www.astrochemistry.org/pahdb](https://www.astrochemistry.org/pahdb/theoretical/3.00/help/about)
* The Astrophysics & Astrochemistry Laboratory at NASA Ames Research
  Center - [www.astrochemistry.org](https://www.astrochemistry.org)
