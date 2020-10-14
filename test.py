import sys

from raise_ import raise_
import manual


class ContextManager(object):
    def __init__(self, suppress, thing):
        self.suppress = suppress
        self.thing = thing

    def __enter__(self):
        self.thing.entered = 'entered'
        return self.thing

    def __exit__(self, t, e, tb):
        self.thing.exited = 'exited'
        return self.suppress


class ObjectWithAttributes(object): pass


def _test_normal(with_):
    nonce = ObjectWithAttributes()
    result = with_(ContextManager(False, nonce), lambda x: x)
    assert nonce is result
    assert nonce.entered == 'entered'
    assert nonce.exited == 'exited'


def test_normal():
    _test_normal(manual.with_)


def _test_raise(with_):
    exception = Exception('fail')
    try:
        with_(ContextManager(False, exception), raise_)
    except:
        _, e, _ = sys.exc_info()
    assert e is exception
    assert exception.entered == 'entered'
    assert exception.exited == 'exited'


def test_raise():
    _test_raise(manual.with_)


def _test_suppress(with_):
    exception = Exception('fail')
    none = with_(ContextManager(True, exception), raise_)
    assert none is None
    assert exception.entered == 'entered'
    assert exception.exited == 'exited'


def test_suppress():
    _test_suppress(manual.with_)


if __name__ == '__main__':
    test_normal()
    test_raise()
    test_suppress()
