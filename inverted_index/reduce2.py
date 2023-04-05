#!/usr/bin/env python3
"""
Reduce 2.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools
import math


def reduce_one_group(key, group):
    """Reduce one group."""
    group = list(group)
    # PASS THROUGH. INPUT CLEANED IN MAP
    docs = []
    for row in group:
        word, doc_id = row.strip().split('\t')
        docs.append(doc_id)
    
    # Calculate inverse document frequency
    idfk = -1  # init val outside of context mgr
    with open("total_document_count.txt") as count_doc:
        total_docs = count_doc.readline() # Read the count
        docs_set = set(docs)
        idfk = math.log10(int(total_docs) / len(docs_set))
    string = ' '.join(docs) # Convert list to string

    print(f'{key}\t{idfk} {string}')


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()