import json
import operator

import flask
from geopy import distance
from geopy import exc
from geopy import geocoders


app = flask.Flask(__name__)
# TODO(lwieczorek): move to database
with open('data/berlin_restaurants.json', 'r') as file_:
    restaurants = json.load(file_)


def near_coordinates(lat, lon):
    near_restaurants = []
    for restaurant in restaurants:
        restaurant_coordinates = (restaurant['lat'], restaurant['lon'])
        restaurant_distance = distance.vincenty((lat, lon),
                                                restaurant_coordinates).km
        if restaurant_distance < 10.0:
            restaurant['distance'] = restaurant_distance
            near_restaurants.append(restaurant)
    sorted_near_restaurants = sorted(near_restaurants,
                                     key=operator.itemgetter('distance'))
    return sorted_near_restaurants[:10]


def near_address(address):
    geocoder = geocoders.Nominatim()
    location = geocoder.geocode(address)
    return near_coordinates(location.latitude, location.longitude)


@app.route("/restaurants/near/<float:lat>/<float:lon>")
def near_lat_long_route(lat, lon):
    return flask.jsonify(near_coordinates(lat, lon))


@app.route("/restaurants/near/<string:address>")
def near_address_route(address):
    try:
        return flask.jsonify(near_address(address))
    except exc.GeopyError:
        return flask.jsonify({'error': 'API call failed'}), 503


@app.route("/restaurants/combo/<string:cusine_a><string:cusine_b>")
def combo_route(cusine_a, cusine_b):
    return "Hello World!"
