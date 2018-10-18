# Examples

This is the examples directory accompanying the pypahdb Python package
and can be used to verify correct installation of the package and as a
templete for using pypahdb in your own code.

The files can be directly run from the terminal, e.g.:

```./example_txt.py```

Or via:

```python example_txt.py```

There are two examples currently:
- `example_txt.py` analyzes a ASCII-tabulated spectrum from a single
position in the NGC 7023 data cube (stored within the pypahdb/data folder).
- `example_fits.py` analyzes a FITS file containing a Spitzer-IRS data cube
of the northwest PDR in NGC 7023.

Upon successfully running an example script, two files should have
appeared: one is a PDF-file summarizing the results, and the other is a
FITS-file with the ionized fraction, large fraction and norm.