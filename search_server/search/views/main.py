"""SEARCH SERVER

URLS Included:
/
"""

import flask
import search


@search.app.route('/')
def show_index():
    return flask.render_template("index.html")  # Add **context eventually
