"""
Utility functions and objects to ease Python 3 compatibility.
Contributed to rdflib 3 by Thomas Kluyver, re-used here.
"""
import sys

try:
    from functools import wraps as wraps_py3
    wraps = wraps_py3
except ImportError:
    # No-op wraps decorator
    def wraps_py2(f):
        def dec(newf):
            return newf
        return dec
    wraps = wraps_py2


def cast_bytes(s, enc='utf-8'):
    if isinstance(s, unicode):
        return s.encode(enc)
    return s

PY3 = (sys.version_info[0] >= 3)


def _modify_str_or_docstring(str_change_func):
    @wraps(str_change_func)
    def wrapper(func_or_str):
        if isinstance(func_or_str, str):
            func = None
            doc = func_or_str
        else:
            func = func_or_str
            doc = func.__doc__

        doc = str_change_func(doc)

        if func:
            func.__doc__ = doc
            return func
        return doc
    return wrapper

if PY3:
    # Python 3:
    # ---------
    def b_py3(s):
        return s.encode('ascii')

    bytestype = bytes

    # Abstract u'abc' syntax:
    @_modify_str_or_docstring
    def format_doctest_out_py3(s):
        """Python 2 version
        "%(u)s'abc'" --> "'abc'"
        "%(b)s'abc'" --> "b'abc'"
        "55%(L)s"    --> "55"

        Accepts a string or a function, so it can be used as a decorator."""
        return s % {'u': '', 'b': 'b', 'L': ''}

    def type_cmp_py3(a, b):
        """Python 2 style comparison based on type"""
        ta, tb = type(a).__name__, type(b).__name__
        # Ugly hack: some tests rely on tuple sorting before unicode, and I
        # don't know if that's important. Better retain it for now.
        if ta == 'str':
            ta = 'unicode'
        if tb == 'str':
            tb = 'unicode'
        # return 1 if ta > tb else -1 if ta < tb else 0
        if ta > tb:
            return 1
        elif ta < tb:
            return -1
        else:
            return 0
    b = b_py3
    format_doctest_out = format_doctest_out_py3
    type_cmp = type_cmp_py3
else:
    # Python 2
    # --------
    def b_py2(s):
        return s

    bytestype = str

    # Abstract u'abc' syntax:
    @_modify_str_or_docstring
    def format_doctest_out_py2(s):
        """Python 2 version
        "%(u)s'abc'" --> "u'abc'"
        "%(b)s'abc'" --> "'abc'"
        "55%(L)s"    --> "55L"

        Accepts a string or a function, so it can be used as a decorator."""
        return s % {'u': 'u', 'b': '', 'L': 'L'}

    def type_cmp_py2(a, b):
        # return 1 if a > b else -1 if a < b else 0
        if a > b:
            return 1
        elif a < b:
            return -1
        else:
            return 0
    b = b_py2
    format_doctest_out = format_doctest_out_py2
    type_cmp = type_cmp_py2
