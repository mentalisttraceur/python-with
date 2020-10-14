from manual import with_


class ContextManager(object):
    def __init__(self, suppress=False, value=None):
        self.suppress = suppress
        self.value = value
    def __enter__(self):
        print('entering')
        if self.value is None:
            return self
        return self.value
    def __exit__(self, exception_type, exception, traceback):
        print('exiting %r' % (exception,))
        return self.suppress
    def __repr__(self):
        return ('ContextManager(suppress=%r, value=%r)'
                % (self.suppress, self.value))


def action(*args, **kwargs):
    print(args)
    print(kwargs)
    return 'result'


def action_with_error(_):
    raise Exception('some error')


def t1():
    result = with_(ContextManager(), action)
    print(result)

def t2():
    with_(ContextManager(value=42), action)

def t3():
    with_(ContextManager(), lambda _: action(1, 2, a=3, b=4))

def t4():
    with_(ContextManager(), action_with_error)

def t5():
    with_(ContextManager(suppress=True), action_with_error)
