# govdelivery

A quite incomplete client for the GovDelivery Communications Cloud API v1.

Currently, you can subscribe a user, manage their topic and category
subscriptions, and get the list of available topics.

The GovDelivery Communications Cloud API is described here:
https://developer.govdelivery.com/api/comm_cloud_v1/Default.htm


## Status

Currently only works with Python 2.7.
We are in the process of adding Python 3 support.


## Installation

`pip install govdelivery`


## Running the tests

1. Create or activate a virtualenv for working on govdelivery.
1. `pip install -e .`
1. `python -m unittest govdelivery.tests`


## Open source licensing info

1. [`TERMS`](TERMS.md)
2. [`LICENSE`](LICENSE)
3. [`CFPB Source Code Policy`](https://github.com/cfpb/source-code-policy)
