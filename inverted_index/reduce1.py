#!/usr/bin/env python3
"""
Reduce 1.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools


def reduce_one_group(_, group):
    """Reduce one group."""
    group = list(group)

    # PASS THROUGH. INPUT CLEANED IN MAP
    for row in group:
        row_list = row.split('\t')
        print(f'{row_list[0]}\t{row_list[1].strip()}')


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Split lines into groups that share a key."""
    for keyey, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(keyey, group)


if __name__ == "__main__":
    main()
