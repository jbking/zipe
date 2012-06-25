# -*- coding:utf-8 -*-
import unicodedata


def convert(s, from_, to):
    s = s.decode(from_)
    try:
        s = s.encode(to)
    except UnicodeEncodeError:
        s = unicodedata.normalize('NFC', s).encode(to)
    return s
