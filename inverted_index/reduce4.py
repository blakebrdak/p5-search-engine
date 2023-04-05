#!/usr/bin/env python3
"""
Reduce 4.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools
import math


def reduce_one_group(key, group):
    """Reduce one group."""
    group = list(group)

    # Gather all info for matching words together
    words = {}
    for line in group:
        _, word, idfk, doc_id, freq, norm = line.strip().split()
        if word not in words:
            words[word] = [idfk]
            words[word].append(f'{doc_id} {freq} {norm}')
        else:
            words[word].append(f'{doc_id} {freq} {norm}')
    
    # Print final output
    for word in words:
        out_groups = words[word][1:]
        out_groups.sort()
        out_final = ' '.join(out_groups)
        print(f"{word} {words[word][0]} {out_final}")
        


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()