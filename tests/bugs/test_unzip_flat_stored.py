from os import walk
from os.path import abspath
from tempfile import TemporaryDirectory
from zipe.unzip import unzip, UnzipContext
from zipe.zip import zip_, ZipContext
from .. import push_dir


def test_zip():
    unzip_context = UnzipContext()
    unzip_context.password = 'password'
    unzip_context.from_ = 'utf-8'
    zip_context = ZipContext()
    zip_context.recursive = True
    zip_context.to = 'utf-8'

    filename = 'foo.txt'
    zipfile_name = 'archive.zip'

    with TemporaryDirectory() as temp_dir, push_dir(temp_dir):
        with open(filename, 'w') as f:
            pass
        zip_(zip_context, zipfile_name, ['.'])
        zipfile_path = abspath(zipfile_name)
        with TemporaryDirectory() as temp_dir2, push_dir(temp_dir2):
            unzip(unzip_context, zipfile_path)
            actual = list(walk(temp_dir2))[0][2]
            assert filename in actual
