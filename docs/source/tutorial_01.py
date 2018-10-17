
# coding: utf-8

# # Tutorial 01: a single Spitzer spectrum

# We begin this series by performing a simple analysis of a single astronomical spectrum. We will use one of the sample spectra here. Feel free to follow along, and attempt the same method with a simple spectrum of your own.

# Data used in this example: `pyPAHdb/data/sample_data_NGC7023-NW-PAHs.txt`

# # Table of contents
# 1. [Import needed modules](#step1)
# 2. [Data validation](#step2)
#     1. [Inspect the data](#step2a)
#     2. [Make a quick plot](#step2b)    
# 3. [Running pyPAHdb](#step3)
#     1. [Instantiate an observation object](#step3a)
#     2. [Pass the spectrum to decomposer](#step3b)
#     3. [Write the results to disk](#step3c)

# ## <font color=blue>Step 1</font>: Necessary modules <a name="step1"></a>

# In[7]:


# The below command will suppress the shell output, since we are using
# matplotlib within a notebook.
get_ipython().run_line_magic('matplotlib', 'inline')

import os
import pkg_resources

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pypahdb.decomposer import Decomposer
from pypahdb.observation import Observation


# ***

# ## <font color=blue>Step 2</font>: Data validation <a name="step2"></a>

# You should ensure your data has a simple format. Acceptable formats include:
# 
# - FITS
#     - ...
#     
# - ASCII
#     - either two-column (wavelength, flux) or three-column (wavelength, flux, flux error)
#     - seperated by commas (CSV) or single spaces

# ### A. Inspect the data <a name="step2a"></a>

# We will use the example spectrum ``sample_data_NGC7023-NW-PAHs.txt``, included in the pypahdb distribution.

# In[8]:


# Loading from the data directory. For your uses, point to the location
# of the spectrum you are examining.
# data_file = data_dir + 'NGC7023-NW-PAHs.txt'
data_file = pkg_resources.resource_filename('pypahdb', 'data/sample_data_NGC7023-NW-PAHs.txt')


# Let's examine the first few lines of this file so we understand its structure...

# In[9]:


for index, line in enumerate(open(data_file, 'r')):
    print(line, end='')
    if index >= 3:
        break


# We will use `pandas` to load the data for quick analysis:

# In[10]:


df = pd.read_csv(data_file, sep=' ')  # Loads the data into a pandas DataFrame.


# In[11]:


df.head()


# ### B. Make a quick plot <a name="step2b"></a>

# Let's make a quick plot to make sure the spectrum has no unusual features/artifacts.

# In[13]:


plt.plot(df['wavelength'], df['surface brightness'])
plt.xlabel('Wavelength (μm)')
plt.ylabel('Surface brightness (MJy/sr)')


# We see that it is a reasonably smooth spectrum composed of Spitzer/IRS
# observations using the SL module (SL1 and SL2, covering ~5-14 microns approximately).

# The data needs to be monotonic, i.e. not double-valued or out of order (as determined by the wavelength array).

# In[14]:


def strictly_increasing(L):
    return all(x < y for x, y in zip(L, L[1:]))

strictly_increasing(df['wavelength'])


# ***

# ## <font color=blue>Step 3</font>: Running pyPAHdb <a name="step3"></a>

# ### A. Instantiate an ``observation`` object <a name="step3a"></a>

# All that's needed is the path to the text file above.

# In[15]:


data_file


# In[16]:


obs = Observation(data_file)


# In[17]:


obs.file_path


# Now we have an ``observation`` object that encapsulates our data.

# ### B. Pass the spectrum to ``decomposer`` <a name="step3b"></a>

# Now with our ``observation`` instance, we simply pass its spectrum to the pyPAHdb ``decomposer``, which will perform the decomposition by PAH.

# In[18]:


pahdb_fit = Decomposer(obs.spectrum)


# Now we have a ``decomposer`` object that encapsulates the fit.

# ### C. Write the results to disk <a name="step3c"></a>

# The `Decomposer` class includes methods for saving the fit results to disk:

# In[19]:


# write results to file
pahdb_fit.save_pdf(filename='NGC7023_pypahdb.pdf')
pahdb_fit.save_fits(filename='NGC7023_pypahdb.fits')


# ***
