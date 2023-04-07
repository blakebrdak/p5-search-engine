"""Helper functions for the index server."""

import csv
import flask
import index 


def load_index():
    """Load the inverted index, stopwords, and PageRank files."""
    # THESE ARE GLOBAL VARIABLES THAT ARE SHARED.
    # Reference the vars with index.<varname> in main.

    index.index_file = {}
    # This is a dictionary of dictionaries (of dictionaries). 
    # each word has an associated dictionary of 
    # each document that it appears in, containing the
    # frequency and norm factor for that document. 
    # Outer dictionary also has idf of the word.
    #
    # --- EXAMPLE USAGE --- #
    # index.index_file[<word>] will return:
    # {
    #   'idf_score': <idf score of the word>
    #   <doc_id1>: {
    #       "frequency": <freq in doc_id1>
    #       "norm_factor": <norm_factor for doc doc_id1>
    #   }
    #   <doc_id2>: {
    #       ... same structure as prev
    #   }
    #   ... and so on
    # }
    # I really hope this is a smart way to store the info after
    # all this documentation i did lmao 
    # -- Blake <3

    # Thank you Blake!
    # -- Cameron <3


    # List of all stopwords
    index.stopwords = []

    # Maps key doc_id to value pagerank score
    index.pagerank = {}

    # Load inverted index
    idx_path = 'index_server/index/inverted_index/' + index.app.config['INDEX_PATH']
    with open(idx_path) as fin:
        for row in fin:
            # initial setup before looping each doc
            row = row.strip().split()
            word = row[0].strip()
            idf_score = row[1].strip()
            index.index_file[word] = {}
            index.index_file[word]['idf_score'] = float(idf_score)

            # Loop over all groups of 3 and assign them correctly
            row = row[2:]  # Remove first 2 items to make iterating simpler.
            doc_id = -1
            frequency = -1
            # iterate and split each group of 3 into dict
            for idx, item in enumerate(row):
                if idx % 3 == 0:
                    doc_id = item.strip()
                elif idx % 3 == 1:
                    frequency = float(item.strip())
                else:  # When idx % 3 = 2
                    index.index_file[word][doc_id] = {}
                    index.index_file[word][doc_id]['frequency'] = frequency
                    index.index_file[word][doc_id]['norm_factor'] = float(item.strip())



    # Load stopwords
    with open('index_server/index/stopwords.txt') as fin:
        for row in fin:
            index.stopwords.append(row.strip())

    # Load PageRank
    with open('index_server/index/pagerank.out') as fin:
        for row in csv.reader(fin):
            doc_id, score = row
            index.pagerank[int(doc_id)] = float(score)


# vaild_docs = set()  # Set of docs containing entire query so far
#     for idx, word in enumerate(cleaned_query):
#         words_set = set()  # Set of all docs containing this word
#         for doc_id in index.index_file[word]:
#             print(word, " ", doc_id)
#             if doc_id is not 'idf_score':
#                 words_set.add(doc_id)  # Add all docs to set
#         # Intersect set of docs containing word with 
#         # set of docs containing all prev words 
#         if idx != 0:
#             valid_docs = vaild_docs.intersection(words_set)
#         else:  # Initialize the set first iteration
#             vaild_docs = words_set
#     print(valid_docs)
#     # NOTE: Valid docs is a set containing id of all docs that contain both words.