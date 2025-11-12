[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17428405.svg)](https://doi.org/10.5281/zenodo.17428405)
![Workflow
Status](https://github.com/pahdb/pyPAHdb/actions/workflows/ci.yml/badge.svg)
[![Coverage
Status](https://codecov.io/gh/PAHdb/pyPAHdb/graph/badge.svg)](https://codecov.io/gh/PAHdb/pyPAHdb)
[![Documentation](https://img.shields.io/badge/docs-available-brightgreen.svg)](https://pahdb.github.io/pyPAHdb/)

# pyPAHdb

pyPAHdb is a Python package to fit and decompose isolated astronomical PAH
emission spectra into contributing PAH subclasses, i.e., charge and size.

A paper describing pyPAHdb was presented at
[SciPy2018](https://scipy2018.scipy.org) and can be found using its DOI:
[https://doi.org/10.25080/Majora-4af1f417-00f](https://doi.org/10.25080/Majora-4af1f417-00f).

## Features

pyPAHdb is the light version of a full suite of [Python software
tools](https://github.com/PAHdb/AmesPAHdbPythonSuite), which has a counterpart
written in [IDL](https://github.com/PAHdb/AmesPAHdbIDLSuite). A feature
comparison is presented in the table below.

| Feature                  | pyPAHdb | IDL/Python Suite |
| ------------------------ | ------- | ---------------- |
| Included PAHs            | Fixed   | User defined     |
| Excitation Energy        | Fixed   | User defined     |
| Emission Profile         | Fixed   | Selectable       |
| FWHM [1]                 | Fixed   | User defined     |
| Band Redshift            | Fixed   | User defined     |
| Emission Model           | Fixed   | Selectable       |
| NNLS [2]                 | ✓       | ✓                |
| Class Breakdown          | ✓       | ✓                |
| Parallelization          | ✓       | ✓                |
| Handle Uncertainties [3] |         | ✓                |

[1] FWHM: full-width at half-maximum for an emission profile.\
[2] NNLS: non-negative least squares.\
[3] In this context, refers to handling observational spectroscopic
uncertainties.

## Requirements

This software requires:

`python3` `specutils` `scipy` `astropy` `matplotlib`

## Installation

pyPAHdb can be directly installed from the
[repository](https://github.com/PAHdb/pyPAHdb) using pip:

`pip install git+https://github.com/PAHdb/pyPAHdb.git`

Note that upon first-run a precomputed matrix will need to be downloaded from
PAHdb's server. A menu with different configurations will be presented from
which a selection must be made. The `version`-keyword to the
`Decomposer`-constructor can be used to pick a specific version directly, e.g.,
"3.20". If the version is not locally available, it will be automatically
downloaded. To present the picker menu again, the `version`-keyword can be set
to "picker". Upon subsequent runs and the `version`-keyword is not set, the
latest locally available version is used.

## Supported data formats

pyPAHdb supports reading IPAC tables, _Spitzer_ FITS files and _JWST_ FITS files.

## Examples

```python
from pypahdb.decomposer import Decomposer
from pypahdb.observation import Observation

# Make sure to run from __main__ context to satisfy multiprocessing
if __name__ == '__main__':
    # read-in a file containing an astronomical observation
    observation = Observation('/path/to/observation.ext')
    # run the decomposer on the spectral data in observation.fits
    result = Decomposer(observation.spectrum)
    # display results
    result.plot_fit().show()
    # Save result to fits-file
    result.save_fits('/path/to/myresult.fits', header=observation.header)
    # Save a PDF summary of the fit results
    result.save_pdf('/path/to/figure.pdf')
```

More examples can be found in the [examples](examples)-directory.

## Documentation

Documentation can be found at
[https://pahdb.github.io/pyPAHdb/](https://pahdb.github.io/pyPAHdb/).

Briefly, the methodology of pyPAHdb can be summarized in the following
flowchart, consisting of three steps: (1) Astronomical spectroscopic data is
loaded, whether loaded from FITS or ASCII files. (2) An over-sampled
pre-computed matrix of PAH spectra is loaded and interpolated onto the
wavelength grid of the astronomical observations. Database-fitting is performed
using non-negative least-squares (NNLS), which yields the contribution of an
individual PAH molecule to the total fit. As a result, we obtain a breakdown of
the model fit in terms of PAH charge and size. (3) The results are written to
disk as a single FITS file and as a PDF summarizing the results (one page per
pixel, if a spectral cube is provided as input)

![Flowchart](docs/source/figures/fig_flowchart.png)

## Background

The pyPAHdb Python package is being developed as part of the awarded [James Webb
Space Telescope](https://www.jwst.nasa.gov/) (_JWST_) Early Release Science
(ERS) program "_Radiative Feedback from Massive Stars as Traced by Multiband
Imaging and Spectroscopic Mosaics_" ([program website](http://pdrs4all.org/); ID:
1288). The program is coordinated by an international "Core team" of 19
scientists and supported by 119 "science collaborators". pyPAHdb is developed by
the [NASA Ames PAH IR Spectroscopic
Database](https://www.astrochemistry.org/pahdb/) team, associated with the
[Astrophysics & Astrochemistry Laboratory](https://www.astrochemistry.org) at
[NASA Ames Research Center](https://www.nasa.gov/centers/ames).

From FY2025 onward the NASA Ames PAH IR Spectroscopic Database is being supported through the Laboratory Astrophysics Round 3 directed Work Package at NASA Ames.

From FY2023-2025 the NASA Ames PAH IR Spectroscopic Database was supported through the Laboratory Astrophysics Round 2 directed Work Package at NASA Ames.

From FY2019-2022 the NASA Ames PAH IR Spectroscopic Database was supported through a directed Work Package at NASA Ames titled: “_Laboratory Astrophysics & The NASA Ames PAH IR Spectroscopic Database_”.

pyPAHdb uses a precomputed matrix of theoretically calculated PAH emission
spectra. This matrix has been constructed from a collection of _"astronomical"_
PAHs, which meet the following criteria and include the fullerenes
C<sub>60</sub> and C<sub>70</sub>:

```IDL
magnesium=0 oxygen=0 iron=0 silicium=0 chx=0 ch2=0 c>20 hydrogen>0
```

The PAH emission spectra have been calculated employing a PAH emission model
using the following general parameters:

- A calculated vibrational temperature upon the absorption of a 7 eV photon
- A calculated integrated band intensity after following the entire emission
  cascade
- A Gaussian emission profile with a FWHM of 15 cm<sup>-1</sup>

Depending on the configuration of the selected version of the precomputed
matrix, there can be variation in these parameters.

Additional information can be found at the NASA Ames PAH IR Spectroscopic
Database website, which is located at
[www.astrochemistry.org/pahdb](https://www.astrochemistry.org/pahdb/pyPAHdb).

You are kindly asked to consider the following references for citation when
using pyPAHdb:

- M.J. Shannon, and C. Boersma, "ORGANIC MOLECULES IN SPACE: INSIGHTS FROM THE
  NASA AMES MOLECULAR DATABASE IN THE ERA OF THE JAMES WEBB SPACE TELESCOPE" in
  Proceedings of the 17th Python in Science Conference, eds. F. Akici, D. Lippa,
  D. Niederhut, and M. Pacer, 99, 2018
  [https://doi.org/10.25080/Majora-4af1f417-00f](https://doi.org/10.25080/Majora-4af1f417-00f)

- Ricca, A., Boersma, C., Maragkoudakis, A., Roser, J.E., Shannon, M.J.
  Allamandola, L.J., Bauschlicher Jr., C.W., "THE NASA AMES PAH IR
  SPECTROSCOPIC DATABASE: COMPUTATIONAL VERSION 4.00, SOFTWARE TOOLS, WEBSITE,
  AND DOCUMENTATION", The Astrophysical Journal Supplement Series, in press,
  2025
  [https://doi.org/10.3847/1538-4365/ae1c38](https://doi.org/10.3847/1538-4365/ae1c38)

- C.W. Bauschlicher, Jr., A. Ricca, C. Boersma, and L.J. Allamandola, "THE NASA
  AMES PAH IR SPECTROSCOPIC DATABASE: COMPUTATIONAL VERSION 3.00 WITH UPDATED
  CONTENT AND THE INTRODUCTION OF MULTIPLE SCALING FACTORS", The Astrophysical
  Journal Supplement Series, 234, 32, 2018
  [https://doi.org/10.3847/1538-4365/aaa019](https://doi.org/10.3847/1538-4365/aaa019)

- C. Boersma, C.W. Bauschlicher, Jr., A. Ricca, A.L. Mattioda, J. Cami, E.
  Peeters, F. Sanchez de Armas, G. Puerta Saborido, D.M. Hudgins, and L.J.
  Allamandola, "THE NASA AMES PAH IR SPECTROSCOPIC DATABASE VERSION 2.00:
  UPDATED CONTENT, WEBSITE AND ON/OFFLINE TOOLS", The Astrophysical Journal
  Supplement Series, 211, 8, 2014
  [https://doi.org/10.1088/0067-0049/211/1/8](https://doi.org/10.1088/0067-0049/211/1/8)

- C.W. Bauschlicher, Jr., C. Boersma, A. Ricca, A.L. Mattioda, J. Cami, E.
  Peeters, F. S&#225;nchez de Armas, G. Puerta Saborido, D.M. Hudgins, and L.J.
  Allamandola, "THE NASA AMES PAH IR SPECTROSCOPIC DATABASE: THE COMPUTED
  SPECTRA", The Astrophysical Journal Supplement Series, 189, 341, 2010
  [https://doi.org/10.1088/0067-0049/189/2/341](https://doi.org/10.1088/0067-0049/189/2/341)

- Mattioda, A. L., Hudgins, D. M., Boersma, C., Ricca, A., Peeters, E., Cami,
  J., Sanchez de Armas, F., Puerta Saborido, G., Bauschlicher, C. W., J., and
  Allamandola, L. J. "THE NASA AMES PAH IR SPECTROSCOPIC DATABASE: THE
  LABORATORY SPECTRA", The Astrophysical Journal Supplement Series, 251, 22,
  2020
  [https://doi.org/10.3847/1538-4365/abc2c8](https://doi.org/10.3847/1538-4365/abc2c8)

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on the code of
conduct, and the process for submitting pull requests.

## Versioning

For the versions available, see the [tags on this
repository](https://github.com/pahdb/pyPAHdb/tags).

## Authors

- **Christiaan Boersma** - _Initial work_ - [PAHdb](https://github.com/pahdb)
- **Matthew J. Shannon** - _Initial work_ - [PAHdb](https://github.com/pahdb)
- **Alexandros Maragkoudakis** - [PAHdb](https://github.com/pahdb)

See also the list of [contributors](AUTHORS.md) who participated in this
project.

## License

This project is licensed under the BSD 3-Clause License - see the
[LICENSE](LICENSE) file for details

## Acknowledgments

- The NASA Ames PAH IR Spectroscopic Database Team -
  [www.astrochemistry.org/pahdb](https://www.astrochemistry.org/pahdb/theoretical/3.00/help/about)
- The Astrophysics & Astrochemistry Laboratory at NASA Ames Research Center -
  [www.astrochemistry.org](https://www.astrochemistry.org)
