# -*- coding:utf-8 -*-
from __future__ import print_function
import argparse
import os
import sys
import zipfile


def zip_(args):
    if args.recursive:
        entries = []
        for root_entry in args.entries:
            for directory, _, files in os.walk(root_entry):
                entries.append(directory)
                entries.extend([os.path.join(directory, f)
                                for f in files])
        args.entries = entries

    with zipfile.ZipFile(args.zip_file, 'a') as z:
        if args.password:
            z.setpassword(args.password)

        for entry in args.entries:
            arcname = entry.decode(args.from_).encode(args.to)
            z.write(entry, arcname)


def main(argv=sys.argv):
    parser = argparse.ArgumentParser(
                        description="Zipper for not native filename")
    parser.add_argument('zip_file', metavar='ZIP_FILE',
                        help="The ZIP archive")
    parser.add_argument('entries', nargs='+', metavar='ENTRY',
                        help="Specify file entries in the archive to extract")
    parser.add_argument('-P', '--password',
                        help="Enter password for encrypted")
    parser.add_argument('-F', '--from', metavar='ENCODING', dest='from_',
                        default=sys.getfilesystemencoding(),
                        help="Specify filename encoding from"
                             "(Default sys.getfilesystemencoding())")
    parser.add_argument('-T', '--to', metavar='ENCODING',
                        required=True,
                        help="Specify filename encoding to ")
    parser.add_argument('-r', '--recursive',
                        action='store_true',
                        help="Archive recursively")
    args = parser.parse_args(argv[1:])
    zip_(args)


if __name__ == '__main__':
    main()
