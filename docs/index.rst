.. Qualia documentation master file, created by
   sphinx-quickstart on Tue Sep 19 16:35:43 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _index:

Welcome to Qualia's documentation!
==================================
:Version: |version|

README
======
.. include:: ../README.md
   :parser: myst_parser.sphinx_

.. toctree::
   :maxdepth: 1
   :caption: User's manual

   Installation
   Update
   User/Usage
   User/ConfigurationFile
   User/Components
   User/MigrationPreviousVersions

.. toctree::
   :maxdepth: 1
   :caption: Developer's manual

   Developer/RepositoryStructure
   Developer/PackageStructure
   Developer/PluginArchitecture
   Developer/Documentation
   Developer/CodeStyleLinter
   Developer/TypeChecking
   Developer/Tests


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
