"""Helper functions for the index server."""

import csv
import flask
import index 


def load_index():
    """Load the inverted index, stopwords, and PageRank files."""
    # THESE ARE GLOBAL VARIABLES THAT ARE SHARED.
    # TODO: STORE THESE IN A USABLE WAY IN THE ENDPOINTS.
    # Reference the vars with index.<varname> in main.
    index.index_file = {}
    index.stopwords = []  # List of all stopwords
    index.pagerank = {}  # Maps key doc_id to value pagerank score

    # Load inverted index
    idx_path = 'index_server/index/inverted_index/' + index.app.config['INDEX_PATH']
    with open(idx_path) as fin:
        for row in fin:
            # TODO How to store index in memory?

    # Load stopwords
    with open('index_server/index/stopwords.txt') as fin:
        for row in fin:
            index.stopwords.append(row.strip())

    # Load PageRank
    with open('index_server/index/pagerank.out') as fin:
        for row in csv.reader(fin):
            doc_id, score = row
            index.pagerank[int(doc_id)] = float(score)
