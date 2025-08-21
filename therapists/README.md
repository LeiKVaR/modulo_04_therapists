# 📦 therapists

Carpeta principal de la aplicación Django para la gestión de terapeutas y ubicación geográfica.

---

## 📁 Estructura y Archivos

```
therapists/
├── __init__.py
├── admin.py
├── apps.py
├── migrations/
│   ├── __init__.py
│   └── [archivos de migración]
├── models/
│   ├── __init__.py
│   ├── therapist.py
│   ├── region.py
│   ├── province.py
│   └── district.py
├── views/
│   ├── __init__.py
│   ├── therapist.py
│   ├── location.py
│   ├── region.py
│   ├── province.py
│   └── district.py
├── serializers/
│   ├── __init__.py
│   ├── therapist.py
│   └── location.py
├── services/
│   ├── __init__.py
│   └── therapist_service.py
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_views.py
│   ├── test_services.py
│   └── conftest.py
├── management/
│   └── commands/
│       ├── __init__.py
│       └── import_ubigeo.py
├── urls.py
├── README.md
└── API_ENDPOINTS.md
```

- **`__init__.py`**  
  Inicializa el paquete Python de la app.

- **`admin.py`**  
  Configura la administración de modelos en el panel de Django.

- **`apps.py`**  
  Configuración de la app para Django.

- **`migrations/`**  
  Archivos de migración para la base de datos.

- **`models/`**  
  Define los modelos de datos organizados por funcionalidad:
  - `therapist.py`: Modelo principal de terapeutas con campos personales, contacto y ubicación geográfica
  - `region.py`, `province.py`, `district.py`: Modelos de ubicación geográfica (sistema de ubigeo)

- **`views/`**  
  Vistas y controladores organizados por funcionalidad:
  - `therapist.py`: Vistas para gestión de terapeutas (CRUD completo con soft delete)
  - `location.py`, `region.py`, `province.py`, `district.py`: Vistas para ubicaciones geográficas

- **`serializers/`**  
  Serializadores para la API REST organizados por funcionalidad:
  - `therapist.py`: Serializadores para terapeutas con validaciones y campos anidados
  - `location.py`: Serializadores para ubicaciones

- **`services/`**  
  Lógica de negocio y servicios organizados por funcionalidad:
  - `therapist_service.py`: Lógica para terapeutas (CRUD, soft delete, restauración)

- **`tests/`**  
  Pruebas unitarias y de integración:
  - `test_models.py`: Pruebas de modelos
  - `test_views.py`: Pruebas de vistas
  - `test_services.py`: Pruebas de servicios
  - `conftest.py`: Configuración de pytest

- **`management/commands/`**  
  Comandos personalizados de Django:
  - `import_ubigeo.py`: Comando para importar datos geográficos desde CSV

- **`urls.py`**  
  Rutas específicas de la app, conectando los endpoints API y vistas web.

- **`API_ENDPOINTS.md`**  
  Documentación completa de todos los endpoints de la API.

---

## 🔗 Rutas Principales (urls.py)

**Archivo:**  
- `therapists/urls.py`

**Responsabilidad:**  
Define las rutas de la app, conectando los endpoints RESTful y vistas web.

### Rutas definidas

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'therapists', TherapistViewSet, basename='therapist')
router.register(r"regions", RegionViewSet, basename="region")
router.register(r"provinces", ProvinceViewSet, basename="province")
router.register(r"districts", DistrictViewSet, basename="district")

urlpatterns = [
    path('', index, name='therapists_index'),  # Página principal en /
    path('', include(router.urls)),  # APIs disponibles en la raíz
]
```

---

## 🗂️ Documentación de Endpoints API

**Archivo:**  
- `therapists/API_ENDPOINTS.md`

### Endpoints disponibles

| Método | Ruta                          | Descripción                                 | Parámetros         |
|--------|-------------------------------|---------------------------------------------|--------------------|
| GET    | `/therapists/`                | Lista todos los terapeutas                  | `search`, `active`, `region`, `province`, `district` |
| POST   | `/therapists/`                | Crea un nuevo terapeuta                     | JSON body          |
| GET    | `/therapists/<id>/`           | Obtiene un terapeuta específico             | `id` (path)        |
| PUT    | `/therapists/<id>/`           | Actualiza un terapeuta                      | `id` (path), body  |
| PATCH  | `/therapists/<id>/`           | Actualiza parcialmente un terapeuta         | `id` (path), body  |
| DELETE | `/therapists/<id>/`           | Soft delete de un terapeuta                 | `id` (path)        |
| GET    | `/therapists/inactive/`       | Lista terapeutas inactivos                  | Query params       |
| POST   | `/therapists/<id>/restore/`   | Restaura un terapeuta eliminado             | `id` (path)        |

#### Ejemplo de respuesta (GET `/therapists/`):

```json
[
    {
        "id": 1,
        "region_fk": 1,
        "province_fk": 1,
        "district_fk": 1,
        "document_type": "DNI",
        "document_number": "75195815",
        "last_name_paternal": "El tesyet",
        "last_name_maternal": "User",
        "first_name": "API",
        "birth_date": "1990-01-24",
        "gender": "M",
        "personal_reference": "",
        "is_active": true,
        "phone": "999999999",
        "email": "test_unop@gmail.com",
        "address": "",
        "profile_picture": null
    }
]
```

---

## 🛠️ Tecnologías y Dependencias

- **Django**: Framework principal del backend.
- **Django REST Framework**: Para la creación de la API REST.
- **SQLite**: Base de datos por defecto (puede cambiarse en producción).
- **Pillow**: Manejo de imágenes (para fotos de perfil).
- **pytest**: Framework de testing.

**Dependencias en `requirements.txt`:**
```
Django>=5.2
djangorestframework
django-cors-headers
Pillow
pytest
pytest-django
```

---

## 🔍 Características Principales

### Gestión de Terapeutas
- **CRUD completo** con operaciones de creación, lectura, actualización y eliminación
- **Soft delete** para mantener historial de terapeutas eliminados
- **Restauración** de terapeutas eliminados
- **Búsqueda avanzada** por múltiples criterios
- **Filtrado geográfico** por región, provincia y distrito

### Sistema de Ubicación
- **Modelo de ubigeo** completo (región, provincia, distrito)
- **Relaciones jerárquicas** entre entidades geográficas
- **Comando de importación** para datos geográficos desde CSV

### API REST
- **Endpoints RESTful** para terapeutas y ubicación geográfica
- **Serialización inteligente** con campos anidados
- **Validaciones robustas** en entrada de datos
- **Filtrado y búsqueda** avanzados

---

## ✅ Checklist de Documentación

- [x] Estructura de archivos explicada
- [x] Rutas principales documentadas
- [x] Ejemplo de endpoints y respuestas
- [x] Tecnologías y dependencias listadas
- [x] Estructura organizada por funcionalidad
- [x] Características principales documentadas
- [x] Información de modelos actualizada
- [x] Endpoints reales documentados
- [x] Eliminadas referencias a funcionalidades no implementadas