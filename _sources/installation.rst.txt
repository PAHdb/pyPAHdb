.. sectnum::
   :start: 3

============
Installation
============

PyPAHdb can be installed using pip directly from its
GitHub-repository with::

    $ pip install git+https://github.com/PAHdb/pyPAHdb.git

Note that upon first-run a precomputed matrix will need to be downloaded from
PAHdb's server. A menu with different configurations will be presented from
which a selection must be made. The `version`-keyword to the
`Decomposer`-constructor can be used to pick a specific version directly, e.g.,
"3.20". If the version is not locally available, it will be automatically
downloaded. To present the picker menu again, the `version`-keyword can be set
to "picker". Upon subsequent runs and the `version`-keyword is not set, the
latest locally available version is used.
