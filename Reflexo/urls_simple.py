from django.urls import path
from .views.views_web import debug_view
from .views.views_country import countries
from .views.views_region import regions
from .views.views_provincia import provinces
from .views.views_distrito import districts

app_name = 'reflexo'

urlpatterns = [
    # API endpoints básicos
    path('', debug_view, name='home'),
    path('api/countries/', countries, name='api_countries'),
    path('api/regions/', regions, name='api_regions'),
    path('api/provinces/', provinces, name='api_provinces'),
    path('api/districts/', districts, name='api_districts'),
]
