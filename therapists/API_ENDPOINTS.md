# 🚀 API Documentation - Sistema de Gestión de Terapeutas

## 📋 Resumen Ejecutivo

Este documento describe la **API REST completa** del Sistema de Gestión de Terapeutas, que incluye:
- **Gestión de terapeutas** (CRUD completo con soft delete)
- **Sistema de ubicación geográfica** (solo lectura)

---

## 🌐 Configuración de URLs

### Base URLs
```
Desarrollo local: http://localhost:8000/
Producción: https://tu-dominio.com/
```

### Estructura de URLs
```
/                           → Página principal (interfaz web)
/admin/                     → Panel de administración Django
/therapists/                → API de terapeutas
/regions/                   → API de regiones
/provinces/                 → API de provincias
/districts/                 → API de distritos
```

---

## 🔌 APIs Externas (Endpoints Públicos)

### 1. 🧑‍⚕️ **API de Terapeutas** (`/therapists/`)

#### Operaciones CRUD Básicas
| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| **GET** | `/therapists/` | Listar terapeutas | Query params |
| **POST** | `/therapists/` | Crear terapeuta | JSON body |
| **GET** | `/therapists/{id}/` | Obtener terapeuta | `id` en path |
| **PUT** | `/therapists/{id}/` | Actualizar terapeuta | `id` + JSON body |
| **PATCH** | `/therapists/{id}/` | Actualizar parcial | `id` + JSON body |
| **DELETE** | `/therapists/{id}/` | Soft delete | `id` en path |

#### Endpoints Especiales
| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| **GET** | `/therapists/inactive/` | Listar inactivos | Query params |
| **POST** | `/therapists/{id}/restore/` | Restaurar terapeuta | `id` en path |

#### Parámetros de Filtrado
```
GET /therapists/?active=true          # Solo activos (por defecto)
GET /therapists/?active=false         # Solo inactivos
GET /therapists/?region=15            # Por ID de región
GET /therapists/?province=1501        # Por ID de provincia
GET /therapists/?district=150101      # Por ID de distrito
GET /therapists/?search=ana           # Búsqueda por texto
```

#### Campos de Búsqueda
- `first_name` - Nombre
- `last_name_paternal` - Apellido paterno
- `last_name_maternal` - Apellido materno
- `document_number` - Número de documento
- `document_type` - Tipo de documento
- `email` - Correo electrónico
- `phone` - Teléfono
- `address` - Dirección
- `region_fk__name` - Nombre de región
- `province_fk__name` - Nombre de provincia
- `district_fk__name` - Nombre de distrito

---

### 2. 🌍 **API de Regiones** (`/regions/`)

#### Operaciones de Solo Lectura
| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| **GET** | `/regions/` | Listar regiones | - |
| **GET** | `/regions/{id}/` | Obtener región | `id` en path |

---

### 3. 🏙️ **API de Provincias** (`/provinces/`)

#### Operaciones de Solo Lectura
| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| **GET** | `/provinces/` | Listar provincias | - |
| **GET** | `/provinces/{id}/` | Obtener provincia | `id` en path |

---

### 4. 🏘️ **API de Distritos** (`/districts/`)

#### Operaciones de Solo Lectura
| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| **GET** | `/districts/` | Listar distritos | - |
| **GET** | `/districts/{id}/` | Obtener distrito | `id` en path |

---

## 📊 Estructura de Datos

### Modelo Therapist
```python
class Therapist(models.Model):
    # Datos personales
    document_type = models.CharField(max_length=10, choices=DOCUMENT_TYPES)
    document_number = models.CharField(max_length=20, unique=True)
    last_name_paternal = models.CharField(max_length=100)
    last_name_maternal = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDERS)
    personal_reference = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(choices=STATUS, default=True)

    # Información de contacto
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)

    # Ubicación con FK
    region_fk = models.ForeignKey(Region, on_delete=models.PROTECT, null=True, blank=True)
    province_fk = models.ForeignKey(Province, on_delete=models.PROTECT, null=True, blank=True)
    district_fk = models.ForeignKey(District, on_delete=models.PROTECT, null=True, blank=True)

    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)
```

### Modelos de Ubicación
```python
class Region(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

class Province(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

class District(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
```

---

## 🛠️ Servicios Disponibles

### Estructura de Servicios
```
therapists/services/
├── __init__.py
└── therapist_service.py    # Lógica de terapeutas
```

### TherapistService
```python
from therapists.services import TherapistService

# Crear instancia del servicio
service = TherapistService()

# Operaciones disponibles
all_therapists = service.get_all_therapists()
therapist_by_id = service.get_therapist_by_id(1)
```

---

## 🔍 Filtros y Búsqueda

### Filtros por Ubicación
- **Por Región**: `GET /therapists/?region=15`
- **Por Provincia**: `GET /therapists/?province=1501`
- **Por Distrito**: `GET /therapists/?district=150101`

### Filtros por Estado
- **Solo Activos**: `GET /therapists/?active=true`
- **Solo Inactivos**: `GET /therapists/?active=false`

### Búsqueda por Texto
- **Búsqueda General**: `GET /therapists/?search=ana`
- **Búsqueda por Documento**: `GET /therapists/?search=12345678`
- **Búsqueda por Email**: `GET /therapists/?search=ana@example.com`

---

## 📝 Ejemplos de Uso

### Crear un Terapeuta
```bash
curl -X POST http://localhost:8000/therapists/ \
  -H "Content-Type: application/json" \
  -d '{
    "document_type": "DNI",
    "document_number": "12345678",
    "first_name": "Ana",
    "last_name_paternal": "García",
    "last_name_maternal": "López",
    "birth_date": "1990-01-01",
    "gender": "F",
    "phone": "999999999",
    "email": "ana@example.com",
    "region_fk": 15,
    "province_fk": 1501,
    "district_fk": 150101,
    "address": "Av. Siempre Viva 123"
  }'
```

### Obtener Terapeutas por Región
```bash
curl "http://localhost:8000/therapists/?region=15"
```

### Buscar Terapeutas por Nombre
```bash
curl "http://localhost:8000/therapists/?search=ana"
```

---

## ✅ Características Implementadas

- [x] CRUD completo de terapeutas
- [x] Soft delete y restauración
- [x] Búsqueda y filtrado avanzado
- [x] Sistema de ubicación geográfica
- [x] Validaciones robustas
- [x] API REST completa
- [x] Documentación detallada

---

## 🚫 Funcionalidades No Implementadas

- ❌ Gestión de especialidades médicas
- ❌ Gestión de certificaciones profesionales
- ❌ Gestión de horarios y disponibilidad
- ❌ Sistema de citas o reservas
- ❌ Gestión de pacientes
- ❌ Sistema de pagos
