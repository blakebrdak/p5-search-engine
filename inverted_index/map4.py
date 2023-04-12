#!/usr/bin/env python3
"""Map 4."""

import sys

# Group everything with doc_id % 3 as key
for line in sys.stdin:
    word, idfk, doc_id, count, norm = line.strip().split()
    key = int(doc_id) % 3
    print(f'{key}\t{line.strip()}')
