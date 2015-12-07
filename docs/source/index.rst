Welcome to django-autocomplete-light's documentation!
=====================================================

.. include:: ../../README.rst

Live Demo
---------

While you can use the `live demo hosted by RedHat on OpenShift
<http://dal-yourlabs.rhcloud.com>`_, you can run test projects for a local demo
in a temporary virtualenv.

.. toctree::
   :maxdepth: 1

   demo

Installation
------------

Advanced Django users are likely to install it in no time by
following this step-list. Click on a step for details.

.. toctree::
   :maxdepth: 1

   install

If you didn't click any, and this is your first install: bravo !

Tutorial
--------

Enabling autocompletes inside and outside of the admin has become piece of
cake.

.. toctree::
   :maxdepth: 1

   tutorial

.. _reference:

Reference and design documentation
----------------------------------

If you need anything more than just enabling autocompletes in the admin, then
you should understand django-autocomplete-light's architecture. Because you can
override any part of it.

The architecture is based on 3 main parts which you can override to build
insanely creative features as many users already did.

.. toctree::
   :maxdepth: 1

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
   :maxdepth: 1

   faq


API: find hidden gems
---------------------

.. toctree::
   :maxdepth: 1

   api

Upgrade
-------

Any change is documented in the :doc:`changelog`, so upgrading from a version
to another is always documented there. Usualy, upgrade from pip with a command
like ``pip install -U django-autocomplete-light``. Check the CHANGELOG for BC
(Backward Compatibility) breaks. There should is no backward compatibility for
minor version upgrades ie. from 1.1.3 to 1.1.22, but there *might* be some
minor BC breaks for middle upgrades ie. 1.2.0 to 1.3.0.

v1 to v2
````````

There are major changes between v1 and v2, upgrading has been extensively
documented:

.. toctree::
   :maxdepth: 1

   1to2

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
