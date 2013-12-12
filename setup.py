import os
from setuptools import setup, find_packages


def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''


setup(
    name='govdelivery',
    version=__import__('govdelivery').__version__,
    author='CFPB',
    author_email='tech@cfpb.gov',
    packages=['django-govdelivery'],
    include_package_data=True,
    description=u'Django app for interacting with the govdelivery api',
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
