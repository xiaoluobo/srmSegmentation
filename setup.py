from distutils.core import setup
import os
from distutils.core import setup

version = '0.1'
README = os.path.join(os.path.dirname(__file__), 'README')
long_description = open(README).read()

setup(name='srm',
      version=version,
      description=("Statistical Region Merging in Python"),
      long_description=long_description,
      classifiers=[
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='image segmentation',
      author='Olivier Schwander',
      author_email='schwander@lix.polytechnique.fr',
      url='http://www.lix.polytechnique.fr/~schwander/python-srm',
      license='BSD',
      packages=['SRM'],
      )

