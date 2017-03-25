# -*- coding:utf-8 -*-
from __future__ import print_function
import argparse
import getpass
import os
import re
from io import StringIO
import sys
import zipfile

from .util import convert


def unzip(args):
    if args.include or args.exclude:
        include = bool(args.include)
        patterns = [re.compile(pattern)
                    for pattern in args.include or args.exclude]
    else:
        include = True
        patterns = None

    with zipfile.ZipFile(args.zip_file) as z:
        if args.list:
            buffer = StringIO()
            _stdout = sys.stdout
            sys.stdout = buffer
            z.printdir()
            sys.stdout = _stdout
            buffer.seek(0)
            print(convert(buffer.read(), args.from_, args.to))
            return

        if args.password:
            z.setpassword(args.password)

        for zinfo in z.infolist():
            file_name = convert(zinfo.filename, args.from_, args.to)

            if args.verbose:
                print("Entry:", file_name, file=sys.stderr)

            if args.entries and file_name not in args.entries:
                if args.verbose:
                    print("Not specified:", file_name, file=sys.stderr)
                continue

            if file_name.startswith(os.sep) and not args.force:
                raise ValueError("Absolute path: %s" % file_name)

            if patterns:
                for pattern in patterns:
                    if pattern.search(file_name):
                        if include:
                            break
                    else:
                        if not include:
                            break
                else:
                    if args.verbose:
                        print("Excluded or not included:", file_name, file=sys.stderr)
                    continue

            # mkdir -p
            dir_name = os.path.dirname(file_name)
            try:
                os.makedirs(dir_name)
            except os.error:
                pass

            if not file_name.endswith(os.sep):
                bin = z.read(zinfo)
                if args.verbose:
                    print("Extracting:", file_name, file=sys.stderr)
                with open(file_name, 'wb') as f:
                    f.write(bin)


def main(argv=sys.argv):
    parser = argparse.ArgumentParser(
                        description="Unzipper for not native encoded filename file")
    parser.add_argument('zip_file', metavar='ZIP_FILE',
                        help="ZIP archive")
    parser.add_argument('entries', nargs='*', metavar='ENTRY',
                        help="can specify file entries")
    parser.add_argument('-l', '--list', action='store_true',
                        help="list entries instead of extracting")
    parser.add_argument('-P', '--password',
                        help="password for encrypted")
    parser.add_argument('--force', action='store_true',
                        help="extract file even if its absolute path")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="verbose mode")
    parser.add_argument('-F', '--from', metavar='ENCODING', dest='from_',
                        required=True,
                        help="filename encoding from")
    parser.add_argument('-T', '--to', metavar='ENCODING',
                        default=sys.getfilesystemencoding(),
                        help="filename encoding to(Default sys.getfilesystemencoding())")
    filter_group = parser.add_mutually_exclusive_group()
    filter_group.add_argument('-x', '--exclude',
                              action='append',
                              help="exclude filename pattern in RegExp")
    filter_group.add_argument('-i', '--include',
                              action='append',
                              help="include filename pattern in RegExp")
    args = parser.parse_args(argv[1:])
    for _ in range(3):
        try:
            unzip(args)
            break
        except RuntimeError:
            args.password = getpass.getpass('Password:')
            if args.verbose:
                print("Retrying", file=sys.stderr)
    else:
        print("Failed to unzip", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
