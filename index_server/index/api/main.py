"""REST API for INdex """

import flask
import index
import re
import math

@index.app.route('/api/v1/', methods=['GET'])
def routes():
    """Returns a list of services available."""
    # EXAMPLE OF HOW TO REFERENCE THE GLOBALS
    # return(index.index_file['smelting'])
    
    out = {
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    }

    return flask.jsonify(out), 200


@index.app.route('/api/v1/hits/', methods=['GET'])
def hits():
    """Returns a list of hits with doc ID and score."""
    # Go to the project 5 spec release party recording at 23 minutes for an explanation
    # of how this is supposed to work.

    # get the query target from the url
    query = flask.request.args.get("q")

    # get the weight if it is specified
    if flask.request.args.get("w"):
        weight = float(flask.request.args.get("w"))
    else:
        # default value from the spec
        weight = 0.5

    cleaned_query = clean_query(query)

    # ERROR HANDLING:
    # If one of the words in the cleaned query is not in the index,
    # return None right away
    # Returns an empty list.
    for word in cleaned_query:
        if word not in index.index_file:
            return flask.jsonify({ 'hits': []})

    # see lab 11 for more info
    # q: tf-idf for the query - see the "Query vector" section of the spec for more info
    # d: dictionary of doc_ids with each doc_id having its own tf-idf vector of tuples
    # in the form (tf-idf, norm_factor)
    # See the "Document vector" section of the spec for more info
    # scores: stores tuples in the form of (document score, doc_id)
    # hits: list of dictionaries with the return values sorted by score
    q = []
    d = {}
    scores = []
    hits = []

    print("Hello!")
    fill_q(cleaned_query, q)
    valid_docs = get_valid_docs(cleaned_query)
    fill_d(cleaned_query, d, valid_docs)
    fill_scores(q, d, scores, weight, valid_docs)

    # sort the scores so that they can be added to hits
    scores.sort(reverse=True)


    for doc in scores:
        hits.append({
            'docid': int(doc[1]),
            'score': float(doc[0])
        })

    # need this for hits to be returned in the correct format for pytest
    return_dic = {}
    return_dic['hits'] = hits

    return flask.jsonify(return_dic), 200

def clean_query(query):
    """Cleans the input query and returns the cleaned input."""
    # Uses the same structure as map1.py to clean the query input
    # Clean input
    text = re.sub(r"[^a-zA-Z0-9 ]+", "", query)  # Remove special chars
    text = text.casefold()  # all lowercase
    text_list = text.strip().split() # Should be delimited by space by default
    # Clean out stopwords
    for word in index.stopwords:
        if word.strip() in text_list:
            while word.strip() in text_list:
                text_list.remove(word.strip())

    # returns a list of strings of all of the words in the query
    return text_list

def fill_q(cleaned_query, q):
    """Fills the query vector."""
    # dictionary to keep track of the term frequency of the words in the query
    q_tf = {}
    for word in cleaned_query:
        if word not in q_tf:
            q_tf[word] = 1.0
        else:
            q_tf[word] += 1.0

    # fill query vector with tf * idf
    for word in cleaned_query:
        q.append(q_tf[word] * index.index_file[word]['idf_score'])

def fill_d(cleaned_query, d, valid_docs):
    """Fills the document vectors."""    
    for doc_id in valid_docs:
        d[doc_id] = []
        for word in cleaned_query:
            d[doc_id].append(((index.index_file[word][doc_id]['frequency'] *
                                index.index_file[word]['idf_score']),
                                index.index_file[word][doc_id]['norm_factor']))

def fill_scores(q, d, scores, weight, valid_docs):
    """Fills the scores vector."""
    # compute query normalization factor for tf-idf
    q_norm = compute_query_norm(q)

    for doc_id in valid_docs:
        scores.append(((weight * index.pagerank[int(doc_id)] + (1.0 - weight) *
                       compute_tf_idf(q, d[doc_id], q_norm)), doc_id))

def compute_tf_idf(q, doc_vec, q_norm):
    """Computes the tf-idf score for each document."""
    # see the "tf-idf" section of the spec for more info

    # compute the dot product between q and doc_vec
    dot_product = 0.0
    for idx, q_val in enumerate(q):
        dot_product += q_val * doc_vec[idx][0]
    
    if dot_product == 0.0:
        return 0.0
    else:
        return (dot_product / (q_norm * math.sqrt(doc_vec[0][1])))

def compute_query_norm(q):
    """Computes the query normalization factor."""
    total = 0.0
    for val in q:
        total += val * val

    return math.sqrt(total)

def get_valid_docs(cleaned_query):
    """Generates a set of valid documents."""
    valid_docs = set()  # Set of docs containing entire query so far
    for idx, word in enumerate(cleaned_query):
        words_set = set()  # Set of all docs containing this word
        for doc_id in index.index_file[word]:
            # print(word, " ", doc_id)
            if doc_id != 'idf_score':
                words_set.add(doc_id)  # Add all docs to set
        # Intersect set of docs containing word with 
        # set of docs containing all prev words 
        if idx != 0:
            valid_docs = valid_docs.intersection(words_set)
        else:  # Initialize the set first iteration
            valid_docs = words_set

    # print("valid_docs: ", valid_docs)
    # NOTE: Valid docs is a set containing id of all docs that contain both words.

    return valid_docs
