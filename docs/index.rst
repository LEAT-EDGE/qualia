.. Qualia documentation master file, created by
   sphinx-quickstart
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _index:

Welcome to Qualia's documentation!
=====================================

:Version: |version|



Overview
========
Qualia is an end-to-end framework for training, quantizing, and deploying deep neural networks on embedded devices.



Key Features
============


* **End-to-End Pipeline**: From data preprocessing to embedded deployment, Qualia manages the complete development lifecycle with automated workflows and unified interfaces.

* **Advanced Training**: Built-in support for multiple frameworks, data augmentation, experiment tracking, and automated hyperparameter optimization.

* **Embedded Optimization**: Smart quantization and memory management for resource-constrained devices, with support for various embedded platforms.

* **Developer Tools**: Modular architecture with built-in visualization, debugging utilities, and version control integration.


Benefits
========
Qualia streamlines the development cycle of deep learning models for embedded systems through its integrated pipeline. The framework provides metrics and analysis tools for monitoring model behavior throughout the development process. Its systematic approach to experimentation and logging ensures reproducible results, while offering a structured path from research to embedded deployment.



Technical Specifications
========================

Supported Features
------------------
Qualia's core capabilities include support for multiple frameworks, quantization methods, and deployment targets. The framework provides data augmentation options and allows for custom model architectures. It includes tools for testing, validation, and performance profiling to optimize models for embedded deployment.

Integration Capabilities
------------------------
Qualia integrates with git for version control and experiment tracking. The framework is designed to work with standard data formats and common deep learning frameworks. It supports deployment to various embedded platforms through its flexible deployment system.



Use Cases
=========

Edge AI Development
-------------------
Qualia facilitates deployment of deep learning models to embedded and IoT devices. The framework's optimization tools help manage resource constraints while maintaining model performance. This makes it suitable for embedded vision systems and real-time processing requirements.

Research and Development
------------------------
The framework supports model architecture research and quantization studies through its parameter research capabilities. Researchers can experiment with different architectures and optimization approaches while maintaining a clear path to deployment.


Conclusion
==========
Qualia is more than just a framework - it's a complete solution for bringing deep learning to embedded systems. Whether you're a researcher exploring new architectures, a developer building production systems, or an organization looking to streamline AI deployment, Qualia provides the tools and capabilities you need to succeed.
You may find the datasets and architecture supported in the :doc:`Configuration File Guide <GettingStarted/ConfigurationFile>`


.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   GettingStarted/GettingStarted
   GettingStarted/Installation
   GettingStarted/ConfigurationFile
   GettingStarted/Usage
   GettingStarted/Components
   GettingStarted/MigrationPreviousVersions

.. toctree::
   :maxdepth: 2
   :caption: Plugins

   Plugins/index

.. toctree::
   :maxdepth: 2
   :caption: Developer Guide

   DeveloperGuide/RepositoryStructure
   DeveloperGuide/PackageStructure
   DeveloperGuide/Plugins
   DeveloperGuide/AddDataset
   DeveloperGuide/Documentation
   DeveloperGuide/CodeStyleLinter
   DeveloperGuide/TypeChecking
   DeveloperGuide/Tests

.. toctree::
   :maxdepth: 2
   :caption: Package Management

   PackageManagement/UsingDocker
   PackageManagement/UsingPDM
   PackageManagement/UsingUV
   PackageManagement/Update

.. toctree::
   :maxdepth: 2
   :caption: Project Information

   ProjectInformation/Changelog

Indices and tables
====================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`