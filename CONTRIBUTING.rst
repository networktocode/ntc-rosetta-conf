CONTRIBUTING
============

All contributions are welcome and even though there are no strict or formal requirements to contribute there are some basic rules contributors need to follow:

1. Make sure your contribution is original and it doesn't violate anybody's copyright
2. Make sure tests pass
3. Make sure your contribution is tested

Below you can find more information depending on what you are trying to contribute, in case of doubt don't hesitate to open a PR with your contribution and ask for help.

Running tests
-------------

To run tests you need ``docker`` and ``GNU Make``. If you meet the requirements all you need to do is execute ``make tests``. All the tests will run inside docker containers you don't need to worry about the environment.

Adding documentation
--------------------

If you want to contribute documentation you need to be sligthly familiar with `sphinx <http://www.sphinx-doc.org/en/stable/>`_ as that's the framework used in this project (and most python projects) to build the documentation.

In addition, if you want to contribute with tutorials or code examples you need to be familiar with `jupyter <https://jupyter.org/>`_. The advantage of using jupyter notebooks over just plain text is that notebooks can be tested. This means code examples and tutorials will be tested by the CI and ensure they stay relevant and work.

The easiest way of working with jupyter is by executing ``make jupyter`` in your local machine and pointing your browser to `http://localhost:8888/notebooks/docs <http://localhost:8888/notebooks/docs>`_. If you are adding a new notebook don't forget to add it to sphinx's documentation.

Coding Style
------------

We use `black <https://github.com/ambv/black>`_ to format the code.

Adding new features
-------------------

New features need to come with tests and a tutorial in the form of a jupyter notebook so it can be tested.

mypy
----

We use `mypy <http://mypy-lang.org/>`_ to bring static typing to our code. This adds some complexity but results in cleaner, less error-prone and more understandable code.
