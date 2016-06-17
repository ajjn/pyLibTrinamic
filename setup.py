# setup.py
from distutils.core import setup
import sys

#windows installer:
# python setup.py bdist_wininst

# patch distutils if it can't cope with the "classifiers" or
# "download_url" keywords
if sys.version < '2.2.3':
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None

setup(
    name="pyLibTrinamic",
    description="Python module for trinamic device communication",
    version="0.0.6",
    author="Antti Nykanen",
    author_email="antti.nykanen@iki.fi",
    packages=['pyLibTrinamic'],
    license="Python",
    long_description="Python module for trinamic device communication using serial MODBUS protocol",
    classifiers = [
        'Development Status :: 1 - Developing/Unstable',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Python Software Foundation License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Topic :: Communications',
        'Topic :: Software Development :: Libraries',
        'Topic :: MODBUS  :: Serial',
    ],
)
