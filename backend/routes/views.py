from datetime import date
from pathlib import Path

from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from routes.services import plan_weather_route

BASE_DIR = Path(__file__).resolve().parent.parent


def home_view(request):
    html = (BASE_DIR / 'templates' / 'index.html').read_text(encoding='utf-8')
    return HttpResponse(html)


@api_view(['GET'])
def health_check(request):
    return Response({'status': 'ok', 'message': 'Weather routing API is live.'})


@api_view(['POST'])
def route_plan(request):
    origin = (request.data.get('origin') or '').strip()
    destination = (request.data.get('destination') or '').strip()
    departure_date = request.data.get('departure_date') or date.today().isoformat()
    preferred_temperature_c = float(request.data.get('preferred_temperature_c', 22.0))

    if not origin or not destination:
        return Response({'error': 'Both origin and destination are required.'}, status=400)

    payload = plan_weather_route(origin, destination, departure_date, preferred_temperature_c)
    return Response(payload)
