from django.urls import path, include
from rest_framework.routers import DefaultRouter

from Reflexo.views import (
    views_distrito,
    views_provincia,
    views_region,
)
from .views import (
    TherapistViewSet, 
    SpecializationViewSet, 
    CertificationViewSet, 
    ScheduleViewSet,
    index
)

router = DefaultRouter()
router.register(r'therapists', TherapistViewSet, basename='therapist')
router.register(r'specializations', SpecializationViewSet, basename='specialization')
router.register(r'certifications', CertificationViewSet, basename='certification')
router.register(r'schedules', ScheduleViewSet, basename='schedule')

urlpatterns = [
    path('', index, name='therapists_index'),  # Página principal en /
    path('', include(router.urls)),  # APIs disponibles en la raíz
    path('distritos/', views_distrito.district_detail, name='distrito_list'),
    path('provincias/', views_provincia.province_detail, name='province_list'),
    path('regiones/', views_region.region_detail, name='region_list'),
]