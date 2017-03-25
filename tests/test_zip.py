from os import walk
from os.path import abspath
from tempfile import TemporaryDirectory
from zipe.unzip import unzip, UnzipContext
from zipe.zip import zip_, ZipContext
from . import nfd_file_name, push_dir


def test_zip():
    unzip_context = UnzipContext()
    unzip_context.password = 'password'
    unzip_context.from_ = 'cp932'
    zip_context = ZipContext()
    zip_context.recursive = True
    zip_context.to = 'cp932'
    zipfile_path = abspath("tests/data/こんにちは.zip")
    expected_part1 = 'こんにちは.txt'
    expected_part2 = nfd_file_name
    new_zipfile_name = 'hello.zip'

    with TemporaryDirectory() as temp_dir, push_dir(temp_dir):
        unzip(unzip_context, zipfile_path)
        zip_(zip_context, new_zipfile_name, ['.'])
        new_zipfile_path = abspath(new_zipfile_name)
        with TemporaryDirectory() as temp_dir2, push_dir(temp_dir2):
            unzip(unzip_context, new_zipfile_path)
            actual = list(walk(temp_dir))[1][2]
            actual_in_encoded = [s.encode() for s in actual]
            assert expected_part1 in actual
            assert expected_part2 in actual_in_encoded, \
                "expected: %s, actual: %s" % (expected_part2, actual_in_encoded)
