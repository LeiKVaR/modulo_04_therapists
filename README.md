# Módulo 4 - Sistema de Gestión de Terapeutas

## Descripción

Este módulo proporciona un sistema completo para la gestión de terapeutas, especialidades médicas y ubicaciones geográficas. Implementa una API REST y vistas web para acceder y manipular información de terapeutas, especializaciones, certificaciones, horarios y datos de ubicación (regiones, provincias y distritos).

## Características Principales

- **API REST completa**: Endpoints para operaciones CRUD en todas las entidades del sistema
- **Gestión de terapeutas**: Sistema completo de registro y administración de profesionales de la salud
- **Especialidades médicas**: Categorización y gestión de especialidades terapéuticas
- **Certificaciones**: Control de certificaciones y credenciales profesionales
- **Horarios y disponibilidad**: Gestión de agendas y horarios de atención
- **Sistema de ubicación**: Integración con datos geográficos (regiones, provincias, distritos)
- **Interfaz web**: Vistas HTML para explorar y gestionar los datos
- **Importación de datos**: Comandos para importar datos geográficos desde archivos CSV
- **Pruebas unitarias**: Cobertura completa de modelos, servicios y vistas

## Estructura del Proyecto

- **therapists_project/**: Configuración principal del proyecto Django
- **therapists/**: Aplicación principal con la lógica de negocio
  - **models/**: Definición de modelos de datos (terapeutas, especialidades, ubicaciones, etc.)
  - **views/**: Vistas y controladores para la API y páginas web
  - **serializers/**: Serializadores para la API REST
  - **services/**: Lógica de negocio y servicios
  - **management/**: Comandos personalizados de Django
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
   python manage.py migrate
   ```

5. Importa los datos geográficos:
   ```bash
   python manage.py import_ubigeo --file=db/regions.csv
   python manage.py import_ubigeo --file=db/provinces.csv
   python manage.py import_ubigeo --file=db/districts.csv
   ```

6. Inicia el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```

## Uso de la API

Consulta la documentación detallada en `therapists/API_ENDPOINTS.md` para ver todos los endpoints disponibles.

Ejemplos básicos:

- Listar terapeutas: `GET /api/therapists/`
- Crear terapeuta: `POST /api/therapists/`
- Obtener especialidades: `GET /api/specializations/`
- Obtener provincias de una región: `GET /api/regions/{region_id}/provinces/`
- Obtener distritos de una provincia: `GET /api/provinces/{province_id}/districts/`

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

O utilizando pytest:

```bash
pytest
```

## Documentación Adicional

Cada carpeta del proyecto contiene un archivo README.md con documentación específica:

- **therapists_project/README.md**: Configuración y estructura del proyecto Django
- **therapists/README.md**: Estructura general de la aplicación
- **therapists/API_ENDPOINTS.md**: Documentación completa de todos los endpoints de la API
- **therapists/models/README.md**: Modelos de datos
- **therapists/views/README.md**: Vistas y controladores
- **therapists/serializers/README.md**: Serializadores para la API
- **therapists/services/README.md**: Servicios y lógica de negocio
- **therapists/test/README.md**: Pruebas unitarias y de integración
- **therapists/management/commands/README.md**: Comandos personalizados
- **db/README.md**: Datos geográficos en CSV

## Contribución

1. Haz un fork del repositorio
2. Crea una rama para tu funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Realiza tus cambios y haz commit (`git commit -am 'Agrega nueva funcionalidad'`)
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT.