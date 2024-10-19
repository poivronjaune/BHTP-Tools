.. BHTP documentation master file, created by
   sphinx-quickstart on Tue Oct 15 21:40:12 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

BHTP documentation
===================

**B**\rothers **H**\obby **T**\rading **P**\latform is a python package to help hobbyist implement trading strategies for fun.

Installation
^^^^^^^^^^^^^

::

   pip install git+https://github.com/poivronjaune/BHTP-Tools.git

.. note::
   If running in `Google Colab`_ use  

   ::

   !pip install git+https://github.com/poivronjaune/BHTP-Tools.git

.. _Google Colab: https://colab.research.google.com/


Test installation 
^^^^^^
Once installed open a Python REPL and

::

   >>> import bhtp
   >>> print(bhtp.get_version())


.. toctree::
   :maxdepth: 2

   bhtp
   github
