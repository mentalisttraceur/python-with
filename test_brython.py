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


__name__ = '__main__'
_with_list = [with_]
_iwith_list = [iwith]


try:
    _BaseException = BaseException
except NameError:
    _BaseException = Exception


def _raise(exception):
    raise exception


class _ContextManager(object):
    def __init__(self, suppress, thing):
        self.suppress = suppress
        self.thing = thing

    def __enter__(self):
        self.thing.entered = 'entered'
        return self.thing

    def __exit__(self, t, e, tb):
        self.thing.exited = 'exited'
        return self.suppress


class _Iterator(object):
    def __init__(self, thing):
        self.thing = thing
    def __iter__(self):
        self.thing.iteratored = 'iteratored'
        return self
    def __next__(self):
        self.thing.iterated = 'iterated'
        return self.thing


class _Closable(_Iterator):
    def close(self):
        self.thing.closed = 'closed'


class ObjectWithAttributes(object):
    pass


def _test(test_function, with_list):
    for with_ in with_list:
        print(test_function.__name__ + ' ' + with_.__module__)
        test_function(with_)


def _test_return(with_):
    nonce = ObjectWithAttributes()
    result = with_(_ContextManager(False, nonce), lambda x: x)
    assert result is nonce
    assert nonce.entered == 'entered'
    assert nonce.exited == 'exited'


def test_return():
    _test(_test_return, _with_list)


def _test_raise(with_):
    exception = Exception('fail')
    try:
        with_(_ContextManager(False, exception), _raise)
    except _BaseException as e_:
        e = e_
    assert e is exception
    assert exception.entered == 'entered'
    assert exception.exited == 'exited'


def test_raise():
    _test(_test_raise, _with_list)


def _test_suppress(with_):
    exception = Exception('fail')
    none = with_(_ContextManager(True, exception), _raise)
    assert none is None
    assert exception.entered == 'entered'
    assert exception.exited == 'exited'


def test_suppress():
    _test(_test_suppress, _with_list)


def _test_iterate(iwith):
    nonce = ObjectWithAttributes()
    def generator(x):
        yield x
        yield x
        yield x
    iterator = iwith(_ContextManager(False, nonce), generator)
    result = list(iterator)
    assert len(result) == 3
    assert result[0] is nonce
    assert result[1] is nonce
    assert result[2] is nonce
    assert nonce.entered == 'entered'
    assert nonce.exited == 'exited'


def test_iterate():
    _test(_test_iterate, _iwith_list)


def _test_iterate_empty(iwith):
    nonce = ObjectWithAttributes()
    iterator = iwith(_ContextManager(False, nonce), lambda x: ())
    result = list(iterator)
    assert result == []
    assert nonce.entered == 'entered'
    assert nonce.exited == 'exited'


def test_iterate_empty():
    _test(_test_iterate_empty, _iwith_list)


def _test_send(iwith):
    nonce = ObjectWithAttributes()
    def generator(x):
        yield (yield x)
    iterator = iwith(_ContextManager(False, nonce), generator)
    first = next(iterator)
    second = iterator.send(42)
    rest = list(iterator)
    assert first is nonce
    assert second == 42
    assert rest == []
    assert nonce.entered == 'entered'
    assert nonce.exited == 'exited'


def test_send():
    _test(_test_send, _iwith_list)


def _test_send_prematurely(iwith):
    nonce = ObjectWithAttributes()
    def generator(x):
        yield x

    # Standard Python behavior is to raise here, but Brython treats
    # premature sends as `iterator.send(None)` / `next(iterator)`,
    # so this try block detects which kind of behavior to expect:
    try:
        generator(None).send(57)
    except TypeError:
        should_raise = True
    else:
        should_raise = False

    iterator = iwith(_ContextManager(False, nonce), generator)
    try:
        value = iterator.send(57)
    except TypeError:
        if not should_raise:
            assert False, 'iterator.send() should not have raised'
        result = list(iterator)
    else:
        if should_raise:
            assert False, 'iterator.send() should have raised'
        result = [value] + list(iterator)
    assert result == [nonce]
    assert nonce.entered == 'entered'
    assert nonce.exited == 'exited'


def test_send_prematurely():
    _test(_test_send_prematurely, _iwith_list)


def _test_send_none_prematurely(iwith):
    nonce = ObjectWithAttributes()
    def generator(x):
        yield x
    iterator = iwith(_ContextManager(False, nonce), generator)
    result = iterator.send(None)
    rest = list(iterator)
    assert result is nonce
    assert rest == []
    assert nonce.entered == 'entered'
    assert nonce.exited == 'exited'


def test_send_none_prematurely():
    _test(_test_send_none_prematurely, _iwith_list)


def _test_throw(iwith):
    nonce = ObjectWithAttributes()
    def generator(x):
        yield x
    iterator = iwith(_ContextManager(False, nonce), generator)
    


def test_throw():
    _test(_test_throw, _iwith_list)


if __name__ == '__main__':
    test_return()
    test_raise()
    test_suppress()
    test_iterate()
    test_iterate_empty()
    test_send()
    test_send_prematurely()
    test_send_none_prematurely()
    #test_send_none()
