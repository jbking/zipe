from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='zipe',
    version='0.1.3',
    description='A zip utility for cross OS, especially file name encoding problem.',
    long_description=long_description,
    url='https://github.com/jbking/zipe/',
    author='MURAOKA Yusuke',
    author_email='yusuke@jbking.org',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='zip utility',
    packages=find_packages(include=['zipe']),
    tests_require=['pytest'],
    extras_require={
        'development': ['pylint', 'twine'],
    },
    entry_points={
        'console_scripts': [
            'zipe=zipe.zip:main',
            'unzipe=zipe.unzip:main'
        ]
    }
)
