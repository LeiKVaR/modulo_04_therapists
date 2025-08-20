from rest_framework import serializers
from ..models import Therapist
from Reflexo.models import Region, Province, District

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name', 'ubigeo_code']

class ProvinceSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    
    class Meta:
        model = Province
        fields = ['id', 'name', 'ubigeo_code', 'region']

class DistrictSerializer(serializers.ModelSerializer):
    province = ProvinceSerializer(read_only=True)
    
    class Meta:
        model = District
        fields = ['id', 'name', 'ubigeo_code', 'province']

class TherapistSerializer(serializers.ModelSerializer):
    # Campos de ubicación con información detallada
    region_detail = RegionSerializer(source='region', read_only=True)
    province_detail = ProvinceSerializer(source='province', read_only=True)
    district_detail = DistrictSerializer(source='district', read_only=True)
    
    # Campos para selección en formularios
    region_name = serializers.CharField(source='region.name', read_only=True)
    province_name = serializers.CharField(source='province.name', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)
    
    class Meta:
        model = Therapist
        fields = [
            'id', 'document_type', 'document_number', 'last_name_paternal', 
            'last_name_maternal', 'first_name', 'birth_date', 'gender', 
            'personal_reference', 'is_active', 'phone', 'email',
            'region', 'province', 'district',  # IDs para formularios
            'region_detail', 'province_detail', 'district_detail',  # Información completa
            'region_name', 'province_name', 'district_name',  # Nombres para display
            'address', 'profile_picture'
        ]
        read_only_fields = ['id', 'region_detail', 'province_detail', 'district_detail', 
                           'region_name', 'province_name', 'district_name']
