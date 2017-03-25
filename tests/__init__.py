from contextlib import contextmanager
from os import getcwd, chdir


# サンプル１.txt in NFD utf-8
nfd_file_name = b'\xe3\x82\xb5\xe3\x83\xb3\xe3\x83\x95\xe3\x82\x9a\xe3\x83\xab\xef\xbc\x91.txt'


@contextmanager
def push_dir(path):
    cwd = getcwd()
    try:
        chdir(path)
        yield
    finally:
        chdir(cwd)
