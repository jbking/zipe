See help at each command.

$ zipe -h
usage: zipe [-h] [-F ENCODING] -T ENCODING [-r] [-x EXCLUDE | -i INCLUDE]
            ZIP_FILE ENTRY [ENTRY ...]

Zipper for not native filename

positional arguments:
  ZIP_FILE              The ZIP archive
  ENTRY                 Specify file entries in the archive to extract

optional arguments:
  -h, --help            show this help message and exit
  -F ENCODING, --from ENCODING
                        Specify filename encoding from(Default
                        sys.getfilesystemencoding())
  -T ENCODING, --to ENCODING
                        Specify filename encoding to
  -r, --recursive       Archive recursively
  -x EXCLUDE, --exclude EXCLUDE
                        Exclude file pattern in RegExp
  -i INCLUDE, --include INCLUDE
                        Include file pattern in RegExp


$ unzipe -h
usage: unzipe [-h] [-l] [-P PASSWORD] [--force] -F ENCODING [-T ENCODING]
              [-x EXCLUDE | -i INCLUDE]
              ZIP_FILE [ENTRY [ENTRY ...]]

Unzipper for not native filename

positional arguments:
  ZIP_FILE              The ZIP archive
  ENTRY                 Specify file entries in the archive to extract

optional arguments:
  -h, --help            show this help message and exit
  -l, --list            List entries instead of extracting
  -P PASSWORD, --password PASSWORD
                        Enter password for encrypted
  --force               Extract file even if its absolute path
  -F ENCODING, --from ENCODING
                        Specify filename encoding from
  -T ENCODING, --to ENCODING
                        Specify filename encoding to (Default
                        sys.getfilesystemencoding())
  -x EXCLUDE, --exclude EXCLUDE
                        Exclude file pattern in RegExp
  -i INCLUDE, --include INCLUDE
                        Include file pattern in RegExp
