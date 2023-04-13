#!/usr/bin/env python3
"""
Reduce 0.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools


def reduce_one_group(_, group):
    """Reduce one group."""
    count = 0
    for _ in group:
        count = count + 1
    print(count)


def keyfunction(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide into groups that share key."""
    for key, grouppp in itertools.groupby(sys.stdin, keyfunction):
        reduce_one_group(key, grouppp)


if __name__ == "__main__":
    main()
