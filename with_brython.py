# SPDX-License-Identifier: 0BSD
# Copyright 2019 Alexander Kozhevnikov <mentalisttraceur@gmail.com>

"""Use context managers with a function instead of a statement.

Provides a minimal and portable interface for using context
managers with all the advantages of functions over syntax.
"""

# This is an implementation of the `with_` module for Brython.
# As of 2022-12-09, Brython had partially broken ``yield from``.
# This variant is a stopgap until that's fixed, relying only
# on ``with`` and bidirectional ``yield``.

from sys import exc_info as _exc_info


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
        iterator = iter(action(value))
        sent = None
        thrown = None
        while True:
            try:
                if thrown is not None:
                    value = throw(*thrown)
                elif sent is not None:
                    value = iterator.send(sent)
                else:
                    value = next(iterator)
            except StopIteration as stop:
                return stop.value
            sent = None
            thrown = None
            try:
                sent = yield value
            except GeneratorExit:
                try:
                    close = iterator.close
                except AttributeError:
                    close = None
                if close is not None:
                    try:
                        close()
                    except BaseException as exception:
                        try:
                            exception.__context__ = None
                        except AttributeError:
                            pass
                        raise
                raise
            except:
                try:
                    throw = iterator.throw
                except AttributeError:
                    throw = None
                if throw is None:
                    raise
                thrown = _exc_info()
    return None
