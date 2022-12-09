// SPDX-License-Identifier: 0BSD
// Copyright 2022 Alexander Kozhevnikov <mentalisttraceur@gmail.com>

// This is an implementation of the `with_` module for Transcrypt.
// It has a more thoroughly correct and compatible implementation
// of `with` behavior than Transcrypt has as of 2022-12-09, while
// keeping with Transcrypt's spirit of native JavaScript speed.

// Key differences from the Python version:
//
// 1. `iwith` is a native JavaScript generator function, so:
//    * its `.throw` only takes one argument,
//    * it does not have `.send` (use `.next(value)` instead),
//    * it does not have `.close` (use `.return()` instead),
//    * if it is iterated on with `for(... of ...)`, it is
//      automatically closed when the loop is exited, and
//    * `GeneratorExit` is not thrown into it when closing.
// 2. `__enter__` and `__exit__` are looked up on the
//    context manager itself, rather than on its type.

import {py_typeof, tuple} from './org.transcrypt.__runtime__.js'

export const __all__ = tuple(['with_', 'iwith'])
export const __version__ = '1.1.0'

export function with_(manager, action)
{
    const exit = manager.__exit__.bind(manager)
    const value = manager.__enter__()
    try
    {
        var result = action(value)
    }
    catch(thrown)
    {
        if(!(exit(py_typeof(thrown), thrown, null)))
        {
            throw thrown
        }
        return null
    }
    exit(null, null, null)
    return result
}

export function* iwith(manager, action)
{
    const exit = manager.__exit__.bind(manager)
    const value = manager.__enter__()
    var caught = false
    try
    {
        var result = yield* action(value)
    }
    catch(thrown)
    {
        caught = true
        if(!(exit(py_typeof(thrown), thrown, null)))
        {
            throw thrown
        }
        return null
    }
    finally
    {
        if(!(caught))
        {
            exit(null, null, null)
        }
    }
    return result
}
