Python ``with`` as a Function
=============================

Use context managers with a function instead of a statement.

Provides a minimal and portable interface for using context
managers with all the advantages of functions over syntax.

Allows using context managers on Python implementations that
are too old or too incomplete to have the ``with`` statement.


Versioning
----------

This library's version numbers follow the `SemVer 2.0.0
specification <https://semver.org/spec/v2.0.0.html>`_.


Installation
------------

::

    pip install with-as-a-function


Usage
-----

Import ``with_``, ``iwith``, or both:

.. code:: python

    from with_ import with_, iwith

``with_`` wraps a function in a context manager.
For example,

.. code:: python

    data = with_(open('my_file.txt'), lambda my_file: my_file.read())

is similar to:

.. code:: python

    with open('my_file.txt') as my_file:
        data = my_file.read()

``iwith`` wraps a generator or other iterable in a context manager.
For example,

.. code:: python

    lines = iwith(open('my_file.txt'), lambda my_file: my_file)

is similar to:

.. code:: python

    def _lines():
        with open('my_file.txt') as my_file:
            yield from my_file
    lines = _lines()

And of course because ``with_`` and ``iwith`` are functions, you
can combine them with ``functools.partial`` and other functional
programming libraries and techniques for many more uses.


Portability
-----------

Portable to all releases of Python 3, and releases
of Python 2 starting with 2.2.

*Even those without the* ``with`` *statement and
without the* ``yield from`` *expression.*

For popular Python reimplementations with quirks or bugs that
make the normal implementation of this module not work, other
implementations are included in the source distribution.
