# SPDX-License-Identifier: 0BSD
# Copyright 2019 Alexander Kozhevnikov <mentalisttraceur@gmail.com>

"""Use context managers with a function instead of a statement.

Provides a minimal and portable interface for using context
managers with all the advantages of functions over syntax.
"""

__all__ = ('with_', 'iwith')
__version__ = '1.1.0'


def with_(manager, action):
    """Execute an action within the scope of a context manager.

    Arguments:
        manager: The context manager instance to use.
        action: The callable to execute. Must accept the ``as`` value
            of the context manager as the only positional argument.

    Returns:
        Any: Return value of the executed action.
        None: If the manager suppresses an exception from the action.

    Raises:
        Any: If raised by calling the action and not suppressed by the
            manager, or if raised by the manager, or if the manager
            does not implement the context manager protocol correctly.
    """
    with manager as value:
        return action(value)
    return None


def iwith(manager, action):
    """Iterate within the scope of a context manager.

    Arguments:
        manager: The context manager instance to use.
        action: The callable to execute to get an iterator. Must
            accept the ``as`` value of the context manager as
            the only positional argument and return an iterable.

    Yields:
        Any: Values from the iterable returned by the action.

    Returns:
        Any: The value "returned" inside the StopIteration exception
            that is raised once the iterable's iterator is exhausted.
        None: If the manager suppresses an exception from the iteration.

    Raises:
        Any: If raised by calling the action or while iterating and
            not suppressed by the manager, or if raised by the manager,
            or if the manager does not implement the context manager
            protocol correctly, or if raised while yielding values
            from and delegating to the iterable returned by the action.
    """
    with manager as value:
        return (yield from action(value))
    return None
