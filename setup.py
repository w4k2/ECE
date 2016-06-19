# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='eec',
    version='0.1',
    description='Exposer Ensemble Classifier',
    long_description=readme,
    author='Paweł Ksieniewicz',
    author_email='pawel.ksieniewicz@pwr.edu.pl',
    url='https://github.com/w4k2/eec',
    package_data={'': ['LICENSE']},
    license=license,
    packages=find_packages(exclude=('docs'))
)
