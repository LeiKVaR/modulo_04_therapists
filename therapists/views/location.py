from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from Reflexo.models import Region, Province, District
from ..serializers.location import (
    LocationRegionSerializer, 
    LocationProvinceSerializer, 
    LocationDistrictSerializer,
    CascadingLocationSerializer
)
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
def get_location_options(request):
    """Obtiene todas las opciones de ubicación para formularios"""
    try:
        regions = Region.objects.all().order_by('name')
        provinces = Province.objects.all().order_by('name')
        districts = District.objects.all().order_by('name')
        
        data = {
            'regions': LocationRegionSerializer(regions, many=True).data,
            'provinces': LocationProvinceSerializer(provinces, many=True).data,
            'districts': LocationDistrictSerializer(districts, many=True).data,
        }
        
        logger.info(f"Location options loaded: {len(regions)} regions, {len(provinces)} provinces, {len(districts)} districts")
        return Response(data)
        
    except Exception as e:
        logger.error(f"Error loading location options: {str(e)}")
        return Response(
            {'error': 'Error al cargar las opciones de ubicación'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_regions_for_form(request):
    """Obtiene solo las regiones para el formulario (sin filtrado)"""
    try:
        regions = CascadingLocationSerializer.get_regions_for_form()
        logger.info(f"Regions for form loaded: {len(regions)} regions")
        return Response(regions)
        
    except Exception as e:
        logger.error(f"Error loading regions for form: {str(e)}")
        return Response(
            {'error': 'Error al cargar las regiones'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_provinces_for_form(request):
    """Obtiene provincias para el formulario con filtrado opcional por región"""
    try:
        region_id = request.GET.get('region_id')
        
        if region_id:
            # Validar que la región existe
            try:
                region = Region.objects.get(id=region_id)
                provinces = CascadingLocationSerializer.get_provinces_for_form(region_id=region_id)
                logger.info(f"Provinces for region {region.name} (ID: {region_id}): {len(provinces)} found")
            except ObjectDoesNotExist:
                return Response(
                    {'error': f'Región con ID {region_id} no encontrada'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            # Si no se especifica región, devolver todas las provincias
            provinces = CascadingLocationSerializer.get_provinces_for_form()
            logger.info(f"All provinces loaded: {len(provinces)} provinces")
        
        return Response(provinces)
        
    except Exception as e:
        logger.error(f"Error loading provinces for form: {str(e)}")
        return Response(
            {'error': 'Error al cargar las provincias'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_districts_for_form(request):
    """Obtiene distritos para el formulario con filtrado opcional por provincia o región"""
    try:
        province_id = request.GET.get('province_id')
        region_id = request.GET.get('region_id')
        
        if province_id:
            # Validar que la provincia existe
            try:
                province = Province.objects.get(id=province_id)
                districts = CascadingLocationSerializer.get_districts_for_form(province_id=province_id)
                logger.info(f"Districts for province {province.name} (ID: {province_id}): {len(districts)} found")
            except ObjectDoesNotExist:
                return Response(
                    {'error': f'Provincia con ID {province_id} no encontrada'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        elif region_id:
            # Validar que la región existe
            try:
                region = Region.objects.get(id=region_id)
                districts = CascadingLocationSerializer.get_districts_for_form(region_id=region_id)
                logger.info(f"Districts for region {region.name} (ID: {region_id}): {len(districts)} found")
            except ObjectDoesNotExist:
                return Response(
                    {'error': f'Región con ID {region_id} no encontrada'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            # Si no se especifica filtro, devolver todos los distritos
            districts = CascadingLocationSerializer.get_districts_for_form()
            logger.info(f"All districts loaded: {len(districts)} districts")
        
        return Response(districts)
        
    except Exception as e:
        logger.error(f"Error loading districts for form: {str(e)}")
        return Response(
            {'error': 'Error al cargar los distritos'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_regions_list(request):
    """Obtiene la lista de regiones"""
    try:
        regions = Region.objects.all().order_by('name')
        serializer = LocationRegionSerializer(regions, many=True)
        
        logger.info(f"Regions list loaded: {len(regions)} regions")
        return Response(serializer.data)
        
    except Exception as e:
        logger.error(f"Error loading regions: {str(e)}")
        return Response(
            {'error': 'Error al cargar las regiones'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_provinces_by_region(request, region_id):
    """Obtiene las provincias de una región específica"""
    try:
        # Validar que la región existe
        region = Region.objects.get(id=region_id)
        
        # Filtrar provincias por región
        provinces = Province.objects.filter(region=region).order_by('name')
        
        # Log para debugging
        logger.info(f"Provinces for region {region.name} (ID: {region_id}): {provinces.count()} found")
        
        # Verificar que las provincias realmente pertenecen a la región
        for province in provinces[:3]:  # Log solo las primeras 3 para verificar
            logger.info(f"  - Province: {province.name} (ID: {province.id}), region_id: {province.region_id}")
        
        serializer = LocationProvinceSerializer(provinces, many=True)
        
        return Response({
            'region': {
                'id': region.id,
                'name': region.name,
                'ubigeo_code': region.ubigeo_code
            },
            'provinces': serializer.data,
            'total_count': provinces.count()
        })
        
    except ObjectDoesNotExist:
        logger.warning(f"Region with ID {region_id} not found")
        return Response(
            {'error': f'Región con ID {region_id} no encontrada'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Error loading provinces for region {region_id}: {str(e)}")
        return Response(
            {'error': 'Error al cargar las provincias'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_districts_by_province(request, province_id):
    """Obtiene los distritos de una provincia específica"""
    try:
        # Validar que la provincia existe
        province = Province.objects.get(id=province_id)
        
        # Filtrar distritos por provincia
        districts = District.objects.filter(province=province).order_by('name')
        
        # Log para debugging
        logger.info(f"Districts for province {province.name} (ID: {province_id}): {districts.count()} found")
        
        # Verificar que los distritos realmente pertenecen a la provincia
        for district in districts[:3]:  # Log solo los primeros 3 para verificar
            logger.info(f"  - District: {district.name} (ID: {district.id}), province_id: {district.province_id}")
        
        serializer = LocationDistrictSerializer(districts, many=True)
        
        return Response({
            'province': {
                'id': province.id,
                'name': province.name,
                'ubigeo_code': province.ubigeo_code,
                'region': {
                    'id': province.region.id,
                    'name': province.region.name
                }
            },
            'districts': serializer.data,
            'total_count': districts.count()
        })
        
    except ObjectDoesNotExist:
        logger.warning(f"Province with ID {province_id} not found")
        return Response(
            {'error': f'Provincia con ID {province_id} no encontrada'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Error loading districts for province {province_id}: {str(e)}")
        return Response(
            {'error': 'Error al cargar los distritos'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def test_filtering(request):
    """Endpoint de prueba para verificar el filtrado de ubicaciones"""
    try:
        # Obtener algunas regiones de ejemplo
        regions = Region.objects.all()[:3]
        
        test_data = []
        
        for region in regions:
            # Obtener provincias de esta región
            provinces = Province.objects.filter(region=region)[:2]
            
            region_data = {
                'region': {
                    'id': region.id,
                    'name': region.name,
                    'ubigeo_code': region.ubigeo_code
                },
                'provinces': []
            }
            
            for province in provinces:
                # Obtener distritos de esta provincia
                districts = District.objects.filter(province=province)[:2]
                
                province_data = {
                    'id': province.id,
                    'name': province.name,
                    'ubigeo_code': province.ubigeo_code,
                    'region_id': province.region_id,
                    'districts': []
                }
                
                for district in districts:
                    district_data = {
                        'id': district.id,
                        'name': district.name,
                        'ubigeo_code': district.ubigeo_code,
                        'province_id': district.province_id
                    }
                    province_data['districts'].append(district_data)
                
                region_data['provinces'].append(province_data)
            
            test_data.append(region_data)
        
        return Response({
            'message': 'Prueba de filtrado de ubicaciones',
            'test_data': test_data,
            'verification': {
                'total_regions': Region.objects.count(),
                'total_provinces': Province.objects.count(),
                'total_districts': District.objects.count()
            }
        })
        
    except Exception as e:
        logger.error(f"Error in test filtering: {str(e)}")
        return Response(
            {'error': f'Error en la prueba de filtrado: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
