.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/PFaHT.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/PFaHT
    .. image:: https://readthedocs.org/projects/PFaHT/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://PFaHT.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/PFaHT/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/PFaHT
    .. image:: https://img.shields.io/pypi/v/PFaHT.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/PFaHT/
    .. image:: https://img.shields.io/conda/vn/conda-forge/PFaHT.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/PFaHT
    .. image:: https://pepy.tech/badge/PFaHT/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/PFaHT
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/PFaHT

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

===========
PFaHT Stack
===========

    Python
    Fastapi
    Alpine
    HTMX
    Tailwind

The PFAHT stack is my personal stack for building web applications.
It is a combination of Python, Fastapi, HTMX, and Tailwind.
The stack is designed to be simple, fast, and easy to use.
It is perfect for building web applications that require real-time updates and a
modern look and feel.


Showcase
========

For this project I wanted to be able to build a simple web application that
I can use to input devices and run commands on them.

To keep things simple we will be delaying implementing auth and just focus on
the core functionality.

For the database we will be using a local SQLite database.

Decisions
=========

- Fastapi: Fastapi is a modern web framework for building APIs with Python 3.6+
    based on standard Python type hints.
- HTMX: HTMX allows you to access AJAX, CSS Transitions, WebSockets, and Server
    Sent Events directly in HTML, using attributes, so you can build modern user
    interfaces with the simplicity and power of hypertext.
- Alpine: A minimal framework for giving client side interactions and logic to
    the application with minimal javascript knowledge.
- Tailwind: A utility-first CSS framework for rapidly building custom designs.

HTMX
====

Extensions
----------

So that we can maintain a consistent encoding between our client either using the
swagger endpoint or the html client we will use json and the `json-enc-custom`
extension.

hx-ext='json-enc-custom'

Tailwind
========

Build Process
-------------

Start a process that will watch for changes in your html files defined in the 
tailwind.config.js file, and when there are changes it will update the output.css file.

This file is imported in the layout.html file and is used to style the application.

.. code-block:: bash

    npx tailwindcss \
        -i ./src/pfaht/web/html/static/input.css \
        -o ./src/pfaht/web/html/static/output.css --watch

.. _pyscaffold-notes:



Making Changes & Contributing
=============================

This project uses `pre-commit`_, please make sure to install it before making any
changes::

    pip install pre-commit
    cd PFaHT
    pre-commit install

It is a good idea to update the hooks to the latest version::

    pre-commit autoupdate

Don't forget to tell your contributors to also install and use pre-commit.

.. _pre-commit: https://pre-commit.com/

Note
====

This project has been set up using PyScaffold 4.6. For details and usage
information on PyScaffold see https://pyscaffold.org/.
