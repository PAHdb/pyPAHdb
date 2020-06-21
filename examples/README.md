# Examples

This is the examples directory accompanying the pypahdb Python package
and can be used to verify correct installation of the package and as a
template for using pypahdb in your own code.

The files can be directly run from the terminal, e.g.,:

```./example_tbl.py```

Or via:

```python example_tbl.py```

There are two example programs:

1. `example_tbl.py` analyzes an IPAC-tabulated Spitzer-IRS spectrum
from a position in the reflection nebula NGC 7023.
2. `example_fits.py` analyzes a FITS file containing a Spitzer-IRS
spectral data cube covering most of the northwest PDR in the
reflection nebula NGC 7023.

Upon successfully running the example programs, a FITS-file will be
created holding the PAH ionized fraction, PAH large fraction and the
norm. A PDF summarizing the results is also created when running the
first program.
