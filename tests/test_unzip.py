from os import walk
from os.path import abspath, basename
import sys
from tempfile import TemporaryDirectory
from zipe.unzip import unzip, unzip_list, UnzipContext
from . import nfc_file_name, nfd_file_name, push_dir


def test_unzip_list():
    context = UnzipContext()
    context.from_ = 'cp932'
    expected_part1 = 'こんにちは.txt'
    if sys.platform == 'darwin':
        expected_part2 = nfd_file_name.decode('utf8')
    else:
        expected_part2 = nfc_file_name.decode('utf8')
    actual = unzip_list(context, 'tests/data/こんにちは.zip')

    assert expected_part1 in actual
    assert expected_part2 in actual


def test_unzip():
    context = UnzipContext()
    context.password = 'password'
    context.from_ = 'cp932'
    expected_part1 = 'こんにちは.txt'
    if sys.platform == 'darwin':
        expected_part2 = nfd_file_name
    else:
        expected_part2 = nfc_file_name
    zipfile_path = abspath('tests/data/こんにちは.zip')

    with TemporaryDirectory() as temp_dir, push_dir(temp_dir):
        unzip(context, zipfile_path)
        actual = list(walk(temp_dir))[1][2]
        actual_in_encoded = [s.encode() for s in actual]
        assert expected_part1 in actual
        assert expected_part2 in actual_in_encoded,\
            "expected: %s, actual: %s" % (expected_part2, actual_in_encoded)


def test_entries():
    context = UnzipContext()
    context.password = 'password'
    context.from_ = 'cp932'
    target_path = 'こんにちは/こんにちは.txt'
    expected = basename(target_path)
    zipfile_path = abspath('tests/data/こんにちは.zip')

    with TemporaryDirectory() as temp_dir, push_dir(temp_dir):
        unzip(context, zipfile_path, entries=[target_path])
        actual = list(walk(temp_dir))[1][2]
        assert [expected] == actual


def test_include():
    context = UnzipContext()
    context.password = 'password'
    context.from_ = 'cp932'
    context.include_patterns = ['.*こんにちは\.txt']
    expected = 'こんにちは.txt'
    zipfile_path = abspath('tests/data/こんにちは.zip')

    with TemporaryDirectory() as temp_dir, push_dir(temp_dir):
        unzip(context, zipfile_path)
        actual = list(walk(temp_dir))[1][2]
        assert [expected] == actual


def test_exclude():
    context = UnzipContext()
    context.password = 'password'
    context.from_ = 'cp932'
    context.exclude_patterns = ['.*こんにちは\.txt']
    if sys.platform == 'darwin':
        expected = nfd_file_name.decode('utf8')
    else:
        expected = nfc_file_name.decode('utf8')
    zipfile_path = abspath('tests/data/こんにちは.zip')

    with TemporaryDirectory() as temp_dir, push_dir(temp_dir):
        unzip(context, zipfile_path)
        actual = list(walk(temp_dir))[1][2]
        assert [expected] == actual
