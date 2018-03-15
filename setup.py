import sys
from os import path,listdir
from setuptools import setup,find_packages
__version__ = "0.0.0.0"
REQUIRES = [
    'numpy>=1.12.1'
]
setup(
    name = 'SDP',
    author = 'zhhrozhh',
    author_email = 'zhangh40@msu.edu',
    url = 'https://github.com/zhhrozhh',
    version = __version__,
    license = 'MIT',
    classifiers = [
        'Programming Language :: Python :: 3.5'
    ],
    keywords = 'TODO',
    packages = find_packages(),
    install_requires = REQUIRES
)
