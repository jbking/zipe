from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='zipe',
      version=version,
      description="A zip utility for cross file name encoding powered by Python.",
      long_description="""\
""",
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
          'Topic :: Utilities',
      ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='MURAOKA Yusuke',
      author_email='yusuke@jbking.org',
      url='https://github.com/jbking/zipe',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      zipe = zipe.zip:main
      unzipe = zipe.unzip:main
      """,
      )
