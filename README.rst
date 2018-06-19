Dask indexed gzip
##################

|pypi-version| |travis| |coveralls|

An implementation compatible with `dask read_text`_ interface,
than can chunk a gzipped text file into several partitions,
thanks to an index, provided by `indexed_gzip`_

This is useful when your data resides in a big gzipped file,
yet you want to leverage dask parallelism capabilities.

Sample session
---------------

::

  >>> import os
  >>> import dask_igzip

.. initalization

  >>> data_path = os.path.join(os.path.dirname(dask_igzip.__file__), "..", "test", "data")

::

  >>> source = os.path.join(data_path, "sample.txt.gz")
  >>> # 3 lines per chunk (obviously this is for demoing)
  >>> bag = dask_igzip.read_text(source, chunk_size=3, encoding="utf-8")
  >>> lines = bag.take(4, npartitions=2)
  >>> print("".join(lines).strip())
  a first sentence
  a second sentence
  a third sentence
  a fourth sentence
  >>> bag.str.upper().str.strip().compute()[8]
  'LINE 9'

Why ?
-----

Dask `read_text` creates a unique partition if you provide it with a gzip file.
This limitations comes from the fact that
there is no way to split the gzip file in a predictable yet coherent way.

This project provides an implementation where the gzip is indexed,
then lines positions are also indexed,
so that reading the text can be done by chunk (thus enabling parallelism).
On first run, indexes are saved on disk, so that subsequent runs are fast.

.. _`indexed_gzip`: https://githuib.com/pauldmccarthy/indexed_gzip
.. _`dask read_text`: https://dask.pydata.org/en/latest/bag-creation.html#db-read-text


.. |pypi-version| image:: https://img.shields.io/pypi/v/dask-igzip.svg
    :target: https://pypi.python.org/pypi/dask-igzip
    :alt: Latest PyPI version
.. |travis| image:: http://img.shields.io/travis/jurismarches/dask_igzip/master.svg?style=flat
    :target: https://travis-ci.org/jurismarches/dask_igzip
.. |coveralls| image:: http://img.shields.io/coveralls/jurismarches/dask_igzip/master.svg?style=flat
    :target: https://coveralls.io/r/jurismarches/dask_igzip


