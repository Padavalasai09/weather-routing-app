from __future__ import annotations

from datetime import date

from routes.models import CityProfile, TripRequest

CITY_PROFILES = {
    'Seattle': {'region': 'Northwest', 'avg_temperature_c': 17, 'avg_rain_mm': 12, 'avg_wind_kph': 18, 'description': 'Cool mornings with frequent rain showers.'},
    'San Francisco': {'region': 'West Coast', 'avg_temperature_c': 20, 'avg_rain_mm': 4, 'avg_wind_kph': 15, 'description': 'Mild coastal weather with a light marine breeze.'},
    'Denver': {'region': 'Mountain West', 'avg_temperature_c': 21, 'avg_rain_mm': 3, 'avg_wind_kph': 22, 'description': 'Dry air and crisp mountain conditions.'},
    'Chicago': {'region': 'Midwest', 'avg_temperature_c': 19, 'avg_rain_mm': 8, 'avg_wind_kph': 24, 'description': 'Variable conditions with gusts in the afternoon.'},
    'Austin': {'region': 'South', 'avg_temperature_c': 27, 'avg_rain_mm': 6, 'avg_wind_kph': 17, 'description': 'Warm and sunny with occasional storm bands.'},
    'Miami': {'region': 'Southeast', 'avg_temperature_c': 29, 'avg_rain_mm': 10, 'avg_wind_kph': 16, 'description': 'Hot humid days with tropical weather swings.'},
    'New York': {'region': 'Northeast', 'avg_temperature_c': 22, 'avg_rain_mm': 7, 'avg_wind_kph': 20, 'description': 'Balanced conditions with seasonal weather shifts.'},
}

ROUTE_PATHS = {
    'Seattle': ['Seattle', 'Denver', 'Austin'],
    'San Francisco': ['San Francisco', 'Denver', 'Miami'],
    'Denver': ['Denver', 'Chicago', 'Miami'],
    'Austin': ['Austin', 'Denver', 'New York'],
    'Miami': ['Miami', 'Chicago', 'New York'],
    'New York': ['New York', 'Chicago', 'Seattle'],
    'Chicago': ['Chicago', 'Denver', 'Austin'],
}


def seed_city_profiles():
    for name, profile in CITY_PROFILES.items():
        CityProfile.objects.update_or_create(
            name=name,
            defaults={
                'region': profile['region'],
                'avg_temperature_c': profile['avg_temperature_c'],
                'avg_rain_mm': profile['avg_rain_mm'],
                'avg_wind_kph': profile['avg_wind_kph'],
                'description': profile['description'],
            },
        )


def build_segment_weather(city, path_index):
    profile = CITY_PROFILES.get(city, CITY_PROFILES['Denver'])
    temperature = profile['avg_temperature_c'] + (path_index * 1.5) - 1.5
    rain = max(0, profile['avg_rain_mm'] + (path_index * 2) - 1)
    wind = max(0, profile['avg_wind_kph'] + (path_index * 3) - 2)
    return {
        'city': city,
        'temperature_c': round(temperature, 1),
        'rain_mm': round(rain, 1),
        'wind_kph': round(wind, 1),
        'condition': 'Clear' if rain < 4 and wind < 18 else 'Mixed' if rain < 8 else 'Challenging',
    }


def compute_route_score(route):
    segments = route.get('segments', [])
    if not segments:
        return 0

    total = 0
    for segment in segments:
        temp = float(segment.get('temperature_c', 22))
        rain = float(segment.get('rain_mm', 0))
        wind = float(segment.get('wind_kph', 0))
        comfort = 100 - abs(temp - 23) * 3.5 - rain * 4.0 - wind * 0.8
        total += max(0, min(100, comfort))
    return round(total / len(segments), 2)


def build_route_options(origin, destination):
    origin = origin.strip()
    destination = destination.strip()
    fallback = ROUTE_PATHS.get(origin) or [origin, 'Denver', destination]
    midpoints = [
        city for city in fallback
        if city not in {origin, destination}
    ]
    if len(midpoints) < 2:
        midpoints = ['Denver', 'Chicago', 'Miami']

    route_variants = [
        {'id': 'coastal', 'name': 'Coastal route', 'waypoints': [origin, midpoints[0], destination]},
        {'id': 'cross-country', 'name': 'Cross-country route', 'waypoints': [origin, midpoints[1] if len(midpoints) > 1 else 'Denver', destination]},
        {'id': 'balanced', 'name': 'Balanced route', 'waypoints': [origin, midpoints[2] if len(midpoints) > 2 else 'Chicago', destination]},
    ]

    options = []
    for idx, route in enumerate(route_variants):
        waypoints = route['waypoints']
        segments = [build_segment_weather(city, idx + 1) for city in waypoints]
        options.append({
            'id': route['id'],
            'name': route['name'],
            'waypoints': waypoints,
            'segments': segments,
            'status': 'Low risk' if idx == 2 else 'Moderate risk' if idx == 1 else 'Weather watch',
            'score': compute_route_score({'segments': segments}),
        })

    return sorted(options, key=lambda item: item['score'], reverse=True)


def plan_weather_route(origin, destination, departure_date=None, preferred_temperature_c=22.0):
    departure = departure_date or date.today().isoformat()
    options = build_route_options(origin, destination)
    best_route = max(options, key=lambda item: item['score'])
    TripRequest.objects.create(
        origin=origin,
        destination=destination,
        departure_date=departure,
        preferred_temperature_c=preferred_temperature_c,
    )

    return {
        'origin': origin,
        'destination': destination,
        'departure_date': departure,
        'preferred_temperature_c': preferred_temperature_c,
        'route_options': options,
        'best_route': best_route,
        'summary': f"{best_route['name']} is the preferred option with a comfort score of {best_route['score']}/100.",
    }
