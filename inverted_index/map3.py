#!/usr/bin/env python3
"""Map 3."""

import sys

# Group everything with docid as key, word and idfk as val
for line in sys.stdin:
    word, items = line.strip().split('\t')
    idfk = -1
    for idx, item in enumerate(items.split()):
        if idx == 0:
            idfk = item.strip()
        else:
            print(f'{item.strip()}\t{word} {idfk}')

    