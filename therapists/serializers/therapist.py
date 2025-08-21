import re
from datetime import date
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
        extra_kwargs = {
            'email': {
                'required': False,
                'allow_null': True,
                'error_messages': {
                    'invalid': "El correo debe ser válido y terminar en @gmail.com"
                }
            }
        }
    def validate_document_number(self, value):
        doc_type = self.initial_data.get("document_type")

        if doc_type == "DNI":
            if not value.isdigit():
                raise serializers.ValidationError("El DNI debe contener solo números.")
            if not (8 <= len(value) <= 9):
                raise serializers.ValidationError(
                    "El DNI debe tener entre 8 y 9 dígitos."
                )

        elif doc_type == "CE":
            if not value.isdigit():
                raise serializers.ValidationError(
                    "El Carné de Extranjería debe contener solo números."
                )
            if len(value) > 12:
                raise serializers.ValidationError(
                    "El Carné de Extranjería debe tener máximo 12 dígitos."
                )

        elif doc_type == "PTP":
            if not value.isdigit():
                raise serializers.ValidationError("El PTP debe contener solo números.")
            if len(value) != 9:
                raise serializers.ValidationError(
                    "El PTP debe tener exactamente 9 dígitos."
                )

        elif doc_type == "CR":
            if not re.match(r"^[A-Za-z0-9]+$", value):
                raise serializers.ValidationError(
                    "El Carné de Refugiado debe contener solo letras y números."
                )

        elif doc_type == "PAS":
            if not re.match(r"^[A-Za-z0-9]+$", value):
                raise serializers.ValidationError(
                    "El Pasaporte debe contener solo letras y números."
                )

        return value

    def validate_first_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío.")
        return value

    def validate_last_name_paternal(self, value):
        if not value.strip():
            raise serializers.ValidationError("El apellido paterno no puede estar vacío.")
        return value

    def validate_last_name_maternal(self, value):
        if not value.strip():
            raise serializers.ValidationError("El apellido materno no puede estar vacío.")
        return value

    def validate_personal_reference(self, value):
        if value and not re.match(r"^[A-Za-z0-9\s]+$", value):
            raise serializers.ValidationError(
                "La referencia personal solo puede contener letras y números."
            )
        return value

    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("El teléfono debe contener solo dígitos.")
        if len(value) > 15:
            raise serializers.ValidationError(
                "El teléfono debe tener máximo 15 dígitos."
            )
        return value

    def validate_email(self, value):
        if value:
            pattern = r'^[A-Za-z0-9._%+-]+@gmail\.com$'
            if not re.match(pattern, value):
                raise serializers.ValidationError("El correo debe ser válido y terminar en @gmail.com (ejemplo: usuario@gmail.com).")
        return value

    def validate_address(self, value):
        if value and not re.match(r"^[A-Za-z0-9\s,.-]+$", value):
            raise serializers.ValidationError(
                "La dirección solo puede contener letras, números y símbolos básicos (,.-)."
            )
        return value

    def validate_profile_picture(self, value):
        if not value:
            return value
        valid_extensions = ["png", "jpg", "jpeg"]
        ext = str(value).split(".")[-1].lower()
        if ext not in valid_extensions:
            raise serializers.ValidationError(
                "La imagen debe estar en formato PNG, JPG o JPEG."
            )
        return value

    def validate_birth_date(self, value):
        today = date.today()

        # No permitir fechas futuras
        if value > today:
            raise serializers.ValidationError("La fecha de nacimiento no puede ser futura.")

        # Calcular edad
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 18:
            raise serializers.ValidationError("El terapeuta debe tener al menos 18 años.")

        return value
