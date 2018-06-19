Dask indexed gzip
##################

An implementation compatible with `dask read_text`_ interface,
than can chunk a gzipped text file into several partitions,
thanks to an index, provided by `indexed_gzip`_

Dask `read_text` create a unique partition if you provide it with a gzip file.
This is understandable, there is no way to split the gzip file in a predictable
yet coherent way.
This project provides an implementation where the gzip is indexed,
then lines positions are also indexed,
so that reading the text can be done by chunk (thus enabling parallelism).
On first run, indexes are saved on disk, so that subsequent runs are fast.

.. _`indexed_gzip`: https://githuib.com/pauldmccarthy/indexed_gzip
.. _`dask read_text`: https://dask.pydata.org/en/latest/bag-creation.html#db-read-text
