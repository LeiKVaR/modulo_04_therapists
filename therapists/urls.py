from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TherapistViewSet, 
    SpecializationViewSet, 
    CertificationViewSet, 
    ScheduleViewSet,
    index,
    get_location_options,
    get_provinces_by_region,
    get_districts_by_province,
    get_regions_list,
    test_filtering,
    get_regions_for_form,
    get_provinces_for_form,
    get_districts_for_form
)

router = DefaultRouter()
router.register(r'therapists', TherapistViewSet, basename='therapist')
router.register(r'specializations', SpecializationViewSet, basename='specialization')
router.register(r'certifications', CertificationViewSet, basename='certification')
router.register(r'schedules', ScheduleViewSet, basename='schedule')

urlpatterns = [
    path('', index, name='therapists_index'),  # Página principal en /
    path('', include(router.urls)),  # APIs disponibles en la raíz
    
    # Endpoints para opciones de ubicación (legacy)
    path('location/options/', get_location_options, name='location_options'),
    path('location/regions/', get_regions_list, name='regions_list'),
    path('location/regions/<int:region_id>/provinces/', get_provinces_by_region, name='provinces_by_region'),
    path('location/provinces/<int:province_id>/districts/', get_districts_by_province, name='districts_by_province'),
    
    # Nuevos endpoints para formularios con filtrado en cascada
    path('location/form/regions/', get_regions_for_form, name='form_regions'),
    path('location/form/provinces/', get_provinces_for_form, name='form_provinces'),
    path('location/form/districts/', get_districts_for_form, name='form_districts'),
    
    # Endpoint de prueba para verificar filtrado
    path('location/test-filtering/', test_filtering, name='test_filtering'),
]