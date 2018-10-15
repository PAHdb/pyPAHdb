
# coding: utf-8

# # Tutorial 01: a single Spitzer spectrum

# We begin this series by performing a simple analysis of a single astronomical spectrum. We will use one of the sample spectra here. Feel free to follow along, and attempt the same method with a simple spectrum of your own.

# Data used in this example: pyPAHdb/data/sample_data_NGC7023-NW-PAHs.txt

# ***

# ## <span style="color:blue">Step 1</span>: Necessary modules and paths

# In[1]:


# The below command will suppress the shell output, since we are using
# matplotlib within a notebook.
get_ipython().run_line_magic('matplotlib', 'inline')

import matplotlib.pyplot as plt
import numpy as np
import os
import pkg_resources
import pypahdb


# ***

# ## <span style="color:blue">Step 2</span>: Preparing the data

# You should ensure your data has a simple format. Acceptable formats include:
# 
# - FITS
#     - ...
#     
# - ASCII
#     - either two-column (wavelength, flux) or three-column (wavelength, flux, flux error)
#     - seperated by commas (CSV) or single spaces
#     - ***what about headers?? do we use skiprows in pypahdb right now??***

# ### Load the data

# We will use the example spectrum ``sample_data_NGC7023-NW-PAHs.txt`` here.

# In[2]:


# Loading from the data directory. For your uses, point to the location
# of the spectrum you are examining.
# data_file = data_dir + 'NGC7023-NW-PAHs.txt'
data_file = pkg_resources.resource_filename('pypahdb', 'data/sample_data_NGC7023-NW-PAHs.txt')
data_file


# Let's examine the first few lines of this file so we understand its structure...

# In[3]:


for index, line in enumerate(open(data_file, 'r')):
    print(line, end='')
    if index >= 3:
        break


# So we have two columns separated by a space, the first being wavelength
# and the second being surface brightness (for convenience we'll call this
# flux). The line breaks (\n) will be handled easily by np.loadtxt (or any other module you desire):

# In[4]:


wave, flux = np.loadtxt(data_file, delimiter=' ', dtype='float', skiprows=1).T


# We used .T to transpose the array (such that it's column-oriented).

# Now let's check its dimensions and type(s).

# In[5]:


len(wave), len(flux), type(wave), type(wave[0]), type(flux[0])


# ### Examine the data

# In[6]:


plt.plot(wave, flux);
plt.xlabel(r'Wavelength ($\mu$m)');
plt.ylabel('Surface brightness (MJy/sr)');


# We see that it is a reasonably smooth spectrum composed of Spitzer/IRS
# observations using the SL module (SL1 and SL2, covering ~5-14 microns approximately).

# The data needs to be monotonic, i.e. not double-valued or out of order (as determined by the wavelength array).

# In[7]:


def strictly_increasing(L):
    return all(x<y for x, y in zip(L, L[1:]))

strictly_increasing(wave)


# ***

# ## <span style="color:blue">Step 3</span>: Running pyPAHdb (short version)

# ### 1. Instantiate an ``observation`` object

# All that's needed is the path to the text file above.
# ** can it accept both space and CSV files ???? **

# In[8]:


observation = pypahdb.observation(data_file)


# In[9]:


observation.file_path


# Now we have an ``observation`` object that encapsulates our data.

# ### 2. Pass the spectrum to ``decomposer``

# Now with our ``observation`` instance, we simply pass its spectrum to the pyPAHdb ``decomposer``, which will perform the decomposition by PAH.

# In[12]:


result = pypahdb.decomposer(observation.spectrum)


# Now we have a ``decomposer`` object that encapsulates the fit.

# ### 3. Plot and save the results using ``writer``

# ``pypahdb.writer`` is a convenient way to view and save your results.

# In[14]:


# write results to file
# by default, will save PDF and FITS files; can turn off with save_pdf=False as an argument.
# by default, saves output to the directory containing the input file;
# can instead save to a user-defined directory by setting output_directory.
# e.g., output_directory='' will save to the local folder.
pypahdb.writer(result);


# ***

# ## <span style="color:blue">Step 3</span>: Running pyPAHdb (long version with details)

# ### 1. Instantiate an ``observation`` object

# All that's needed is the path to the text file above.
# ** can it accept both space and CSV files ???? **

# In[32]:


observation = pypahdb.observation(data_file)


# Now we have an ``observation`` object that encapsulates our data.

# In[34]:


observation.file_path


# The wavelength array is contained within ``observation.spectrum.abscissa``.

# In[46]:


type(observation.spectrum.abscissa)


# In[45]:


observation.spectrum.abscissa[:10]


# In[47]:


observation.spectrum.abscissa.shape


# The flux array is within ``observation.spectrum.ordinate``.

# In[42]:


type(observation.spectrum.ordinate)


# In[43]:


observation.spectrum.ordinate.shape


# ### 2. Pass the spectrum to ``decomposer``

# Now with our ``observation`` instance, we simply pass its spectrum to the pyPAHdb ``decomposer``, which will perform the decomposition by PAH.

# ** seems like you shouldn't need to specify observation.spectrum?? just observation? or...? **

# In[48]:


result = pypahdb.decomposer(observation.spectrum)


# In[49]:


type(result)


# In[51]:


type(result.charge)


# In[53]:


type(result.fit)


# In[54]:


type(result.ionized_fraction)


# In[55]:


type(result.large_fraction)


# In[56]:


type(result.norm)


# In[57]:


type(result.size)


# In[58]:


type(result.spectrum)
