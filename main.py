from contextlib import contextmanager
import importlib
import sys


def report(module):
    print('path\n\t{}'.format('\n\t'.join(repr(i) for i in sys.path)))
    print('path_hooks\n\t{}'.format('\n\t'.join(repr(i) for i in sys.path_hooks)))
    print('meta\n\t{}'.format('\n\t'.join(repr(i) for i in sys.meta_path)))
    print('path_cache\n\t{}'.format('\n\t'.join(f'{k}\t->\t{v}' for k, v in sys.path_importer_cache.items())))
    print('\n')

    print('module', repr(module))
    for key in dir(module):
        if key == '__builtins__':
            print(key)
        elif key.startswith('__'):
            print(f'{key} \t {getattr(module, key)}')
    print('\n')


class StubObjects:
    SYS_PATH_IMPORTER_CACHE = {}
    SYS_MODULES = {}


@contextmanager
def switch_to_stub_cache():
    prev_cache = dict(sys.path_importer_cache)
    sys.path_importer_cache.clear()
    sys.path_importer_cache.update(StubObjects.SYS_PATH_IMPORTER_CACHE)

    yield

    StubObjects.SYS_PATH_IMPORTER_CACHE = dict(sys.path_importer_cache)
    sys.path_importer_cache.clear()
    sys.path_importer_cache.update(prev_cache)


@contextmanager
def switch_to_stub_modules():
    prev_cache = dict(sys.modules)
    sys.modules.clear()
    sys.modules['sys'] = prev_cache['sys']  # yeah don't punk that
    sys.modules.update(StubObjects.SYS_MODULES)

    yield

    StubObjects.SYS_MODULES = dict(sys.path_importer_cache)
    sys.modules.clear()
    sys.modules.update(prev_cache)


@contextmanager
def enable_stub_suffix():
    stub_suffix = '.pyi'
    importlib.machinery.SOURCE_SUFFIXES.insert(0, stub_suffix)
    yield
    at_index = importlib.machinery.SOURCE_SUFFIXES.index(stub_suffix)
    del importlib.machinery.SOURCE_SUFFIXES[at_index]


@contextmanager
def disable_cache_usage():
    ext = list(importlib.machinery.BYTECODE_SUFFIXES)
    importlib.machinery.BYTECODE_SUFFIXES.clear()
    importlib.machinery.BYTECODE_SUFFIXES.append('.pyic')
    yield
    importlib.machinery.BYTECODE_SUFFIXES.clear()
    importlib.machinery.BYTECODE_SUFFIXES.extend(ext)


@contextmanager
def load_stub():
    with enable_stub_suffix():
        with switch_to_stub_cache():
            with switch_to_stub_modules():
                with disable_cache_usage():
                    yield


def test_import():
    import magic
    report(magic)
    # noinspection PyUnresolvedReferences
    import typing

    del magic
    del typing


test_import() #

with load_stub():
    test_import()

test_import()
