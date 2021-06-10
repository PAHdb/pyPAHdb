"""The pypahdb Python package is being developed as part of the
awarded James Webb Space Telescope (JWST) Early Release Science (ERS)
program "Radiative Feedback from Massive Stars as Traced by Multiband
Imaging and Spectroscopic Mosaics" (ID: 1288). The entire program is
coordinated by an international "Core team" of 19 scientists and
supported by 119 "science collaborators". pypahdb is developed by the
NASA Ames PAH IR Spectroscopic Database team, asscociated with the
Astrophysics & Astrochemistry Laboratory at NASA Ames Research Center.

The NASA Ames PAH IR Spectroscopic Database and pypahdb are being
supported through a directed Work Package at NASA Ames titled:
"Laboratory Astrophysics - The NASA Ames PAH IR Spectroscopic
Database".

pypahdb uses a precomputed matrix of theoretically calculated PAH
emission spectra from version 3.00 of the library of computed
spectra and is downloaded when installing the package. This matrix has
been constructed from a collection of "astronomical" PAHs, which meet
the following critera and include the fullerenes C₆₀ and C₇₀:

       'magnesium=0 oxygen=0 iron=0 silicium=0 chx=0 ch2=0 c>20 hydrogen>0'

The PAH emission spectra have been calculated employing a PAH emission
model with the following parameters:

* A calculated vibrational temperature upon the absorption of a 7 eV
  photon.
* A calculated integrated band intensity after following the entire
  emission cascade.
* A redshift of 15 cm⁻¹ to mimic *some* anharmonic effect.
* A Gaussian emission profile with a FWHM of 15 cm⁻¹.

Additional information can be found at the NASA Ames PAH IR
Spectroscopic Database website, which is located at
https://www.astrochemistry.org/pahdb/

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
      SPECTROSCOPIC DATABASE VERSION 2.00: UPDATED CONTENT, WEBSITE
      AND ON/OFFLINE TOOLS", The Astrophysical Journal Supplement
      Series, 211, 8, 2014 https://doi.org/10.1088/0067-0049/211/1/8

    * Mattioda, A. L., Hudgins, D. M., Boersma, C., Ricca, A.,
      Peeters, E., Cami, J., Sanchez de Armas, F., Puerta Saborido,
      G., Bauschlicher, C. W., J., and Allamandola, L. J. "THE NASA
      AMES PAH IR SPECTROSCOPIC DATABASE: THE LABORATORY SPECTRA", The
      Astrophysical Journal Supplement Series, 251, 22, 2020,
      https://doi.org/10.3847/1538-4365/abc2c8
"""

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
