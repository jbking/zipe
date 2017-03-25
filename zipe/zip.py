import argparse
import os
import sys
import zipfile

from .util import Context


class ZipContext(Context):
    recursive = True

    def find_entries(self, original_entries):
        if self.recursive:
            entries = []
            for root_entry in original_entries:
                for directory, _, files in os.walk(root_entry):
                    entries.append(directory)
                    entries.extend([os.path.join(directory, f)
                                    for f in files])
            return entries
        else:
            return original_entries


def zip_(context, zip_file, entries):
    entries = context.find_entries(entries)

    with zipfile.ZipFile(zip_file, 'a') as z:
        for entry in entries:
            if not context.is_target(entry):
                continue
            context.log("Archiving: %s" % entry)
            arcname = context.convert_str_to_zip_str(entry)
            z.write(entry, arcname)


def main(argv=sys.argv):
    parser = argparse.ArgumentParser(
                        description="Zipper for not native encoded filename file")
    parser.add_argument('zip_file', metavar='ZIP_FILE',
                        help="ZIP archive")
    parser.add_argument('entries', nargs='+', metavar='ENTRY',
                        help="file entries")
    parser.add_argument('-F', '--from', metavar='ENCODING', dest='from_',
                        default=sys.getfilesystemencoding(),
                        help="filename encoding from"
                             "(Default sys.getfilesystemencoding())")
    parser.add_argument('-T', '--to', metavar='ENCODING',
                        required=True,
                        help="filename encoding to ")
    # No support
    # parser.add_argument('-P', '--password',
    #                     help="password for encrypted")
    parser.add_argument('-r', '--recursive',
                        action='store_true',
                        help="archive recursively")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="verbose mode")
    filter_group = parser.add_mutually_exclusive_group()
    filter_group.add_argument('-x', '--exclude',
                              action='append',
                              help="exclude file pattern in RegExp")
    filter_group.add_argument('-i', '--include',
                              action='append',
                              help="include file pattern in RegExp")
    args = parser.parse_args(argv[1:])

    context = ZipContext()
    context.verbose = args.verbose
    context.from_ = args.from_
    context.to = args.to
    context.exclude_patterns = args.exclude
    context.include_patterns = args.include
    context.recursive = args.recursive

    zip_(context, args.zip_file, args.entries)


if __name__ == '__main__':
    main()
