import flask
from geopy import exc

import geo


app = flask.Flask(__name__)


@app.route("/restaurants/near/<float:lat>/<float:lon>")
def near_coordinates_route(lat: float, lon: float):
    return flask.jsonify(geo.near_coordinates(lat, lon))


@app.route("/restaurants/near/<string:address>")
def near_address_route(address: str):
    try:
        return flask.jsonify(geo.near_address(address))
    except exc.GeopyError:
        return flask.jsonify({'error': 'Geopy API call failed.'}), 503


@app.route("/restaurants/combo/<string:cuisine_a>/<string:cuisine_b>")
def combo_route(cuisine_a: str, cuisine_b: str):
    return flask.jsonify(geo.combo(cuisine_a, cuisine_b))
