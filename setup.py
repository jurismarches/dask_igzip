# -*- coding: utf-8 -*-
from setuptools import setup


# inject version
__version__ = None
with open("dask_igzip/__version__.py") as f:
    exec(f.read())


with open('README.rst', 'r') as f:
    long_description = f.read()
with open('CHANGELOG.rst', 'r') as f:
    long_description += "\n\n" + f.read()


setup(
    name='dask-igzip',
    version=__version__,
    description="dask chunked read_text on gzip file",
    long_description=long_description,
    author='Jurismarches',
    author_email='contact@jurismarches.com',
    url='https://github.com/jurismarches/dask-igzip',
    packages=[
        'dask_igzip',
    ],
    install_requires=[
        'indexed_gzip>=0.8.5',
        'dask[bag]>=0.17.5',
    ],
    extras_require={
        "tests": [
            'pytest>=3.4.2',
            'pytest-cov>=2.5.1',
            'flake8>=3.5.0',
            'distributed>=1.22',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Topic :: Information Analysis',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
