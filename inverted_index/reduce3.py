#!/usr/bin/env python3
"""
Reduce 2.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools


def reduce_one_group(key, group):
    """Reduce one group."""
    group = list(group)
    # Calculate normalization factor

    # Find frequency for each word in doc
    seen_terms = {}  # list to avoid duplicates
    term_idfk = {}
    for line in group:
        _, other = line.strip().split('\t')
        word, idfk = other.strip().split()
        # First instance of a word
        if word not in seen_terms:
            seen_terms[word] = 1
            term_idfk[word] = idfk
        else:
            # Increment total count for document
            seen_terms[word] = seen_terms[word] + 1
    # Calculate norm factor for doc
    norm = 0
    for term, termval in seen_terms:
        norm = norm + ((termval * float(term_idfk[term])) ** 2)

    # handle output
    for word, wordval in seen_terms:
        print(f'{word}\t{term_idfk[word]} {key} {wordval} {norm}')


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
