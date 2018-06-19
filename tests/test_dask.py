"""Dask integration tests
"""
import gzip

import pytest
from dask.distributed import Client

import dask_igzip

from .test_base import sample_data_3  # noqa


@pytest.fixture(scope="session")
def dask_client():
    client = Client(processes=False)
    return client


def test_read_text_simple(sample_data_3, dask_client):  # noqa
    bag = dask_igzip.read_text(str(sample_data_3), chunk_size=3)
    assert bag.compute(scheduler='threads') == list(gzip.open(str(sample_data_3), "rb"))


def test_read_text_multiple(sample_data_3, dask_client):  # noqa
    bag = dask_igzip.read_text([str(sample_data_3)] * 3, chunk_size=3)
    data = list(gzip.open(str(sample_data_3), "rb"))
    assert bag.compute(scheduler='threads') == data * 3


def test_read_text_with_ops(sample_data_3, dask_client):  # noqa

    def decode(x):
        return x.decode("utf-8")

    bag = dask_igzip.read_text(str(sample_data_3), chunk_size=3)
    result = bag.map(decode).map_partitions("".join).compute()
    assert result == [
        """a first sentence
a second sentence
a third sentence
""",
        """a fourth sentence
a fifth sentence
a sixth sentence
""",
        """line 7
line 8
line 9
""",
        """the last line
""",
    ]


def test_read_text_delayed(sample_data_3, dask_client):  # noqa
    result = dask_igzip.read_text(str(sample_data_3), chunk_size=3, collection=False)
    assert isinstance(result, list)
    assert len(result) == 4
    assert hasattr(result[0], "__dask_keys__")
    assert result[0].compute() == [
        b"a first sentence\n",
        b"a second sentence\n",
        b"a third sentence\n",
    ]


def test_empty():
    with pytest.raises(ValueError):
        dask_igzip.read_text([], chunk_size=3)


def test_non_existing():
    with pytest.raises(FileNotFoundError):
        dask_igzip.read_text("unexistant_data.gz", chunk_size=3)
