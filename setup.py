#!/usr/bin/env python3

from setuptools import setup

setup(name="deathmetal",
      version='0.1',
      description='Intel AMT Pentest Toolkit',
      author='Victor Teissler',
      author_email='nope@nope.nope',
      url='zombo.com',
      packages=['charles'],
      scripts=['bin/dm_pickles',
               'bin/dm_toki',
               'bin/dm_nathan',
               'bin/dm_rockso'],
      install_requires=['hexdump'],
)
