import json
import logging
import os.path

import dask.bag.core
import dask.base
import dask.bytes.core
import indexed_gzip as igzip
import toolz
from dask.delayed import delayed


log = logging.getLogger(__name__)


delayed = delayed(pure=True)


class IGzipReader:

    def __init__(self, urlpath, chunk_size, spacing=1048576):
        self.urlpath = urlpath
        self.chunk_size = chunk_size
        self.spacing = spacing

    @property
    def igzip_index_path(self):
        return "%s.gzidx" % (os.path.splitext(self.urlpath)[0],)

    @property
    def lines_index_path(self):
        return "%s.lines-index-%d" % (self.urlpath, self.chunk_size)

    def ensure_indexes(self):
        if not os.path.exists(self.igzip_index_path):
            log.warning("Generating gzip index for %s" % self.urlpath)
            with igzip.IndexedGzipFile(self.urlpath, spacing=self.spacing) as fobj:
                fobj.build_full_index()
                fobj.export_index(self.igzip_index_path)
        if not os.path.exists(self.lines_index_path):
            log.warning("Generating lines index for %s" % self.urlpath)
            with igzip.IndexedGzipFile(self.urlpath, index_file=self.igzip_index_path) as fobj:
                line_index = []
                line_index.append(fobj.tell())  # start
                for i, l in enumerate(fobj):
                    if (i + 1) % self.chunk_size == 0:  # +1, for we already read the line
                        line_index.append(fobj.tell())
            with open(self.lines_index_path, "w") as f:
                json.dump(line_index, f)

    def count_chunks(self):
        return len(json.load(open(self.lines_index_path)))

    def __call__(self, chunk):
        # read chunk
        line_index = json.load(open(self.lines_index_path))
        start = line_index[chunk]
        data = []
        with igzip.IndexedGzipFile(self.urlpath, index_file=self.igzip_index_path) as fobj:
            fobj.seek(start)
            for i, text in zip(range(self.chunk_size), fobj):
                data.append(text)
        return data


def _read_chunk(urlpath, chunk_size, chunk):
    return IGzipReader(urlpath=urlpath, chunk_size=chunk_size)(chunk)


def read_lines(urlpath, chunk_size=None, storage_options=None):
    spacing = storage_options.get("index_spacing", 1048576) if storage_options else 1048576
    fs, fs_token, paths = dask.bytes.core.get_fs_token_paths(
        urlpath, mode='rb', storage_options=storage_options)
    all_chunks = []
    for path in paths:
        reader = IGzipReader(urlpath=path, chunk_size=chunk_size, spacing=spacing)
        reader.ensure_indexes()
        all_chunks.append(list(range(reader.count_chunks())))
    delayed_read = delayed(_read_chunk)
    out = []
    for path, chunks in zip(paths, all_chunks):
        token = dask.base.tokenize(fs_token, path, fs.ukey(path), "igzip", chunks)
        keys = ['read-block-%s-%s' % (chunk, token) for chunk in chunks]
        out.append([
            delayed_read(path, chunk_size, chunk, dask_key_name=key)
            for chunk, key in zip(chunks, keys)
        ])
    return False, out


def read_text(urlpath, collection=True, chunk_size=None, storage_options=None,
              encoding=None, errors='strict'):
    _, blocks = read_lines(
        urlpath, chunk_size=chunk_size, storage_options=storage_options)

    if encoding:
        ddecode = delayed(decode)
        blocks = [ddecode(block, encoding, errors) for block in toolz.concat(blocks)]
    else:
        blocks = list(toolz.concat(blocks))
    if not collection:
        return blocks
    else:
        return dask.bag.core.from_delayed(blocks)


def decode(lines, encoding, errors):
    return [line.decode(encoding, errors) for line in lines]
