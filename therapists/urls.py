from django.urls import path, include
from rest_framework.routers import DefaultRouter
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
]