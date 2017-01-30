from codecs import open
from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

packages = find_packages(exclude=['contrib', 'docs', 'tests'])

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requires = [lib for lib in f.readlines()]

setup(
    name='rushing',
    version='0.2.0',
    description='Crawl, download, and parse TV news rush transcripts!',
    long_description=long_description,
    url='https://github.com/pezon/rushing',
    author='Peter Pezon',
    author_email='peter@pezon.net',
    license='MIT',
    packages=packages,
    install_requires=requires,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Other Audience',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    entry_points={
        'console_scripts': [
            'rush-cnn=scripts:cnn',
        ],
    },
)
