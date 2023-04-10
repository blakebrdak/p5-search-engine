"""Search Server Views. 

URLS Included:
/
"""
import requests
import json
import threading
import flask
import search


@search.app.route('/')
def show_index():
    # Gather data from form
    query = ""
    if 'q' in flask.request.args:
        query = flask.request.args.get('q')  # THIS ONLY GETS FIRST WORD RIGHT NOW?
    weight = 0.5
    if 'w' in flask.request.args:
        weight = flask.request.args['w']
    context = {'query': query, 'weight': weight}
    search_urls = []
    for url in search.app.config['SEARCH_INDEX_SEGMENT_API_URLS']:
        processed_query = query.replace(' ', '+')
        search_urls.append(url + '?w=' + weight + '&q=' + processed_query)

    # Call Index Servers and gather results
    # This works right now (it gathers all the results)
    # BUT it still needs to sort results, actually show the data
    # on the page, and be multi-threaded. 
    results = []
    for url in search_urls:
        results = results + json.loads(call_index(url))['hits']
    print("results = ", results)

    # Make requests to the index servers
    return flask.render_template("index.html", **context)  # Add **context eventually


def call_index(route):
    """Make a call to the index server, return results."""
    r = requests.get(route)
    return r.text