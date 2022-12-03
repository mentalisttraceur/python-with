# Copyright 2019 Alexander Kozhevnikov <mentalisttraceur@gmail.com>
# SPDX-License-Identifier: 0BSD

"""Use context managers with a function instead of a statement.

Provides a minimal and portable interface for using context
managers with all the advantages of functions over syntax.
"""

from sys import exc_info as _exc_info


__all__ = ('with_',)
__version__ = '1.0.9'


class _OldStyleClass:
    pass


_OldStyleClassInstance = type(_OldStyleClass())
del _OldStyleClass


def _type(obj):
    if isinstance(obj, _OldStyleClassInstance):
        return obj.__class__
    return type(obj)


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
    """
    exit_ = _type(manager).__exit__
    value = _type(manager).__enter__(manager)
    try:
        result = action(value)
    except:
        if not exit_(manager, *_exc_info()):
            raise
        return None
    exit_(manager, None, None, None)
    return result
