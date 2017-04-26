import argparse
import getpass
import os
from io import StringIO
import sys
import zipfile

from .util import Context


class UnzipContext(Context):
    to = sys.getfilesystemencoding()
    force = False

    def is_safe_path(self, path):
        if not path.startswith(os.sep):
            return True
        if self.force:
            return True
        return False


def unzip_list(context, zip_file):
    with zipfile.ZipFile(zip_file) as z:
        buffer = StringIO()
        z.printdir(file=buffer)
        return context.convert_zip_str_to_str(buffer.getvalue())


def unzip(context, zip_file, entries=None):
    with context.wrap(zipfile.ZipFile(zip_file)) as z:
        for zinfo in z.infolist():
            file_name = context.convert_zip_str_to_str(zinfo.filename)
            context.log("Entry: %s" % file_name)

            if entries and file_name not in entries:
                context.log("Not specified: %s" % file_name)
                continue

            if not context.is_safe_path(file_name):
                raise ValueError("May be dangerous path in ZIP: %s" % file_name)

            if not context.is_target(file_name):
                context.log("Skipping: %s" % file_name)
                continue

            # mkdir -p
            dirname = os.path.dirname(file_name)
            if dirname:
                os.makedirs(dirname, exist_ok=True)

            if not file_name.endswith(os.sep):
                bin = z.read(zinfo)
                context.log("Extracting: %s" % file_name)
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

    context = UnzipContext()
    context.verbose = args.verbose
    context.force = args.force
    context.from_ = args.from_
    context.to = args.to
    context.exclude_patterns = args.exclude
    context.include_patterns = args.include
    context.password = args.password

    # list mode
    if args.list:
        print(unzip_list(context, args.zip_file))
        return

    # unzip mode
    for _ in range(3):
        try:
            unzip(context, args.zip_file)
            break
        except RuntimeError:
            context.password = getpass.getpass('Password:')
            context.log("Retrying")
    else:
        context.log("Failed to unzip")
        sys.exit(1)


if __name__ == '__main__':
    main()
