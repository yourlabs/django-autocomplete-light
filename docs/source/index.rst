Welcome to django-autocomplete-light's documentation!
=====================================================

.. include:: ../../README.rst

Demo
----

You can run test projects for a local demo in a temporary virtualenv.
  
.. toctree::
   :maxdepth: 1

   demo

Install
-------

Click on any instruction step for details.

.. toctree::
   :maxdepth: 3

   install

If you didn't click any, and this is your first install: bravo !

Upgrade
-------

v1 to v2
````````

.. toctree::
   :maxdepth: 3

   1to2

Other upgrades
``````````````

Run ``pip install -U django-autocomplete-light``. Check the CHANGELOG
for BC (Backward Compatibility) breaks. There should be none for minor
version upgrades ie. from 1.1.3 to 1.1.22, but there might be some
minor BC breaks for middle upgrades ie. 1.2.0 to 1.3.0.

Quick start
-----------

Enabling autocompletes inside and outside of the admin has become piece of
cake.

.. toctree::
   :maxdepth: 3

   tutorial

.. _reference:

Tutorial
--------

If you need anything more than just enabling autocompletes in the admin, then
you should understand django-autocomplete-light's architecture. Because you can
override any part of it. 

The architecture is based on 3 main parts which you can override to build
insanely creative features as many users already did.

.. toctree::
   :maxdepth: 3

   autocomplete
   form
   script
   cookbook

Topics
------

Using just the concepts you've learned in the reference, here are some of the
things you can do.

.. toctree::
   :maxdepth: 1

   template
   navigation
   dependant
   generic
   debug

FAQ
---

.. toctree::
   :maxdepth: 2

   faq


API: find hidden gems
---------------------

.. toctree::
   :maxdepth: 3

   api

Documentation that has not yet been ported to v2
------------------------------------------------

.. toctree::
   :maxdepth: 1

   charfield
   addanother
   remote
   django13
   contrib

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

