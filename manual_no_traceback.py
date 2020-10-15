# Copyright 2019 Alexander Kozhevnikov <mentalisttraceur@gmail.com>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


"""Use context managers with a function instead of a statement.

Provides a minimal and portable interface for using context
managers with all the advantages of functions over syntax.

Note:
    This is the "no traceback" variant, for Python implementations that
    do not support getting the traceback object for an exception. It
    exists to allow code using the ``with_`` interface to gracefully
    degrade in the absence of full traceback support.
"""

__all__ = ('with_',)
__version__ = '1.0.3'


try:
    _BaseException = BaseException
except NameError:
    _BaseException = Exception


def with_(manager, action):
    """Execute an action within the scope of a context manager.

    Arguments:
        manager: The context manager instance to use.
        action: The callable to execute. Must accept the `as` value
            of the context manager as the only positional argument.

    Returns:
        Any: Return value of the executed action.
        None: If the manager suppresses an exception from the action.

    Raises:
        Any: If raised by calling the action and not suppressed by the
            manager, or if raised by the manager, or if the manager
            does not implement the context manager protocol correctly.

    Note:
        This "no traceback" variant always passes ``None`` for the
        ``traceback`` argument to the context manager's ``__exit__``,
        because it is meant for Python implementations that do not
        support getting the traceback object for an exception.
    """
    exit_ = type(manager).__exit__
    value = type(manager).__enter__(manager)
    try:
        result = action(value)
    except _BaseException as exception:  # pylint: disable=broad-except
        if not exit_(manager, type(exception), exception, None):
            raise
        return None
    exit_(manager, None, None, None)
    return result
