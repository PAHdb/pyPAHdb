commit b2fd2b9578097e2c022676e26ac1146122c52f79
Author: Christiaan Boersma <Christiaan.Boersma@nasa.gov>
Date:   Wed Aug 15 21:40:10 2018 -0700

    Added coveralls badge and removed pipy badge.

commit 05d13ef66f1976cffa12e61d4f9ab6c6def8ef86
Author: Christiaan Boersma <Christiaan.Boersma@nasa.gov>
Date:   Wed Aug 15 21:07:01 2018 -0700

    Added _templates-directory to docs/source. Fixed README.md badges ensuring uppercase pyPAHdb. Added Authors.md. Regenerated CHANGELOG.md from git log; should find other way to do that ... Removed unnecessary builds from Makefile

commit 5c21ff334409877ecc34042a99730990a702df71
Author: Matt Shannon <matthew.j.shannon@gmail.com>
Date:   Wed Aug 15 20:37:34 2018 -0700

    Flake8 fixes (#6)
    
    * Applied flake8 fixes to writer.py
    
    * Applied flake8 fixes to spectrum.py
    
    * Applied flake8 fixes to observation.py
    
    * Applied flake8 fixes to decomposer.py
    
    * Applied flake8 fixes to setup.py
    
    * Applied flake8 fixes to example.py
    
    * Applied flake8 fixes to test_observation.py
    
    * Applied flake8 fixes to test_writer.py
    
    * Applied flake8 fixes to test_spectrum.py
    
    * Applied flake8 fixes to __init__.py
    
    * Changed multiline formatting of sphinx Description text, sounds like it could be causing the travis CI failure.
    
    * Updated decomposer.py's docstrings to Google style
    
    * Removing 'pypahdb' from index.rst to troubleshoot.
    
    * Adding :noindex: to pypahdb.observation in pypahdb.rst
    
    * More :noindex: in pypahdb.rst. Might need Doctr configured first?
    
    * Looks like it was the missing '_static' folder after all?
    
    * Figured it out; using .gitkeep to keep '_static' folder around; reverting pypahdb.rst
    
    * Revert "Figured it out; using .gitkeep to keep '_static' folder around; reverting pypahdb.rst"
    
    This reverts commit f6207b2a46649a45a763797f38a36c6a00a8944d.
    
    Renames tmp.txt as .gitkeep.

commit 3e601b284d3937e91f1c6cd2a8213c7d3a2f29ae
Author: Christiaan Boersma <Christiaan.Boersma@nasa.gov>
Date:   Wed Aug 15 12:31:38 2018 -0700

    Fixed typo in setup.py

commit 68f40afd1dbc09231e93af1f1a4dd30c27ed95de
Author: Christiaan Boersma <Christiaan.Boersma@nasa.gov>
Date:   Wed Aug 15 12:23:30 2018 -0700

    REL: v0.6.0

commit d6d1f6d77a075bb8eaf1cb7daebf19681f037171
Author: Christiaan Boersma <Christiaan.Boersma@nasa.gov>
Date:   Tue Aug 14 11:49:31 2018 -0700

    Put data-directory back.

commit 41087f3301a15796522e29f4172bcd0f189c2146
Author: Christiaan Boersma <Christiaan.Boersma@nasa.gov>
Date:   Tue Aug 14 11:44:54 2018 -0700

    Fixed typo in setup.pp

commit 448e3b6a1f370487d0a3c45273c63fae3c7f3561
Author: Christiaan Boersma <Christiaan.Boersma@nasa.gov>
Date:   Tue Aug 14 11:36:20 2018 -0700

    Moved away from LFS. Updated README.md to reflect changes.

commit e6f580493462027fc7c005d3de89daf2f65bf9a2
Author: Christiaan Boersma <Christiaan.Boersma@nasa.gov>
Date:   Mon Aug 13 13:32:25 2018 -0700

    Added SciPy2018 paper to README.md and fixed small spelling errors.

commit 4b95e226a149e8d405c3c269a3de4597a3e56346
Author: Christiaan Boersma <Christiaan.Boersma@nasa.gov>
Date:   Tue Jul 31 11:51:22 2018 -0700

    writer.py now uses the units provided by the spectrum-attribute. spectrum.py converunitsto now sets abscissa units. observation now falls through all errors and throws final exception on fail. precomputed matrix has been updated to contain spectra calculated using the cascade-model. NGC7023-NW-PAHs.txt now contains a continuum subtracted spectrum. README.md updated to reflect recent changes.

commit 4d17798318d00b22cf2ac6aad6be72beabc6b3f7
Author: Christiaan Boersma <Christiaan.Boersma@nasa.gov>
Date:   Sun Apr 8 19:41:40 2018 -0700

    Updated README.md install instructions and example

commit d973af53c96ceeca101781dc48d7b91e409c2f25
Author: Christiaan Boersma <Christiaan.Boersma@nasa.gov>
Date:   Wed Apr 4 09:12:37 2018 +0200

    Removed not needed astropy.io.fits import from example.py, check for non-zero elements in divide in decomposer.py and updated observation.py to use fits header keywords to retrieve ordinate values

commit 379db8933c346ace382ba86ebc5ac94778a1523b
Author: Christiaan Boersma <Christiaan.Boersma@nasa.gov>
Date:   Mon Apr 2 16:19:28 2018 +0200

    Updated README.md to reflect Git LFS

commit 935b95ea74b00701e08b42ca67845a5c130dac79
Author: Christiaan Boersma <Christiaan.Boersma@nasa.gov>
Date:   Mon Apr 2 14:05:36 2018 +0200

    Readded precomputed matrix for LFS storage

commit 0053dde7c8b1b3b39cf0153f228247fb3e18c0d4
Author: Christiaan Boersma <Christiaan.Boersma@nasa.gov>
Date:   Mon Apr 2 14:01:48 2018 +0200

    Removed precomputed matrix for updated LFS storage

commit 76de7bb7f0ff90d5332a75188fc27adb6a60e79b
Author: Christiaan Boersma <Christiaan.Boersma@nasa.gov>
Date:   Mon Apr 2 13:48:05 2018 +0200

    Moved LSF Storage to astrochemistry.org

commit ebe6e5eb488658f927f88f815c76964db814b0de
Author: Christiaan Boersma <Christiaan.Boersma@nasa.gov>
Date:   Fri Mar 30 12:13:23 2018 -0700

    Fixed typo in decomposer.py preventing correct multiprocessing for size breakdown.

commit 5a5b7ea1daa212946df44f9cbf47e60cf156201c
Author: Christiaan Boersma <Christiaan.Boersma@nasa.gov>
Date:   Fri Mar 30 10:03:26 2018 -0700

    Precomputed matrix uses now PAH spectra from version 3.00 of the library of computed spectra from PAHdb.

commit 4e3f522ace6e6d6c3644e418f305f85fac0a155d
Author: Christiaan Boersma <Christiaan.Boersma@nasa.gov>
Date:   Fri Mar 30 09:55:52 2018 -0700

    Track precomputed matrix (.pkl) using Git LFS

commit 05caf24e4354dce6d01d6b0deb0883fbc9b81843
Author: Christiaan Boersma <Christiaan.Boersma@nasa.gov>
Date:   Thu Mar 29 12:51:52 2018 -0700

    Some aestetic changes to the PDF output.

commit 1573135d1819909f4117d6e747cbdbcb1bb30eb2
Merge: 21dc812 0246d22
Author: NASA Ames PAH IR Spectroscopic Database <30665870+PAHdb@users.noreply.github.com>
Date:   Thu Mar 29 11:19:31 2018 -0700

    Merge pull request #4 from mattjshannon/master
    
    Updated figure plotting in writer.py, and a few print statements

commit 0246d22dd3d8a0fa52147155b315c7d8f47c57b0
Author: Matt Shannon <matthew.j.shannon@gmail.com>
Date:   Thu Mar 29 11:12:50 2018 -0700

    Added title to figure: cation fraction, large fraction, norm

commit 3c1b6e4c176abfe2c3fa673faed74e06def45630
Author: Matt Shannon <matthew.j.shannon@gmail.com>
Date:   Thu Mar 29 11:01:25 2018 -0700

    Updated figure plotting in writer.py, adjusted print statements in observation.py and decomposer.py

commit 21dc81220453cdc61b3b9e15c271181667d98918
Author: Christiaan Boersma <Christiaan.Boersma@nasa.gov>
Date:   Wed Mar 28 16:15:46 2018 -0700

    Added more multiprocessing support to decomposer.py. Cleaned-up examples and added README.md. Minor overall fixes.

commit bd0289b50658dae7a150d37560e1b251be84b500
Author: Christiaan Boersma <Christiaan.Boersma@nasa.gov>
Date:   Tue Mar 27 22:01:16 2018 -0700

    Refactored observation.py to handle both simply fits- and ASCII-files. Started streamlining output in writer.py and generating the necessary data in decomposer.py.

commit f74ddd53154a2a7c472c7a20f7537d53685890c2
Author: Christiaan Boersma <Christiaan.Boersma@nasa.gov>
Date:   Tue Mar 20 11:52:13 2018 -0700

    Added framework for reading in Spitzer-IRS data cubes and minor cosmetic fixes.

commit 934de7a0e3e4b9edc296ba7042d4d098701d14d5
Merge: 300dade 5495357
Author: NASA Ames PAH IR Spectroscopic Database <30665870+PAHdb@users.noreply.github.com>
Date:   Tue Mar 13 16:34:43 2018 -0700

    Merge pull request #1 from mattjshannon/master
    
    Added Python3 functionality to codebase, updated documentation.

commit 549535796fb5ce4ea82ed8e30da2b68f112bc6bf
Author: Matt Shannon <matthew.j.shannon@gmail.com>
Date:   Tue Mar 13 16:25:26 2018 -0700

    Updated makefiles to accept either version of Python (2 or 3).

commit 2bf7189ae126c7bfcca8dc9f2e3a8e7fc81bb122
Author: Matt Shannon <matthew.j.shannon@gmail.com>
Date:   Tue Mar 13 16:15:14 2018 -0700

    Updated .py files to accept Python 3 (as well as 2).

commit a841f4db1ffd441ace82d414d209e05e1339881d
Author: Matt Shannon <matthew.j.shannon@gmail.com>
Date:   Tue Mar 13 15:40:57 2018 -0700

    Added VERSION to setup.py list of required files.

commit d30c67bb51a7ab51d8382303e89944a3967a4ef9
Author: Matt Shannon <matthew.j.shannon@gmail.com>
Date:   Tue Mar 13 15:35:39 2018 -0700

    Updated readme.md
    
    Removed extra installation options (unnecessary!).

commit 9bbdbc2397babda02bd5b94a80ef5dc85da2c754
Merge: 300dade 718e788
Author: Matt Shannon <matthew.j.shannon@gmail.com>
Date:   Tue Mar 13 15:29:22 2018 -0700

    Merge pull request #1 from mattjshannon/update-documentation
    
    Updated readme

commit 718e7880b087c94c2a04539a8c2bf62c950f59bf
Author: Matt Shannon <matthew.j.shannon@gmail.com>
Date:   Tue Mar 13 15:05:43 2018 -0700

    Updated readme
    
    Added alternative installation method, set headers for examples, unit tests, documentaiton; and created requirements category (needs version numbers still).

commit 300dade8b2847d035fe665421dc34f1009114615
Author: Christiaan Boersma <Christiaan.Boersma@nasa.gov>
Date:   Wed Mar 7 17:37:57 2018 -0800

    Fixed typos, inconsistencies and added documentation

commit e9b5cc0f245bf939ea5bede43d81210c01f2ff6c
Author: Christiaan Boersma <Christiaan.Boersma@nasa.gov>
Date:   Wed Mar 7 17:29:33 2018 -0800

    This reverts commit 9555fb1961d5e31763e82a1b3fe68ef0c743c384.

commit eab997a79c0a360cdb0ebac8e746a3e565ecc835
Author: Christiaan Boersma <Christiaan.Boersma@nasa.gov>
Date:   Wed Mar 7 17:23:24 2018 -0800

    Fixed typos, inconsistencies and added documentation

commit bc09b8f2819eff0c2f2c3e78fbd5a20ea513036b
Author: Christiaan Boersma <Christiaan.Boersma@nasa.gov>
Date:   Fri Mar 2 12:40:39 2018 -0800

    Initial commit

commit c127492041a6298111e8eb42e75bc59607ad32b6
Author: NASA Ames PAH IR Spectroscopic Database <30665870+PAHdb@users.noreply.github.com>
Date:   Wed Aug 2 11:07:41 2017 -0700

    Initial commit
