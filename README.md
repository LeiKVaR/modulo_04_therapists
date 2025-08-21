# Módulo 4 - Sistema de Gestión de Terapeutas

## Descripción

Este módulo proporciona un sistema completo para la gestión de terapeutas y ubicaciones geográficas. Implementa una API REST y vistas web para acceder y manipular información de terapeutas y datos de ubicación (regiones, provincias y distritos).

## Características Principales

- **API REST completa**: Endpoints para operaciones CRUD en terapeutas y ubicación geográfica
- **Gestión de terapeutas**: Sistema completo de registro y administración de profesionales de la salud
- **Sistema de ubicación**: Integración con datos geográficos (regiones, provincias, distritos)
- **Interfaz web**: Vistas HTML para explorar y gestionar los datos
- **Importación de datos**: Comandos para importar datos geográficos desde archivos CSV
- **Pruebas unitarias**: Cobertura completa de modelos, servicios y vistas

## Estructura del Proyecto

- **therapists_project/**: Configuración principal del proyecto Django
- **therapists/**: Aplicación principal con la lógica de negocio
  - **models/**: Definición de modelos de datos (terapeutas, ubicaciones)
  - **views/**: Vistas y controladores para la API y páginas web
  - **serializers/**: Serializadores para la API REST
  - **services/**: Lógica de negocio y servicios
  - **management/commands/**: Comandos personalizados de Django
  - **tests/**: Pruebas unitarias y de integración
- **db/**: Archivos CSV con datos geográficos (regiones, provincias, distritos)

## Requisitos

- Python 3.8+
- Django 5.2+
- Django Rest Framework 3.12+
- Otras dependencias listadas en requirements.txt

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/modulo_04_therapists.git
   cd modulo_04_therapists
   ```

2. Crea y activa un entorno virtual:
   ```bash
   python -m venv env
   source env/bin/activate  # En Windows: env\Scripts\activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Aplica las migraciones:
   ```bash
   python manage.py makemigrations
   ```

   ```bash
   python manage.py migrate
   ```

5. Importa los datos geográficos:
   ```bash
   python manage.py import_ubigeo --path db --truncate
   ```

6. Inicia el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```

## Uso de la API

Consulta la documentación detallada en `therapists/API_ENDPOINTS.md` para ver todos los endpoints disponibles.

Ejemplos básicos:

- Listar terapeutas: `GET /therapists/`
- Crear terapeuta: `POST /therapists/`
- Obtener regiones: `GET /regions/`
- Obtener provincias de una región: `GET /provinces/?region={region_id}`
- Obtener distritos de una provincia: `GET /districts/?province={province_id}`

## Integración con Otros Módulos

Este módulo está diseñado para ser utilizado por otros módulos del sistema. Para integrarlo:

1. Incluye este módulo como dependencia en tu proyecto
2. Utiliza los endpoints de la API para obtener y manipular datos de terapeutas y ubicaciones
3. Importa los modelos y servicios necesarios para acceder directamente a la lógica de negocio

## Pruebas

Ejecuta las pruebas unitarias y de integración:

```bash
python manage.py test
```

O usando pytest:

```bash
pytest
```

## Estructura de la Aplicación

### Modelos
- `therapist.py`: Modelo principal de terapeutas
- `region.py`: Modelo de regiones geográficas
- `province.py`: Modelo de provincias geográficas
- `district.py`: Modelo de distritos geográficos

### Vistas
- `therapist.py`: Vistas para gestión de terapeutas
- `location.py`: Vistas para ubicaciones
- `region.py`: Vistas para regiones
- `province.py`: Vistas para provincias
- `district.py`: Vistas para distritos

### Serializers
- `therapist.py`: Serializadores para terapeutas
- `location.py`: Serializadores para ubicaciones

### Servicios
- `therapist_service.py`: Lógica para terapeutas

## Funcionalidades Implementadas

- ✅ CRUD completo de terapeutas
- ✅ Soft delete y restauración
- ✅ Búsqueda y filtrado avanzado
- ✅ Sistema de ubicación geográfica
- ✅ Validaciones robustas
- ✅ API REST completa
- ✅ Documentación detallada

## Funcionalidades No Implementadas

- ❌ Gestión de especialidades médicas
- ❌ Gestión de certificaciones profesionales
- ❌ Gestión de horarios y disponibilidad
- ❌ Sistema de citas o reservas
- ❌ Gestión de pacientes
- ❌ Sistema de pagos

## Documentación

- **README.md** (este archivo): Documentación general del proyecto
- **therapists/README.md**: Estructura detallada de la aplicación
- **therapists/API_ENDPOINTS.md**: Documentación completa de la API

## Contribución

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature
3. Realiza los cambios necesarios
4. Ejecuta las pruebas
5. Envía un pull request

## Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo LICENSE para más detalles.