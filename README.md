# govdelivery

A quite incomplete client for the GovDelivery Communications Cloud API v1.

Currently, you can subscribe a user; manage their topics, categories, and
question responses; and get the list of available topics.

The GovDelivery Communications Cloud API is described here:
https://developer.govdelivery.com/api/comm_cloud_v1/Default.htm


## Status

Officially supports both Python 2.7 and Python 3.6.


## Installation

`pip install govdelivery`


## Running the tests

To lint the code and execute the unit tests,
we recommend using [tox](https://tox.readthedocs.io/).

1. Install tox in a virtualenv or in your global Python environment by running
   `pip install tox`.

   Alternately, we also like using [pipx](https://github.com/pipxproject/pipx)
   for installing and running system-wide tools like tox.
1. Run all the tests in one go with `tox`.
1. If you want to run just the linting tools (flake8 and isort), you can run
   `tox -e lint`.
1. If you want to run tests in just Python 2 or just Python 3, you can run
   `tox -e py27` or `tox -e py36`.


## Changelog

### 1.3 – 2019-11-25

- Add Python 3 support
- Improve test coverage and add tox support for easy test running
- Fix a few assorted bugs

### 1.2 – 2018-09-17

- Support updating a subscriber's response to a select question (as opposed to
  a free response question)

### 1.1 – 2017-11-06

- Allow SMS subscriptions
- Allow notifications to be enabled on certain method calls

### 1.0 – 2017-01-31

Initial public release.


## Open source licensing info

1. [`TERMS.md`](TERMS.md)
2. [`LICENSE`](LICENSE)
3. [CFPB Source Code Policy](https://github.com/cfpb/source-code-policy)
