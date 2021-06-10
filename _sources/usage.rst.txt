.. sectnum::
   :start: 4

=====
Usage
=====

Sample code demonstrating the use of pypahdb is shown below, which has been
included in the pypahdb package as ``examples/example_tbl.py``. The example
makes use of  the bundled ``sample_data_NGC7023.tbl`` spectrum.

.. code-block:: python

    import pkg_resources

    from pypahdb.decomposer import Decomposer
    from pypahdb.observation import Observation


    if __name__ == '__main__':

        # The sample data (IPAC table).
        file_path = 'resources/sample_data_NGC7023.tbl'
        data_file = pkg_resources.resource_filename('pypahdb', file_path)

        # Construct an Observation object.
        obs = Observation(data_file)

        # Pass the Observation's spectrum to Decomposer, which performs the fit.
        pahdb_fit = Decomposer(obs.spectrum)

        # Save the fit to disk, both as a PDF and FITS file.
        pahdb_fit.save_pdf('NGC7023_pypahdb_tbl_example.pdf', domaps=False)
        pahdb_fit.save_fits('NGC7023_pypahdb_tbl_example.fits', header=obs.header)


Details
---------

Let's briefly explore what the code above is doing.

First the ``Decomposer`` and ``Observation`` classes are imported from
pypahdb. The``pkg_resources`` package is used to locate and load the
provided sample data.

.. code-block:: python

    import pkg_resources

    from pypahdb.decomposer import Decomposer
    from pypahdb.observation import Observation


    if __name__ == '__main__':

        # The sample data (IPAC table).
        file_path = 'resources/sample_data_NGC7023.tbl'
        data_file = pkg_resources.resource_filename('pypahdb', file_path)



The included example IPAC table, ``sample_data_NGC7023.tbl``, contains the
astronomical PAH spectrum shown below:

.. image:: figures/ngc7023_spectrum.png
   :align: center

The file is read with the ``Observation`` class by instantiating it and passing
the path as its argument:

.. code-block:: python

    # Construct an Observation object.
    obs = Observation(data_file)

Note that that the ``Observation`` class is able to handle a variety of
file-formats, not just IPAC tables.

The decomposition is performed by creating a ``Decomposer``-instance and
passing it ``obs.spectrum`` as its only positional argument.
.. code-block:: python

    # Pass the Observation's spectrum to Decomposer, which performs the fit.
    pahdb_fit = Decomposer(obs.spectrum)

The ``Decomposer`` class has two methods for producing output. On for saving
to PDF; ``save_pdf``, the other for saving to FITS, ``save_fits``. Both
methods require the filename to write to as their first positional argument.

.. code-block:: python

    # Save the fit to disk, both as a PDF and FITS file.
    pahdb_fit.save_pdf('NGC7023_pypahdb_tbl_example.pdf', domaps=False)
    pahdb_fit.save_fits('NGC7023_pypahdb_tbl_example.fits', header=obs.header)

Note that ``header=obs.header`` is explicitely passed to ``save_fits``, but
can be set arbitrary, i.e., it is possible to provide a customized the header.
