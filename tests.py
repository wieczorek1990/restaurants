import unittest
from unittest import mock

import geo


class GeoTest(unittest.TestCase):
    def assertRestaurant(self, restaurant):
        self.assertTrue('id' in restaurant)
        self.assertTrue('lat' in restaurant)
        self.assertTrue('lon' in restaurant)
        self.assertTrue('tags' in restaurant)

    def test_get_restaurants(self):
        restaurants = geo.get_restaurants()
        self.assertIsInstance(restaurants, list)
        first_restaurant = restaurants[0]
        self.assertRestaurant(first_restaurant)

    def test_get_restaurants_with_cuisine(self):
        restaurants = geo.get_restaurants_with_cuisine(geo.RESTAURANTS)
        self.assertIsInstance(restaurants, list)
        first_restaurant = restaurants[0]
        self.assertRestaurant(first_restaurant)
        self.assertTrue('cuisine_list' in first_restaurant)
        self.assertTrue('cuisine' in first_restaurant['tags'])

    def test_near_coordinates(self):
        lat, lon = 52.538554, 13.4102856
        restaurants = geo.near_coordinates(lat, lon)
        self.assertIsInstance(restaurants, list)
        first_restaurant = restaurants[0]
        self.assertRestaurant(first_restaurant)
        self.assertTrue('distance' in first_restaurant)
        second_restaurant = restaurants[1]
        self.assertTrue(first_restaurant['distance'] <
                        second_restaurant['distance'])

    def test_near_address(self):
        class LocationMock:
            def __init__(self, lat, lon):
                self.latitude = lat
                self.longitude = lon

        with mock.patch('geo.get_location',
                        return_value=LocationMock(52.538554, 13.4102856)):
            address = 'Berlin'
            restaurants = geo.near_address(address)
            self.assertIsInstance(restaurants, list)
            first_restaurant = restaurants[0]
            self.assertRestaurant(first_restaurant)
            self.assertTrue('distance' in first_restaurant)

    def get_restaurants(self):
        return [
            {
                'id': 1234567890,
                'lat': 0.0,
                'lon': 0.0,
                'tags': {
                    'cuisine': 'polish',
                },
                'cuisine_list': ['polish'],
            },
            {
                'id': 1234567891,
                'lat': 1.0,
                'lon': 1.0,
                'tags': {
                },
                'cuisine_list': [],
            },
            {
                'id': 1234567892,
                'lat': 2.0,
                'lon': 2.0,
                'tags': {
                    'cuisine': 'polish;czech;german',
                },
                'cuisine_list': ['polish', 'czech', 'german'],
            },
        ]

    def test_filter_restaurants(self):
        with mock.patch('geo.RESTAURANTS_WITH_CUISINE',
                        self.get_restaurants()):
            restaurants = geo.filter_restaurants_by_cuisine('polish')
            self.assertEqual(len(restaurants), 2)
            first_restaurant = restaurants[0]
            self.assertRestaurant(first_restaurant)
            second_restaurant = restaurants[1]
            self.assertRestaurant(second_restaurant)

    def test_combo(self):
        with mock.patch('geo.RESTAURANTS_WITH_CUISINE',
                        self.get_restaurants()):
            restaurants = geo.combo('polish', 'german')
            self.assertIsInstance(restaurants, list)
            self.assertEqual(len(restaurants), 2)
            first_near_restaurants = restaurants[0]
            self.assertTrue('distance' in first_near_restaurants)
            self.assertTrue('restaurant_a' in first_near_restaurants)
            self.assertTrue('restaurant_b' in first_near_restaurants)
            self.assertRestaurant(first_near_restaurants['restaurant_a'])
            self.assertRestaurant(first_near_restaurants['restaurant_b'])


if __name__ == '__main__':
    unittest.main()
