from rest_framework import serializers
from Reflexo.models import Region, Province, District

class LocationRegionSerializer(serializers.ModelSerializer):
    """Serializer para mostrar opciones de regiones en formularios"""
    class Meta:
        model = Region
        fields = ['id', 'name', 'ubigeo_code']

class LocationProvinceSerializer(serializers.ModelSerializer):
    """Serializer para mostrar opciones de provincias en formularios"""
    region_name = serializers.CharField(source='region.name', read_only=True)
    
    class Meta:
        model = Province
        fields = ['id', 'name', 'ubigeo_code', 'region_name']

class LocationDistrictSerializer(serializers.ModelSerializer):
    """Serializer para mostrar opciones de distritos en formularios"""
    province_name = serializers.CharField(source='province.name', read_only=True)
    region_name = serializers.CharField(source='province.region.name', read_only=True)
    
    class Meta:
        model = District
        fields = ['id', 'name', 'ubigeo_code', 'province_name', 'region_name']

# Serializers para filtrado en cascada
class CascadingLocationSerializer:
    """Clase para manejar el filtrado en cascada de ubicaciones"""
    
    @staticmethod
    def get_regions_for_form():
        """Obtiene solo las regiones para el formulario"""
        regions = Region.objects.all().order_by('name')
        return LocationRegionSerializer(regions, many=True).data
    
    @staticmethod
    def get_provinces_for_form(region_id=None):
        """Obtiene provincias filtradas por región o todas si no se especifica región"""
        if region_id:
            provinces = Province.objects.filter(region_id=region_id).order_by('name')
        else:
            provinces = Province.objects.all().order_by('name')
        return LocationProvinceSerializer(provinces, many=True).data
    
    @staticmethod
    def get_districts_for_form(province_id=None, region_id=None):
        """Obtiene distritos filtrados por provincia o región"""
        if province_id:
            districts = District.objects.filter(province_id=province_id).order_by('name')
        elif region_id:
            # Obtener distritos de todas las provincias de una región
            provinces = Province.objects.filter(region_id=region_id)
            districts = District.objects.filter(province__in=provinces).order_by('name')
        else:
            districts = District.objects.all().order_by('name')
        return LocationDistrictSerializer(districts, many=True).data
