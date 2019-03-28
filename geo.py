import itertools
import json
import operator

from geopy import distance
from geopy import geocoders


def get_restaurants() -> list:
    """Returns restaurants parsed from data file.

    :returns: list[dict]
    :returns: Restaurants
    """
    with open('data/berlin_restaurants.json', 'r') as restaurants_file:
        return json.load(restaurants_file)


def get_restaurants_with_cuisine(restaurants: list) -> list:
    """Returns restaurants with cuisine data based on passed restaurants.

    :param restaurants: list[dict]
    :returns: list[dict]
    :returns: Restaurants
    """
    restaurants_with_cuisine = []
    for restaurant in restaurants:
        if 'cuisine' in restaurant['tags']:
            restaurant['cuisine_list'] = restaurant['tags']['cuisine']\
                                         .split(';')
            restaurants_with_cuisine.append(restaurant)
    return restaurants_with_cuisine


# TODO(lwieczorek): Remove global variables
RESTAURANTS = get_restaurants()
RESTAURANTS_WITH_CUISINE = get_restaurants_with_cuisine(RESTAURANTS)


def near_coordinates(lat: float, lon: float) -> list:
    """Returns at most 10 near restaurants based on passed coordinates.

    :param lat: Latitude
    :param lon: Longitude
    :returns: list[dict]
    :returns: Restaurants
    """
    near_restaurants = []
    for restaurant in RESTAURANTS:
        restaurant_coordinates = (restaurant['lat'], restaurant['lon'])
        restaurant_distance = distance.distance((lat, lon),
                                                restaurant_coordinates).km
        if restaurant_distance < 10.0:
            restaurant['distance'] = restaurant_distance
            near_restaurants.append(restaurant)
    sorted_near_restaurants = sorted(near_restaurants,
                                     key=operator.itemgetter('distance'))
    return sorted_near_restaurants[:10]


def get_location(address: str):
    """Fetches location using geopy.
    :param address: Address
    :returns: Location
    :raises: geopy.exc.GeopyError
    """
    geocoder = geocoders.Nominatim(user_agent="restaurants")
    return geocoder.geocode(address)


def near_address(address: str) -> list:
    """Returns at most 10 near restaurants based on address.

    :param address: Address
    :returns: list[dict]
    :returns: Restaurants
    :raises: geopy.exc.GeopyError
    """
    location = get_location(address)
    return near_coordinates(location.latitude, location.longitude)


def filter_restaurants_by_cuisine(cuisine: str) -> list:
    """Returns filtered restaurants with cuisine data based on passed cuisine.

    :param cuisine: Cuisine
    :returns: list[dict]
    :returns: Restaurants
    """
    return [restaurant for restaurant in RESTAURANTS_WITH_CUISINE
            if cuisine in restaurant['cuisine_list']]


def combo(cuisine_a: str, cuisine_b: str) -> list:
    """Returns near restaurant pairs based on two cuisines.

    :param cuisine_a: Cuisine A
    :param cuisine_b: Cuisine B
    :returns: list[dict]
    :returns: Restaurants
    """
    cuisine_a_restaurants = filter_restaurants_by_cuisine(cuisine_a)
    cuisine_b_restaurants = filter_restaurants_by_cuisine(cuisine_b)
    near_restaurants = []
    for restaurant_a, restaurant_b in itertools.product(
            cuisine_a_restaurants, cuisine_b_restaurants):
        restaurant_distance = distance.distance(
                (restaurant_a['lat'], restaurant_a['lon']),
                (restaurant_b['lat'], restaurant_b['lon'])).km
        near_restaurants.append({'distance': restaurant_distance,
                                 'restaurant_a': restaurant_a,
                                 'restaurant_b': restaurant_b})
    sorted_near_restaurants = sorted(near_restaurants,
                                     key=operator.itemgetter('distance'))
    return sorted_near_restaurants[:10]
