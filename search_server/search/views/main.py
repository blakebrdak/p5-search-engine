"""Search Server Views. 

URLS Included:
/
"""
import requests
import json
import threading
import heapq
import flask
import search

threads_out = [None, None, None]

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
        search_urls.append(url + '?w=' + str(weight) + '&q=' + processed_query)

    # Call Index Servers and gather results
    # This works right now (it gathers all the results)
    # BUT it still needs to sort results, actually show the data
    # on the page, and be multi-threaded. 
    results = []
    threads = []
    # Split into threads, then join threads
    for idx, url in enumerate(search_urls):
        thread = threading.Thread(target=call_index,args=(url, idx))
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    # Merge the result lists
    count = 0
    shown_pages = []
    for item in heapq.merge(*threads_out, key=lambda dict: dict['score'], reverse=True):
        shown_pages.append(item)
        count = count + 1
        if count == 10:
            break
    print("ordered pages = ", shown_pages)

    # Pull needed info from db and build context dict
    context['results'] = []
    connection = search.model.get_db()
    for page in shown_pages:
        print(page)
        cur = connection.execute(
            """SELECT title, summary, url FROM Documents WHERE docid = ?""",
            (page['docid'],)
        )
        context['results'].append(cur.fetchone())
    print(context)
    return flask.render_template("index.html", **context)  # Add **context eventually


def call_index(route, idx):
    """Make a call to the index server, return results."""
    r = requests.get(route)
    threads_out[idx] = json.loads(r.text)['hits']
    return r.text