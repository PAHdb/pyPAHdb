"""
The pyPAHdb module: Using a precomputed matrix of theoretically
calculated PAH emission spectra from the NASA Ames PAH IR
Spectroscopic Database a spectrum is decomposed into contribution PAH
subclasses using a nnls-approach.

The matrix of precomputed spectra is for a collection of
"astronomical" PAHs, which meet the following critera:

       'magnesium=0 oxygen=0 iron=0 silicium=0 chx=0 ch2=0 c>20'

Version 2.00 of the library of computed spectra from the NASA Ames PAH
IR Spectroscopic Database (PAHdb) has been used.

The PAH emission spectra have been calculated with the following
parameters:

   * Pure PAHs/PANHs more than 20 carbon atoms in size
   * A calculated vibrational temperature upon the absorption of a 7
     eV photon
   * Blackbody emission at the calculated vibrational temperature
   * A redshift of 15 /cm to mimic some anharmonic effect
   * Gaussian emission profile with a FWHM of 15 /cm

The NASA Ames PAH IR Spectroscopic Database website is located at
www.astrochemistry.org/pahdb/.

You are kindly asked to cite the following papers when using pyPAHdb:

    * C. Boersma, C.W. Bauschlicher, Jr., A. Ricca, A.L. Mattioda,
      J. Cami, E. Peeters, F. Sanchez de Armas, G. Puerta Saborido,
      D.M. Hudgins, and L.J. Allamandola, "THE NASA AMES PAH IR
      SPECTROSCOPIC DATABASE VERSION 2.00: UPDATED CONTENT, WEBSITE AND
      ON/OFFLINE TOOLS", The Astrophysical Journal Supplement Series,
      211, 8, 2014 10.1088/0067-0049/211/1/8

    * C.W. Bauschlicher, Jr., C. Boersma, A. Ricca, A.L. Mattioda,
      J. Cami, E. Peeters, F. Sanchez de Armas, G. Puerta Saborido,
      D.M. Hudgins, and L.J. Allamandola, "THE NASA AMES PAH IR
      SPECTROSCOPIC DATABASE: THE COMPUTED SPECTRA", The Astrophysical
      Journal Supplement Series, 189, 341, 2010
      10.1088/0067-0049/189/2/341

    * Mattioda, A. L., Hudgins, D. M., Boersma, C., Ricca, A.,
      Peeters, E., Cami, J., Sanchez de Armas, F., Puerta Saborido,
      G., Bauschlicher, C. W., J., and Allamandola, L. J. "THE NASA
      AMES PAH IR SPECTROSCOPIC DATABASE: THE LABORATORY SPECTRA", The
      Astrophysical Journal Supplement Series, XXX, 201X (in
      preparation)
"""

#with open(os.path.join(here, 'VERSION'), encoding='utf-8') as f:
#    __version__ = f.read().strip()

__version__ = "0.0.5a1"

from .observation import observation
from .spectrum import spectrum
from .decomposer import decomposer
from .writer import writer
