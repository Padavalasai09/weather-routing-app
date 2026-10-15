from django.test import SimpleTestCase

from routes.services import compute_route_score


class RouteScoringTests(SimpleTestCase):
    def test_rain_and_wind_penalize_a_route(self):
        route = {
            'segments': [
                {'temperature_c': 22, 'rain_mm': 16, 'wind_kph': 35, 'city': 'Seattle'},
                {'temperature_c': 24, 'rain_mm': 5, 'wind_kph': 18, 'city': 'Denver'},
                {'temperature_c': 28, 'rain_mm': 1, 'wind_kph': 10, 'city': 'Austin'},
            ]
        }

        score = compute_route_score(route)

        self.assertLess(score, 70)
        self.assertGreater(score, 0)

    def test_balanced_weather_scores_higher(self):
        route = {
            'segments': [
                {'temperature_c': 21, 'rain_mm': 1, 'wind_kph': 12, 'city': 'San Francisco'},
                {'temperature_c': 23, 'rain_mm': 0, 'wind_kph': 9, 'city': 'Denver'},
                {'temperature_c': 25, 'rain_mm': 0, 'wind_kph': 8, 'city': 'Miami'},
            ]
        }

        score = compute_route_score(route)

        self.assertGreater(score, 80)
