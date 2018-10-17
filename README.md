[![Travis Status](https://img.shields.io/travis/PAHdb/pyPAHdb.svg)](https://travis-ci.org/PAHdb/pyPAHdb) [![Coverage Status]( https://codecov.io/gh/PAHdb/pyPAHdb/graph/badge.svg)](https://codecov.io/gh/PAHdb/pyPAHdb) [![Documentation](https://img.shields.io/badge/docs-available-brightgreen.svg)](https://pahdb.github.io/pyPAHdb/)


# pypahdb

pypahdb is a Python package to fit and decompose astronomical PAH
emission spectra into contributing PAH subclasses.

A paper describing pypahdb was presented at
[SciPy2018](https://scipy2018.scipy.org) and can be found using the
doi
[10.25080/Majora-4af1f417-00f](http://doi.org/10.25080/Majora-4af1f417-00f).

## Requirements

This software requires:

``python``
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
# read-in observation.fits
observation = pypahdb.observation('observation.fits')
# run the decomposer on the spectrum in observation.fits
result = pypahdb.decomposer(observation.spectrum)
# write decomposer results to file
pypahdb.writer(result)
```
More examples can be found in the
[examples](examples)-directory.

## Documentation

Documentation can be found at
[www.astrochemistry.org/pahdb/pypahdb](http://www.astrochemistry.org/pahdb/pypahdb).

## Background

The pypahdb package is being developed as part of the awarded [James
Webb Space Telescope](https://www.jwst.nasa.gov/) (*JWST*) Early
Release Science (ERS) program "Radiative Feedback from Massive Stars
as Traced by Multiband Imaging and Spectroscopic Mosaics" ([program
website](http://jwst-ism.org/); ID: 1288). The program is coordinated
by an international "Core team" of 19 scientists and supported by 119
"science collaborators". pypahdb is developed by the [NASA Ames PAH IR
Spectroscopic Database](http://www.astrochemistry.org/pahdb/) team,
asscociated with the [Astrophysics & Astrochemistry
Laboratory](http://www.astrochemistry.org) at [NASA Ames Research
Center](https://www.nasa.gov/centers/ames).

pypahdb uses a precomputed matrix of theoretically calculated PAH
emission spectra from version 3.00 of the library of computed
spectra. This matrix has been constructed from a collection of
"astronomical" PAHs, which meet the following critera and include the
fullerenes C<sub>60</sub> and C<sub>70</sub>:

       'magnesium=0 oxygen=0 iron=0 silicium=0 chx=0 ch2=0 c>20 hydrogen>0'

The PAH emission spectra have been calculated with the following
parameters:

* A calculated vibrational temperature upon the absorption of a 7 eV
  photon
* A calculated integrated band intensity after following the entire emission cascade
* A redshift of 15 /cm to mimic some anharmonic effect
* A Gaussian emission profile with a FWHM of 15 /cm

Additional information can be found at the NASA Ames PAH IR
Spectroscopic Database website, which is located at
[www.astrochemistry.org/pahdb](http://www.astrochemistry.org/pahdb/pypahdb).

You are kindly asked to cite the following paper when using pypahdb:

	* Shannon, M.J., Boersma, C., "Organic Molecules in Space: Insights from
	  the NASA Ames Molecular Database in the era of the James Webb Space
      Telescope", 2018, SciPy, 99 doi:10.25080/majora-4af1f417-00f

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md)
for details on the code of conduct, and the process for submitting
pull requests.

## Versioning

For the versions available, see the
[tags on this repository](https://github.com/pahdb/pypahdb/tags).

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
  [www.astrochemistry.org/pahdb](http://www.astrochemistry.org/pahdb/theoretical/3.00/help/about)
* The Astrophysics & Astrochemistry Laboratory at NASA Ames Research
  Center - [www.astrochemistry.org](http://www.astrochemistry.org)
