Look help at each command.

zipe only supports cp932 and utf-8 as encoding to. And no support making encrypt zip archive for now.

::

    usage: zipe [-h] [-F ENCODING] -T ENCODING [-r] [-v]
                [-x EXCLUDE | -i INCLUDE]
                ZIP_FILE ENTRY [ENTRY ...]

    Zipper for not native encoded filename file

    positional arguments:
      ZIP_FILE              ZIP archive
      ENTRY                 file entries

    optional arguments:
      -h, --help            show this help message and exit
      -F ENCODING, --from ENCODING
                            filename encoding from(Default
                            sys.getfilesystemencoding())
      -T ENCODING, --to ENCODING
                            filename encoding to
      -r, --recursive       archive recursively
      -v, --verbose         verbose mode
      -x EXCLUDE, --exclude EXCLUDE
                            exclude file pattern in RegExp
      -i INCLUDE, --include INCLUDE
                            include file pattern in RegExp

::

    usage: unzipe [-h] [-l] [-P PASSWORD] [--force] -F ENCODING [-T ENCODING]
                  [-x EXCLUDE | -i INCLUDE]
                  ZIP_FILE [ENTRY [ENTRY ...]]

    Unzipper for not native encoded filename file

    positional arguments:
      ZIP_FILE              ZIP archive
      ENTRY                 can specify file entries

    optional arguments:
      -h, --help            show this help message and exit
      -l, --list            list entries instead of extracting
      -P PASSWORD, --password PASSWORD
                            password for encrypted
      --force               extract file even if its absolute path
      -v, --verbose         verbose mode
      -F ENCODING, --from ENCODING
                            filename encoding from
      -T ENCODING, --to ENCODING
                            filename encoding to(Default
                            sys.getfilesystemencoding())
      -x EXCLUDE, --exclude EXCLUDE
                            exclude filename pattern in RegExp
      -i INCLUDE, --include INCLUDE
                            include filename pattern in RegExp
