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

Import ``with_``:

.. code:: python

    from with_ import with_

With it we can do things like this:

.. code:: python

    data = with_(open('my_file.txt'), lambda my_file: my_file.read())

Which is similar to:

.. code:: python

    with open('my_file.txt') as my_file:
        data = my_file.read()

And of course because ``with_`` is a function, you can combine
it with ``functools.partial`` and other functional programming
libraries and techniques for many more uses.


Portability
-----------

Portable to all releases of both Python 3 and Python 2.

*Even those without the* ``with`` *statement.*

(The oldest tested is 2.5, but it will likely work on all
Python 2 versions and probably on even earlier versions.)

For Python implementations that neither support the ``with``
statement nor have ``sys.exc_info``, a "no traceback" variant
is included in the source that can be installed manually.
