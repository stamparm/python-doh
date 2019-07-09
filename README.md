python-doh [![Build Status](https://api.travis-ci.org/stamparm/python-doh.svg?branch=master)](https://travis-ci.org/stamparm/python-doh) [![Python 2.6|2.7|3.x](https://img.shields.io/badge/python-2.6|2.7|3.x-yellow.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/stamparm/python-doh/blob/master/LICENSE)
=========

Python client for DNS over HTTPS (DoH) protocol

Example usage:

```
>>> import client
>>> print(client.query("one.one.one.one"))
['1.0.0.1', '1.1.1.1']
>>> print(client.query("one", "NS"))
['a.nic.one.', 'b.nic.one.', 'c.nic.one.', 'd.nic.one.']
```
