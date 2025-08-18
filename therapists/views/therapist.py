# -*- coding: utf-8 -*-
"""
Vistas para la aplicación de terapeutas.
Maneja las operaciones CRUD y renderizado de templates.
"""

from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Therapist
from ..serializers import TherapistSerializer

class TherapistViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar operaciones CRUD de terapeutas.
    Incluye soft delete, restauración y filtros.
    """
    serializer_class = TherapistSerializer
    queryset = Therapist.objects.all()  # pylint: disable=no-member
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'first_name', 'last_name_paternal', 'last_name_maternal',
        'document_number', 'document_type', 'email', 'phone', 'country',
        'department', 'province', 'district', 'address'
    ]

    def get_queryset(self):
        """
        Filtra terapeutas por estado activo/inactivo.
        Por defecto muestra solo activos.
        """
        qs = Therapist.objects.all()  # pylint: disable=no-member
        active = self.request.query_params.get('active', 'true').lower()
        if active in ('true', '1', 'yes'):
            qs = qs.filter(is_active=True)
        elif active in ('false', '0', 'no'):
            qs = qs.filter(is_active=False)
        return qs

    def destroy(self, request, *args, **kwargs):
        """
        Soft delete - marca como inactivo en lugar de eliminar.
        """
        instance = self.get_object()
        instance.is_active = False
        instance.save(update_fields=['is_active'])
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def inactive(self, request):
        """
        Endpoint personalizado para obtener terapeutas inactivos.
        """
        queryset = Therapist.objects.filter(is_active=False)  # pylint: disable=no-member
        return Response(self.get_serializer(queryset, many=True).data)

    @action(detail=True, methods=['post', 'patch'])
    def restore(self, request, pk=None):
        """
        Restaura un terapeuta marcándolo como activo.
        """
        try:
            therapist = Therapist.objects.get(pk=pk)  # pylint: disable=no-member
        except Therapist.DoesNotExist:
            return Response(
                {"detail": "No encontrado."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        therapist.is_active = True
        therapist.save(update_fields=['is_active'])
        return Response(self.get_serializer(therapist).data)


def index(request):
    """
    Vista para renderizar la página principal de terapeutas.
    """
    return render(request, 'therapists_ui.html')
