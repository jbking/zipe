from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='zipe',
      version=version,
      description="zip/unzip with converting file name encoding",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='MURAOKA Yusuke',
      author_email='yusuke@jbking.org',
      url='',
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
