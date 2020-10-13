Python ``with`` as a Function
=============================

Use context managers with a function instead of a statement.

Provides a minimal, clean and portable interface for using context
managers with all the advantages of functions over syntax.


Why
---

Because context managers are awesome, but currently can't be used in
as many places as I would like, and this is the first step towards
making that possible with less boilerplate and more portability.


Versioning
----------

This library's version numbers follow the `SemVer 2.0.0 specification
<https://semver.org/spec/v2.0.0.html>`_.

The current version number is available in the variable ``__version__``
as is normal for Python modules.


Installation
------------

::

    pip install with-as-a-function


Usage
-----

The ``with_`` function implements the raw basic logic of executing a
context manager as described in PEP-343:

.. code:: python

    from with_ import with_

With it we can do things like this:

.. code:: python

    data = with_(open('my_file.txt'), lambda my_file: my_file.read(4096))

Which is equivalent to:

.. code:: python

    with open('my_file.txt') as my_file:
        data = my_file.read(4096)

You can think of it as being functionally equivalent to:

.. code:: python

    def with_(manager, action):
        with manager as value:
            return action(value)
        return None

except that it's also portable to Python implementations and versions
that don't support the ``with`` statement.


Portability
-----------

Portable to all releases of both Python 3 and Python 2.

*Even those without the* ``with`` *statement.*

(The oldest tested is 2.5, but it will likely work on all Python 2
versions and probably on even earlier versions.)

For Python implementations that do not support ``sys.exc_info``, a
"no traceback" variant can be installed manually, by grabbing the
``with_no_traceback.py`` file and saving it *as* ``with_.py``.
(Saving it as ``with_.py`` has the advantage that your code can just do
``from with_ import with_`` and it'll just work consistently, without
version-detecting boilerplate.)

You are of course welcome to just copy-paste the tiny ``with_``
function definition into your code.
