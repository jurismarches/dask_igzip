"""Base unit tests
"""
import py
import pytest

from dask_igzip import text


@pytest.fixture
def sample_data_3():
    sample = py.path.local(__file__).dirpath("data", "sample.txt.gz")
    text.IGzipReader(str(sample), chunk_size=3).ensure_indexes()
    return sample


@pytest.fixture
def tmp_sample(tmpdir):
    sample = py.path.local(__file__).dirpath("data", "sample.txt.gz")
    sample.copy(tmpdir)
    return tmpdir.join("sample.txt.gz")


def test_ensure_indexes(tmp_sample):
    reader = text.IGzipReader(str(tmp_sample), chunk_size=3)
    reader.ensure_indexes()
    assert tmp_sample.dirpath("sample.txt.gzidx").exists()
    assert tmp_sample.dirpath("sample.txt.gz.lines-index-3").exists()


def test_read_chunk(sample_data_3):
    assert text._read_chunk(str(sample_data_3), 3, 0) == [
        b"a first sentence\n",
        b"a second sentence\n",
        b"a third sentence\n",
    ]
    assert text._read_chunk(str(sample_data_3), 3, 3) == [
        b"the last line\n",
    ]
    assert text._read_chunk(str(sample_data_3), 3, 2) == [
        b"line 7\n",
        b"line 8\n",
        b"line 9\n",
    ]


def test_igzip_lines_info_in_order(sample_data_3):
    """even if we access only lines_count and then lines_index, it works
    """
    reader = text.IGzipReader(str(sample_data_3), chunk_size=3)
    # just accessing withotu raising is enough
    reader.lines_count
    reader.lines_index


def test_igzip_lines_info_not_indexed(tmp_sample):
    reader = text.IGzipReader(str(tmp_sample), chunk_size=3)
    with pytest.raises(RuntimeError):
        reader.chunks_count
    with pytest.raises(RuntimeError):
        reader.lines_count
    with pytest.raises(RuntimeError):
        reader.lines_index
