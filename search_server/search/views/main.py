"""Search Server Views. 

URLS Included:
/
"""
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
    context = {'query': query}
    return flask.render_template("index.html", **context)  # Add **context eventually


def call_index(route):
    """Make a call to the index server, return results."""