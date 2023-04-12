#!/usr/bin/env python3
"""Map 3."""

import sys

# Group everything with docid as key, word and IDFK as val
for line in sys.stdin:
    word, items = line.strip().split('\t')
    IDFK = -1
    for idx, item in enumerate(items.split()):
        if idx == 0:
            IDFK = item.strip()
        else:
            print(f'{item.strip()}\t{word} {IDFK}')
