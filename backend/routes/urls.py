from django.urls import path

from routes.views import health_check, route_plan

urlpatterns = [
    path('health/', health_check, name='api-health'),
    path('routes/plan/', route_plan, name='route-plan'),
]
