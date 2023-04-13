#!/usr/bin/env python3
"""Map 2."""

import sys

# Group everything with word as key and docid as value
for line in sys.stdin:
    docid, text = line.strip().split('\t')
    for word in text.strip().split():
        print(f"{word}\t{docid}")
