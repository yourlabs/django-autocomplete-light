# Autocomplete-Light: simple autocompletion web component

Difference with other HTML autocompletion elements:

- defers the rendering of the select box to the server
- lightweight javascript web component with no dependency

While it is best suited for server side framework integration, it may also be
used on its own, to create a global navigation input like in the facebook top
bar, as well as to create replacement widgets for HTML selects.

Demo
====

Clone the repository and run `python serve.py`

Usage
=====

For usage, check the [index.html source
code](https://yourlabs.io/oss/autocomplete-light/-/blob/master/index.html)

Testing
=======

This module exposes a Python library to provide an API for Selenium and make
integration testing easier with Python projects.

Install the python package with test dependencies:

```
# in repository clone
pip install -e .[test]
python serve.py &
py.test -sv
```
