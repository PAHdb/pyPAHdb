[33m5c21ff3[m[33m ([m[1;36mHEAD -> [m[1;32mmaster[m[33m, [m[1;31morigin/master[m[33m, [m[1;31morigin/HEAD[m[33m)[m Flake8 fixes (#6)
[33m3e601b2[m Fixed typo in setup.py
[33m68f40af[m[33m ([m[1;33mtag: v0.6.0[m[33m)[m REL: v0.6.0
[33md6d1f6d[m Put data-directory back.
[33m41087f3[m Fixed typo in setup.pp
[33m448e3b6[m Moved away from LFS. Updated README.md to reflect changes.
[33me6f5804[m Added SciPy2018 paper to README.md and fixed small spelling errors.
[33m4b95e22[m writer.py now uses the units provided by the spectrum-attribute. spectrum.py converunitsto now sets abscissa units. observation now falls through all errors and throws final exception on fail. precomputed matrix has been updated to contain spectra calculated using the cascade-model. NGC7023-NW-PAHs.txt now contains a continuum subtracted spectrum. README.md updated to reflect recent changes.
[33m4d17798[m Updated README.md install instructions and example
[33md973af5[m Removed not needed astropy.io.fits import from example.py, check for non-zero elements in divide in decomposer.py and updated observation.py to use fits header keywords to retrieve ordinate values
[33m379db89[m Updated README.md to reflect Git LFS
[33m935b95e[m Readded precomputed matrix for LFS storage
[33m0053dde[m Removed precomputed matrix for updated LFS storage
[33m76de7bb[m Moved LSF Storage to astrochemistry.org
[33mebe6e5e[m Fixed typo in decomposer.py preventing correct multiprocessing for size breakdown.
[33m5a5b7ea[m Precomputed matrix uses now PAH spectra from version 3.00 of the library of computed spectra from PAHdb.
[33m4e3f522[m Track precomputed matrix (.pkl) using Git LFS
[33m05caf24[m Some aestetic changes to the PDF output.
[33m1573135[m Merge pull request #4 from mattjshannon/master
[33m0246d22[m Added title to figure: cation fraction, large fraction, norm
[33m3c1b6e4[m Updated figure plotting in writer.py, adjusted print statements in observation.py and decomposer.py
[33m21dc812[m Added more multiprocessing support to decomposer.py. Cleaned-up examples and added README.md. Minor overall fixes.
[33mbd0289b[m Refactored observation.py to handle both simply fits- and ASCII-files. Started streamlining output in writer.py and generating the necessary data in decomposer.py.
[33mf74ddd5[m Added framework for reading in Spitzer-IRS data cubes and minor cosmetic fixes.
[33m934de7a[m Merge pull request #1 from mattjshannon/master
[33m5495357[m Updated makefiles to accept either version of Python (2 or 3).
[33m2bf7189[m Updated .py files to accept Python 3 (as well as 2).
[33ma841f4d[m Added VERSION to setup.py list of required files.
[33md30c67b[m Updated readme.md
[33m9bbdbc2[m Merge pull request #1 from mattjshannon/update-documentation
[33m718e788[m Updated readme
[33m300dade[m Fixed typos, inconsistencies and added documentation
[33me9b5cc0[m This reverts commit 9555fb1961d5e31763e82a1b3fe68ef0c743c384.
[33meab997a[m Fixed typos, inconsistencies and added documentation
[33mbc09b8f[m Initial commit
[33mc127492[m Initial commit
