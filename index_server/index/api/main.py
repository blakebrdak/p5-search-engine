"""REST API for INdex """

import flask
import index

@index.app.route('/api/v1/', methods=['GET'])
def routes():
    # EXAMPLE OF HOW TO REFERENCE THE GLOBALS
    # TODO: IMPLEMENT ME
    return(index.index_file['smelting'])

@index.app.route('/api/v1/hits/', methods=['GET'])
def hits():
    # TODO: IMPLEMENT ME
    return("IMPLEMENT ME")