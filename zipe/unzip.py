# -*- coding:utf-8 -*-
from __future__ import print_function
import argparse
import getpass
import os
import sys
import zipfile


def unzip(args):
    with zipfile.ZipFile(args.zip_file) as z:
        if args.password:
            z.setpassword(args.password)

        for zinfo in z.infolist():
            file_name = zinfo.filename.decode(args.from_).encode(args.to)

            if args.list:
                print("%d\t%d/%d/%d %d:%d:%d\t%s" %
                      ((zinfo.file_size,) + zinfo.date_time + (file_name,)))
                continue

            if args.entries and file_name not in args.entries:
                continue

            # mkdir -p
            dir_name = os.path.dirname(file_name)
            try:
                os.makedirs(dir_name)
            except os.error:
                pass

            if not file_name.endswith('/'):
                bin = z.read(zinfo)
                with open(file_name, 'wb') as f:
                    f.write(bin)


def main(argv=sys.argv):
    parser = argparse.ArgumentParser(
                        description="Unzipper for not native filename")
    parser.add_argument('zip_file', metavar='ZIP_FILE',
                        help="The ZIP archive")
    parser.add_argument('entries', nargs='*', metavar='ENTRY',
                        help="Specify file entries in the archive to extract")
    parser.add_argument('-l', '--list', action='store_true',
                        help="List entries instead of extracting")
    parser.add_argument('-P', '--password',
                        help="Enter password for encrypted")
    parser.add_argument('-F', '--from', metavar='ENCODING', dest='from_',
                        required=True,
                        help="Specify filename encoding from")
    parser.add_argument('-T', '--to', metavar='ENCODING',
                        default=sys.getfilesystemencoding(),
                        help="Specify filename encoding to "
                             "(Default sys.getfilesystemencoding())")
    args = parser.parse_args(argv[1:])
    for _ in range(3):
        try:
            unzip(args)
            break
        except RuntimeError:
            args.password = getpass.getpass('password:')
    else:
        print("Failed to unzip", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
