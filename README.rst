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
context manager as described in PEP-0343:

.. code:: python

    from with_ import with_

With it we can do things like this:

.. code:: python

    data = with_(open('my_file.txt'), lambda my_file: my_file.read(4096))

Which is equivalent to:

.. code:: python

    with open('my_file.txt) as my_file:
        data = my_file.read(4096)

You can think of it as being functionally equivalent to:

.. code:: python

    def with_(manager, action)
        with manager as value:
            return action(value)

except that it's also portable to Python implementations and versions
that don't support the ``with`` statement.


Portability
-----------

Portable to all releases of both Python 3 and Python 2.

(The oldest tested is 2.5, **without** importing ``with_statement``
from ``__future__``, but it will likely work on all Python 2 versions
probably on even earlier versions.)

For Python implementations that do not support ``sys.exc_info``, a
"no traceback" variant can be installed manually, by grabbing the
``with_no_traceback.py`` file and saving it *as* ``with_.py``.
(Saving it as the ``with_.py`` has the advantage that your code can
just do ``from with_ import with_`` and it'll just work consistently,
without version-detecting boilerplate.)

You are of course welcome to just copy-paste the tiny ``with_``
function definition into your code.


Design Decisions
----------------

* Not exposing anything special to support the equivalent of wrapping
  ``yield from`` and ``yield`` within ``with`` blocks, because that is
  a more complex problem, and I want to have more experience seeing
  those usecases before I start committing to an interface.

* Not using ``finally`` as the reference code in PEP-343 does because
  the only purpose of the ``finally`` was to catch escaping statements
  like ``return``, ``break``, and ``continue``. Since we use a single
  function instead of a "suite" of code, those cannot happen.

* Not using an ``else`` clause for the clean exit variant, because the
  code is still equally clear without it, and arguably is even clearer
  because it's the same number of lines but code paths terminate faster.

* Also not using either ``else`` or ``finally`` because of "portability
  conservatism": the principle that when portability matters, it is
  safer to bet on the most conservative feature-set possible. You'd
  think every pragmatically usable Python implementation would get
  ``try`` block ``else`` and ``finally`` clauses right, but it turns out
  no, some don't.

  If it made a big difference in code clarity or correness, I would be
  reticent to consider this a sufficient reason by itself, but it is a
  factor worth considering.