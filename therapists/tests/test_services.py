from django.test import TestCase
from ..services import TherapistService
from ..models import Therapist, Region, Province, District
from datetime import date

class TherapistServiceTest(TestCase):
    def setUp(self):
        # Crear datos de ubicación necesarios
        self.region = Region.objects.create(ubigeo_code='15', name='Lima')
        self.province = Province.objects.create(ubigeo_code='1501', name='Lima', region=self.region)
        self.district = District.objects.create(ubigeo_code='150101', name='Lima', province=self.province)
        
        self.therapist = Therapist.objects.create(
            document_type='DNI',
            document_number='12345678',
            last_name_paternal='García',
            last_name_maternal='López',
            first_name='Juan',
            birth_date=date(1990, 1, 1),
            gender='M',
            phone='123456789',
            email='juan@example.com',
            region_fk=self.region,
            province_fk=self.province,
            district_fk=self.district
        )

    def test_get_active_therapists(self):
        active_therapists = TherapistService.get_active_therapists()
        self.assertEqual(active_therapists.count(), 1)
        self.assertIn(self.therapist, active_therapists)

    def test_get_inactive_therapists(self):
        self.therapist.is_active = False
        self.therapist.save()
        inactive_therapists = TherapistService.get_inactive_therapists()
        self.assertEqual(inactive_therapists.count(), 1)
        self.assertIn(self.therapist, inactive_therapists)

    def test_soft_delete_therapist(self):
        result = TherapistService.soft_delete_therapist(self.therapist.id)
        self.assertTrue(result)
        self.therapist.refresh_from_db()
        self.assertFalse(self.therapist.is_active)

    def test_restore_therapist(self):
        self.therapist.is_active = False
        self.therapist.save()
        result = TherapistService.restore_therapist(self.therapist.id)
        self.assertTrue(result)
        self.therapist.refresh_from_db()
        self.assertTrue(self.therapist.is_active)

    def test_search_therapists(self):
        # Buscar por nombre
        found_therapists = TherapistService.search_therapists('Juan')
        self.assertEqual(found_therapists.count(), 1)
        self.assertIn(self.therapist, found_therapists)

        # Buscar por apellido
        found_therapists = TherapistService.search_therapists('García')
        self.assertEqual(found_therapists.count(), 1)
        self.assertIn(self.therapist, found_therapists)

        # Buscar por documento
        found_therapists = TherapistService.search_therapists('12345678')
        self.assertEqual(found_therapists.count(), 1)
        self.assertIn(self.therapist, found_therapists)

        # Buscar por email
        found_therapists = TherapistService.search_therapists('juan@example.com')
        self.assertEqual(found_therapists.count(), 1)
        self.assertIn(self.therapist, found_therapists)

        # Buscar algo que no existe
        found_therapists = TherapistService.search_therapists('NoExiste')
        self.assertEqual(found_therapists.count(), 0)

    def test_soft_delete_therapist_not_found(self):
        result = TherapistService.soft_delete_therapist(99999)
        self.assertFalse(result)

    def test_restore_therapist_not_found(self):
        result = TherapistService.restore_therapist(99999)
        self.assertFalse(result)
