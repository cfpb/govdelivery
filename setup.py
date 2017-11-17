from setuptools import setup


setup(
    name='govdelivery',
    version_format='{tag}.dev{commitcount}+{gitsha}',
    author='CFPB',
    author_email='tech@cfpb.gov',
    packages=['govdelivery'],
    include_package_data=True,
    description=u'python module for interacting with the govdelivery api',
    long_description=open('README.rst').read(),
    url='https://github.com/cfpb/govdelivery',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'License :: Public Domain',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Topic :: Communications :: Email',
    ],
    zip_safe=False,
    setup_requires=['setuptools-git-version'],
)
