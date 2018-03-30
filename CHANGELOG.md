[33mcommit e08f5b8ba954727900c1ffbcfc8068966c41eca3[m[33m ([m[1;36mHEAD -> [m[1;32mmaster[m[33m, [m[1;31morigin/master[m[33m, [m[1;31morigin/HEAD[m[33m)[m
Author: Christiaan Boersma <Christiaan.Boersma@nasa.gov>
Date:   Fri Mar 30 10:03:26 2018 -0700

    Precomputed matrix uses now PAH spectra from version 3.00 of the library of computed spectra from PAHdb.

[33mcommit 37444003fca35d632af8d1430076590d38faf174[m
Author: Christiaan Boersma <Christiaan.Boersma@nasa.gov>
Date:   Fri Mar 30 09:55:52 2018 -0700

    Track precomputed matrix (.pkl) using Git LFS

[33mcommit ca10bed323cb934b3e49449cc8212372983eab46[m
Author: Christiaan Boersma <Christiaan.Boersma@nasa.gov>
Date:   Thu Mar 29 12:51:52 2018 -0700

    Some aestetic changes to the PDF output.

[33mcommit edce61c0e430a21ad968aec7c2766a48503dbc9b[m
Merge: 036ad3b 1a57010
Author: NASA Ames PAH IR Spectroscopic Database <30665870+PAHdb@users.noreply.github.com>
Date:   Thu Mar 29 11:19:31 2018 -0700

    Merge pull request #4 from mattjshannon/master
    
    Updated figure plotting in writer.py, and a few print statements

[33mcommit 1a5701053204dd8e776cdd14aaf1644a6c2bdd05[m
Author: Matt Shannon <matthew.j.shannon@gmail.com>
Date:   Thu Mar 29 11:12:50 2018 -0700

    Added title to figure: cation fraction, large fraction, norm

[33mcommit 3a7e59526ded79c4e8a011fb6f088c8f68550360[m
Author: Matt Shannon <matthew.j.shannon@gmail.com>
Date:   Thu Mar 29 11:01:25 2018 -0700

    Updated figure plotting in writer.py, adjusted print statements in observation.py and decomposer.py

[33mcommit 036ad3b3be49922b5e560efba4d9feb8c09917e5[m
Author: Christiaan Boersma <Christiaan.Boersma@nasa.gov>
Date:   Wed Mar 28 16:15:46 2018 -0700

    Added more multiprocessing support to decomposer.py. Cleaned-up examples and added README.md. Minor overall fixes.

[33mcommit 9d543c422041dda1dc2dd2ff820991d74a5519b0[m
Author: Christiaan Boersma <Christiaan.Boersma@nasa.gov>
Date:   Tue Mar 27 22:01:16 2018 -0700

    Refactored observation.py to handle both simply fits- and ASCII-files. Started streamlining output in writer.py and generating the necessary data in decomposer.py.

[33mcommit 810150b918accf0a0d6d7af6dc43fc4def15cfbc[m
Author: Christiaan Boersma <Christiaan.Boersma@nasa.gov>
Date:   Tue Mar 20 11:52:13 2018 -0700

    Added framework for reading in Spitzer-IRS data cubes and minor cosmetic fixes.

[33mcommit 0371988fed7b79661d929fbb83430e3072d99c61[m
Merge: 0b700df ae017ac
Author: NASA Ames PAH IR Spectroscopic Database <30665870+PAHdb@users.noreply.github.com>
Date:   Tue Mar 13 16:34:43 2018 -0700

    Merge pull request #1 from mattjshannon/master
    
    Added Python3 functionality to codebase, updated documentation.

[33mcommit ae017ac4e5f9d506d38b4e94f49eadeb93f571e8[m
Author: Matt Shannon <matthew.j.shannon@gmail.com>
Date:   Tue Mar 13 16:25:26 2018 -0700

    Updated makefiles to accept either version of Python (2 or 3).

[33mcommit 113010a542187582b572678ba9c64d61b0325dc4[m
Author: Matt Shannon <matthew.j.shannon@gmail.com>
Date:   Tue Mar 13 16:15:14 2018 -0700

    Updated .py files to accept Python 3 (as well as 2).

[33mcommit b299a0faf1c957eb43e95ac040d3f05633aab207[m
Author: Matt Shannon <matthew.j.shannon@gmail.com>
Date:   Tue Mar 13 15:40:57 2018 -0700

    Added VERSION to setup.py list of required files.

[33mcommit 7fd7487635487486e9d0d0ae456b6257b61a4520[m
Author: Matt Shannon <matthew.j.shannon@gmail.com>
Date:   Tue Mar 13 15:35:39 2018 -0700

    Updated readme.md
    
    Removed extra installation options (unnecessary!).

[33mcommit 7991fd2a99be4e6f2ddf80cba9c249c78129f807[m
Merge: 0b700df 1c3a036
Author: Matt Shannon <matthew.j.shannon@gmail.com>
Date:   Tue Mar 13 15:29:22 2018 -0700

    Merge pull request #1 from mattjshannon/update-documentation
    
    Updated readme

[33mcommit 1c3a03639a372c3ba84bb99a41703dfffed19131[m
Author: Matt Shannon <matthew.j.shannon@gmail.com>
Date:   Tue Mar 13 15:05:43 2018 -0700

    Updated readme
    
    Added alternative installation method, set headers for examples, unit tests, documentaiton; and created requirements category (needs version numbers still).

[33mcommit 0b700df9160684719cd86d2cb2dfadec97fedf58[m
Author: Christiaan Boersma <Christiaan.Boersma@nasa.gov>
Date:   Wed Mar 7 17:37:57 2018 -0800

    Fixed typos, inconsistencies and added documentation

[33mcommit cceca613bee9148fb2ba49cf8ecb774d3232152a[m
Author: Christiaan Boersma <Christiaan.Boersma@nasa.gov>
Date:   Wed Mar 7 17:29:33 2018 -0800

    This reverts commit 9555fb1961d5e31763e82a1b3fe68ef0c743c384.

[33mcommit 9555fb1961d5e31763e82a1b3fe68ef0c743c384[m
Author: Christiaan Boersma <Christiaan.Boersma@nasa.gov>
Date:   Wed Mar 7 17:23:24 2018 -0800

    Fixed typos, inconsistencies and added documentation

[33mcommit 8cdd2185faf277358f4959ad3894b230e851b56a[m
Author: Christiaan Boersma <Christiaan.Boersma@nasa.gov>
Date:   Fri Mar 2 12:40:39 2018 -0800

    Initial commit

[33mcommit f9215596ca4f7ff0ef4517c7b3a30b8237d00a2b[m
Author: NASA Ames PAH IR Spectroscopic Database <30665870+PAHdb@users.noreply.github.com>
Date:   Wed Aug 2 11:07:41 2017 -0700

    Initial commit
