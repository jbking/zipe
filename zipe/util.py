# -*- coding:utf-8 -*-
import sys
import unicodedata


def convert(s, from_, to):
    s = s.decode(from_)
    try:
        s = s.encode(to)
    except UnicodeEncodeError:
        s = unicodedata.normalize('NFC', s).encode(to)
    return s


class Context:
    verbose = False

    # encoding pair
    from_ = None
    to = None

    def log(self, line):
        if self.verbose:
            print(line, file=sys.stderr)

    def convert(self, src):
        return convert(src, self.from_, self.to)
