from os import path
from os import getenv
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
import versioneer

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

"""
NOTE: This file must remain Python 2 compatible for the foreseeable future,
to ensure that we error out properly for people with outdated setuptools
and/or pip.
if sys.version_info < (3, 6):
   error = '''
pypahdb does not support Python {0}.{2}.
Python 3.6 and above is required. Check your Python version like so:

python3 --version

This may be due to an out-of-date pip. Make sure you have pip >= 9.0.1.
Upgrade pip like so:

pip install --upgrade pip
'''.format(3, 6)
   sys.exit(error)
"""

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

with open(path.join(here, 'requirements.txt')) as requirements_file:
    # Parse requirements.txt, ignoring any commented-out lines.
    requirements = [line for line in requirements_file.read().splitlines()
                    if not line.startswith('#')]


class BuildPyCommand(build_py):
    def run(self):
        remote_pkl = 'https://www.astrochemistry.org/pahdb/pypahdb/pickle.php'
        if getenv('GITHUB_ACTIONS') == 'true':
            remote_pkl += '?github_actions=true'
        local_pkl = 'pypahdb/resources/precomputed.pkl'
        # honor the --dry-run flag
        if not self.dry_run:
            response = urlopen(remote_pkl)
            with open(path.join(here, local_pkl), 'wb') as f:
                f.write(response.read())
        versioneer.get_cmdclass()['build_py'].run(self)
        build_py.run(self)

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.


setup(
    # This is the name of your project. The first time you publish this
    # package, this name will be registered for you. It will determine how
    # users can install this project, e.g.:
    #
    # $ pip install pypahdb
    #
    # There are some restrictions on what makes a valid project name
    # specification here:
    # https://packaging.python.org/specifications/core-metadata/#name
    name='pypahdb',  # Required

    # Versions should comply with PEP 440:
    # https://www.python.org/dev/peps/pep-0440/
    #
    # For a discussion on single-sourcing the version across setup.py and the
    # project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=versioneer.get_version(),  # Required

    # This is a one-line description or tagline of what your project does. This
    # corresponds to the "Summary" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#summary
    description='Using a precomputed matrix of theoretically calculated \
                PAH emission spectra from the NASA Ames PAH IR Spectroscopic \
                Database, a spectrum is decomposed into contribution PAH \
                subclasses using a NNLS-approach',  # Required

    # This is an optional longer description of your project that represents
    # the body of text which users will see when they visit PyPI.
    #
    # Often, this is the same as your README, so you can just read it in from
    # that file directly (as we have already done above)
    #
    # This field corresponds to the "Description" metadata field:
    # https://packaging.python.org/specifications/
    # core-metadata/#description-optional
    long_description=long_description,  # Optional

    # This should be a valid link to your project's main homepage.
    #
    # This field corresponds to the "Home-Page" metadata field:
    # https://packaging.python.org/specifications/
    # core-metadata/#home-page-optional
    url='https://www.astrochemistry.org/pahdb/pypahdb/',  # Optional

    # This should be your name or the name of the organization which owns the
    # project.
    author='Dr. Christiaan Boersma',  # Optional

    # This should be a valid email address corresponding to the author listed
    # above.
    author_email='Christiaan.Boersma@nasa.gov',  # Optional

    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Astronomy',

        # Pick your license as you wish
        'License :: OSI Approved :: BSD License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
    ],

    # This field adds keywords for your project which will appear on the
    # project page. What does your project relate to?
    #
    # Note that this is a string of words separated by whitespace, not a list.
    keywords='PAH Spectroscopy NASA Ames Fitting',  # Optional

    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    packages=find_packages(exclude=['docs', 'tests']),  # Required

    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    #
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=requirements,  # Optional

    # List additional groups of dependencies here (e.g. development
    # dependencies). Users will be able to install these using the "extras"
    # syntax, for example:
    #
    #   $ pip install sampleproject[dev]
    #
    # Similar to `install_requires` above, these must be valid existing
    # projects.
    # extras_require={  # Optional
    #    'dev': ['check-manifest'],
    #    'test': ['coverage'],
    # },

    # If there are data files included in your packages that need to be
    # installed, specify them here.
    #
    # If using Python 2.6 or earlier, then these have to be included in
    # MANIFEST.in as well.
    include_package_data=True,
    package_data={  # Optional
        'pypahdb': ['resources/*'],
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/
    # setupscript.html#installing-additional-files
    #
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],  # Optional

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    # entry_points={  # Optional
    #    'console_scripts': [
    #        'sample=sample:main',
    #    ],
    # },

    # List additional URLs that are relevant to your project as a dict.
    #
    # This field corresponds to the "Project-URL" metadata fields:
    # https://packaging.python.org/specifications/
    # core-metadata/#project-url-multiple-use
    #
    # Examples listed include a pattern for specifying where the package tracks
    # issues, where the source is hosted, where to say thanks to the package
    # maintainers, and where to support the project financially. The key is
    # what's used to render the link text on PyPI.
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/pahdb/pypahdb/issues',
        'Source': 'https://github.com/pahdb/pypahdb/',
    },

    # Run custom commands
    cmdclass={  # Optional
        'build_py': BuildPyCommand,
    },
)
