# SPDX-License-Identifier: 0BSD
# Copyright 2019 Alexander Kozhevnikov <mentalisttraceur@gmail.com>

"""Use context managers with a function instead of a statement.

Provides a minimal and portable interface for using context
managers with all the advantages of functions over syntax.
"""

# This is an implementation of the `with_` module for Skulpt.
# As of 2022-12-09, Skulpt lacks bidirectional generators.
# Older versions of Skulpt also lacked `with` entirely, and
# then had bugs like running context manager `__exit__` more
# than once on exit.

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

    Note:
        This variant of ``with_`` always passes ``None`` for the
        traceback argument to the context manager's ``__exit__``,
        because it is meant for a Python implementation that does
        not support getting the traceback object for an exception.
    """
    exit_ = type(manager).__exit__
    value = type(manager).__enter__(manager)
    try:
        result = action(value)
    except BaseException as exception:
        if not exit_(manager, type(exception), exception, None):
            raise
        return None
    exit_(manager, None, None, None)
    return result


def _next(iterator):
    return type(iterator).__next__(iterator)


try:
    _GeneratorExit = GeneratorExit
except NameError:
    class _GeneratorExit(BaseException):
        pass


class iwith(object):
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

    Note:
        This variant of ``with_`` always passes ``None`` for the
        traceback argument to the context manager's ``__exit__``,
        because it is meant for a Python implementation that does
        not support getting the traceback object for an exception.
    """
    __slots__ = (
        '_yielded', '_closed',
        '_iterator',
        '_manager', '_action', '_exit',
        '__weakref__',
    )

    def __init__(self, manager, action):
        self._yielded = False
        self._closed = False
        self._iterator = None
        self._manager = manager
        self._action = action

    def __iter__(self):
        return self

    def _enter(self):
        manager = self._manager
        exit_ = type(manager).__exit__
        self._exit = exit_
        value = type(manager).__enter__(manager)
        try:
            self._iterator = iter(self._action(value))
        except BaseException as exception:
            if not exit_(manager, type(exception), exception, None):
                raise
            raise StopIteration

    def __next__(self):
        if self._closed:
            raise StopIteration
        try:
            if not self._yielded:
                self._enter()
            try:
                result = _next(self._iterator)
            except StopIteration:
                self._exit(self._manager, None, None, None)
                raise
            except BaseException as exception:
                if not self._exit(self._manager, type(exception), exception, None):
                    raise
                raise StopIteration
        except:
            self._closed = True
            raise
        self._yielded = True
        return result

    def send(self, value):
        if self._closed:
            raise StopIteration
        if value is not None and not self._yielded:
            raise TypeError("can't send non-None value to a just-started generator")
        try:
            if not self._yielded:
                self._enter()
            try:
                if value is not None:
                    result = self._iterator.send(value)
                else:
                    result = _next(self._iterator)
            except StopIteration:
                self._exit(self._manager, None, None, None)
                raise
            except BaseException as exception:
                if not self._exit(self._manager, type(exception), exception, None):
                    raise
                raise StopIteration
        except:
            self._closed = True
            raise
        self._yielded = True
        return result

    def throw(self, exception, value=None, traceback=None):
        if self._yielded and not self._closed:
            try:
                if _is_generator_exit(exception):
                    try:
                        close = self._iterator.close
                    except AttributeError:
                        _raise(exception, value)
                    close()
                    _raise(exception, value)
                try:
                    throw = self._iterator.throw
                except AttributeError:
                    _raise(exception, value)
            except BaseException as exception:
                self._closed = True
                if not self._exit(self._manager, type(exception), exception, None):
                    raise
                raise StopIteration
            try:
                return throw(exception, value, traceback)
            except StopIteration:
                self._closed = True
                self._exit(self._manager, None, None, None)
                raise
            except BaseException as exception:
                self._closed = True
                if not self._exit(self._manager, type(exception), exception, None):
                    raise
                raise StopIteration
        self._closed = True
        _raise(exception, value)

    def close(self):
        if not self._yielded:
            self._closed = True
        if not self._closed:
            try:
                self.throw(_GeneratorExit)
            except (_GeneratorExit, StopIteration):
                return
            self._closed = True
            raise RuntimeError('generator ignored GeneratorExit')


def _is_generator_exit(exception):
    if isinstance(exception, _GeneratorExit):
        return True
    try:
        return issubclass(exception, _GeneratorExit)
    except TypeError:
        return False


def _raise(exception, value):
    if isinstance(exception, BaseException):
        if value is not None:
            raise TypeError('instance exception may not have a separate value')
    elif (not isinstance(exception, type)
    or    not issubclass(exception, BaseException)):
        raise TypeError('exceptions must derive from BaseException')
    elif not isinstance(value, exception):
        if value is None:
            exception = exception()
        elif isinstance(value, tuple):
            exception = exception(*value)
        else:
            exception = exception(value)
    raise exception
