from setuptools import setup, find_packages
import os


VERSION = '1.0.0' # alpha
DESCRIPTION = 'Web Feature Service in python'
LONG_DESCRIPTION = 'Web Feature Service (WFS) written in Python3'

setup(
      name = "pywfs",
      version=VERSION,
      author = "Anders Johan Konnestad",
      author_email="anders.johan@konnestad.com",
      description=DESCRIPTION,
      long_description_content_type="text/markdown",
      long_description=LONG_DESCRIPTION,
      packages=find_packages(),
      install_requires=['bs4'],
      keywords=["WFS"]
      )
