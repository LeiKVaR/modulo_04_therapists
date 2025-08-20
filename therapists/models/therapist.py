from django.db import models
from Reflexo.models import Region, Province, District

class Therapist(models.Model):
    # Datos personales
    document_type = models.CharField(max_length=50)  # Tipo de Documento
    document_number = models.CharField(max_length=20, unique=True)  # Nro Documento
    last_name_paternal = models.CharField(max_length=100)  # Apellido Paterno
    last_name_maternal = models.CharField(max_length=100, blank=True, null=True)  # Apellido Materno
    first_name = models.CharField(max_length=100)  # Nombre
    birth_date = models.DateField()  # Fecha de Nacimiento
    gender = models.CharField(max_length=20)  # Sexo
    personal_reference = models.CharField(max_length=255, blank=True, null=True)  # Referencia Personal
    is_active = models.BooleanField(default=True)

    # Información de contacto
    phone = models.CharField(max_length=15)  # Teléfono
    email = models.EmailField(blank=True, null=True)  # Correo Electrónico
    
    # Ubicación usando relaciones con Reflexo
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Región")
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Provincia")
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Distrito")
    
    # Campos de texto para compatibilidad (opcionales)
    address = models.TextField(blank=True, null=True)  # Dirección de Domicilio
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True) # Foto de Perfil

    def __str__(self):
        return f"{self.first_name} {self.last_name_paternal} {self.last_name_maternal or ''}"
    
    class Meta:
        verbose_name = "Terapeuta"
        verbose_name_plural = "Terapeutas"
