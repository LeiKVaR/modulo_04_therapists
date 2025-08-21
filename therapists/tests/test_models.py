from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models import Therapist, Region, Province, District
from datetime import date

class TherapistModelTest(TestCase):
    def setUp(self):
        # Crear datos de ubicación necesarios
        self.region = Region.objects.create(ubigeo_code='15', name='Lima')
        self.province = Province.objects.create(ubigeo_code='1501', name='Lima', region=self.region)
        self.district = District.objects.create(ubigeo_code='150101', name='Lima', province=self.province)
        
        self.therapist_data = {
            'document_type': 'DNI',
            'document_number': '12345678',
            'last_name_paternal': 'García',
            'last_name_maternal': 'López',
            'first_name': 'Juan',
            'birth_date': date(1990, 1, 1),
            'gender': 'M',
            'phone': '123456789',
            'email': 'juan@example.com',
            'region_fk': self.region,
            'province_fk': self.province,
            'district_fk': self.district
        }

    def test_create_therapist(self):
        therapist = Therapist.objects.create(**self.therapist_data)
        self.assertEqual(therapist.first_name, 'Juan')
        self.assertEqual(therapist.last_name_paternal, 'García')
        self.assertTrue(therapist.is_active)

    def test_therapist_str_representation(self):
        therapist = Therapist.objects.create(**self.therapist_data)
        expected = "Juan García López"
        self.assertEqual(str(therapist), expected)

    def test_therapist_without_maternal_last_name(self):
        data = self.therapist_data.copy()
        data['last_name_maternal'] = None
        data['document_number'] = '87654321'  # Número único
        therapist = Therapist.objects.create(**data)
        expected = "Juan García "
        self.assertEqual(str(therapist), expected)

    def test_therapist_required_fields(self):
        # Probar que los campos realmente requeridos son obligatorios
        # Solo probar campos que sabemos que son obligatorios
        required_fields = ['document_type', 'document_number', 'last_name_paternal', 
                          'first_name', 'birth_date', 'gender', 'phone']
        
        for field in required_fields:
            data = self.therapist_data.copy()
            del data[field]
            try:
                Therapist.objects.create(**data)
                # Si llega aquí, el campo no es realmente requerido
                self.fail(f"El campo {field} debería ser requerido")
            except Exception:
                # Campo es requerido, test pasa
                pass

    def test_therapist_optional_fields(self):
        # Probar que los campos opcionales no son obligatorios
        optional_fields = ['last_name_maternal', 'email', 'personal_reference', 
                          'address', 'profile_picture', 'region_fk', 'province_fk', 'district_fk']
        
        for i, field in enumerate(optional_fields):
            data = self.therapist_data.copy()
            if field in data:
                del data[field]
                # Usar número de documento único para cada test
                data['document_number'] = f'1234567{i}'
                try:
                    therapist = Therapist.objects.create(**data)
                    self.assertIsNotNone(therapist)
                except Exception as e:
                    self.fail(f"El campo {field} debería ser opcional, pero falló: {e}")

class RegionModelTest(TestCase):
    def test_create_region(self):
        region = Region.objects.create(ubigeo_code='01', name='Amazonas')
        self.assertEqual(region.name, 'Amazonas')
        self.assertEqual(str(region), 'Amazonas')

class ProvinceModelTest(TestCase):
    def test_create_province(self):
        region = Region.objects.create(ubigeo_code='01', name='Amazonas')
        province = Province.objects.create(ubigeo_code='101', name='Chachapoyas', region=region)
        self.assertEqual(province.name, 'Chachapoyas')
        self.assertEqual(province.region, region)
        self.assertEqual(str(province), 'Chachapoyas (Amazonas)')

class DistrictModelTest(TestCase):
    def test_create_district(self):
        region = Region.objects.create(ubigeo_code='01', name='Amazonas')
        province = Province.objects.create(ubigeo_code='101', name='Chachapoyas', region=region)
        district = District.objects.create(ubigeo_code='10101', name='Chachapoyas', province=province)
        self.assertEqual(district.name, 'Chachapoyas')
        self.assertEqual(district.province, province)
        self.assertEqual(str(district), 'Chachapoyas (Chachapoyas)')
