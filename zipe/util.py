# -*- coding:utf-8 -*-
import os
import re
import sys
import unicodedata


class Context:
    verbose = False
    force = False
    password = None

    # encoding pair
    from_ = None
    to = None

    @property
    def include_patterns(self):
        return self._include_patterns

    @include_patterns.setter
    def include_patterns(self, patterns):
        if patterns:
            self._include_patterns = [re.compile(pattern) for pattern in patterns]

    _include_patterns = []

    @property
    def exclude_patterns(self):
        return self._exclude_patterns

    @exclude_patterns.setter
    def exclude_patterns(self, patterns):
        if patterns:
            self._exclude_patterns = [re.compile(pattern) for pattern in patterns]

    _exclude_patterns = []

    def log(self, line):
        if self.verbose:
            print(line, file=sys.stderr)

    def convert_zip_str_to_str(self, s):
        # http://qiita.com/methane/items/8493c10c19ca3584d31d
        if self.from_ == 'cp932':
            s = s.encode('cp437')
        form = 'NFD' if sys.platform == 'darwin' else 'NFC'
        return unicodedata.normalize(form, s.decode(self.from_))

    def convert_str_to_zip_str(self, s):
        return s.encode(self.to)

    def is_safe_path(self, path):
        if not path.startswith(os.sep):
            return True
        if self.force:
            return True
        return False

    def is_target(self, path):
        if self._include_patterns:
            for pattern in self._include_patterns:
                if pattern.search(path):
                    break
            else:
                return False

        for pattern in self._exclude_patterns:
            if pattern.search(path):
                return False

        return True

    def wrap(self, zipfile):
        if self.password:
            zipfile.setpassword(self.password.encode())
        return zipfile
