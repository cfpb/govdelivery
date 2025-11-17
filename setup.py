from setuptools import find_packages, setup


long_description = open('README.md', 'r').read()

install_requires = ['requests>=2.22.0,<3']

testing_extras = [
    'coverage',
    'responses',
]

setup(
    name='govdelivery',
    url='https://github.com/cfpb/govdelivery',
    author='CFPB',
    author_email='tech@cfpb.gov',
    description='Python module for interacting with the GovDelivery API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='CC0',
    version='1.5',
    include_package_data=True,
    packages=find_packages(),
    install_requires=install_requires,
    extras_require={
        'testing': testing_extras,
    },
    test_suite='govdelivery.tests',
    python_requires='>=3.10',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Communications :: Email',
    ],
    zip_safe=False,
)
