import os
from setuptools import setup, find_packages


setup(
    name='govdelivery',
    version=__import__('govdelivery').__version__,
    author='CFPB',
    author_email='tech@cfpb.gov',
    packages=['govdelivery'],
    include_package_data=True,
    description=u'python module for interacting with the govdelivery api',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',      
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
    ],
    zip_safe=False,
)
