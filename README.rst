Dask indexed gzip
##################

|pypi-version| |travis| |coveralls|


An implementation compatible with `dask read_text`_ interface,
than can chunk a gzipped text file into several partitions,
thanks to an index, provided by `indexed_gzip`_


Sample session ::

  >>> import dask_igzip
  >>> file_path = dask_igzip()
  >>> dask.igzip.

Dask `read_text` create a unique partition if you provide it with a gzip file.
This is understandable, there is no way to split the gzip file in a predictable
yet coherent way.
This project provides an implementation where the gzip is indexed,
then lines positions are also indexed,
so that reading the text can be done by chunk (thus enabling parallelism).
On first run, indexes are saved on disk, so that subsequent runs are fast.

.. _`indexed_gzip`: https://githuib.com/pauldmccarthy/indexed_gzip
.. _`dask read_text`: https://dask.pydata.org/en/latest/bag-creation.html#db-read-text


.. |pypi-version| image:: https://img.shields.io/pypi/v/dask-igzip.svg
    :target: https://pypi.python.org/pypi/dask-igzip
    :alt: Latest PyPI version
.. |travis| image:: http://img.shields.io/travis/jurismarches/dask-igzip/master.svg?style=flat
    :target: https://travis-ci.org/jurismarches/dask-igzip
.. |coveralls| image:: http://img.shields.io/coveralls/jurismarches/dask-igzip/master.svg?style=flat
    :target: https://coveralls.io/r/jurismarches/dask-igzip


