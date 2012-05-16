# -*- coding:utf-8 -*-
from __future__ import print_function
import argparse
import getpass
import os
import re
import StringIO
import sys
import zipfile


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
            buffer = StringIO.StringIO()
            _stdout = sys.stdout
            sys.stdout = buffer
            z.printdir()
            sys.stdout = _stdout
            buffer.seek(0)
            print(buffer.read().decode(args.from_).encode(args.to))
            return

        if args.password:
            z.setpassword(args.password)

        for zinfo in z.infolist():
            file_name = zinfo.filename.decode(args.from_).encode(args.to)

            if args.verbose:
                print("Entry:", file_name)

            if args.entries and file_name not in args.entries:
                if args.verbose:
                    print("Not specified:", file_name)
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
                        print("Excluded or not included:", file_name)
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
                    print("Extracting:", file_name)
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
    parser.add_argument('--force', action='store_true',
                        help="Extract file even if its absolute path")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="Verbose mode")
    parser.add_argument('-F', '--from', metavar='ENCODING', dest='from_',
                        required=True,
                        help="Specify filename encoding from")
    parser.add_argument('-T', '--to', metavar='ENCODING',
                        default=sys.getfilesystemencoding(),
                        help="Specify filename encoding to "
                             "(Default sys.getfilesystemencoding())")
    filter_group = parser.add_mutually_exclusive_group()
    filter_group.add_argument('-x', '--exclude',
                              action='append',
                              help="Exclude file pattern in RegExp")
    filter_group.add_argument('-i', '--include',
                              action='append',
                              help="Include file pattern in RegExp")
    args = parser.parse_args(argv[1:])
    for _ in range(3):
        try:
            unzip(args)
            break
        except RuntimeError:
            args.password = getpass.getpass('Password:')
            if args.verbose:
                print("Retrying")
    else:
        print("Failed to unzip", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
