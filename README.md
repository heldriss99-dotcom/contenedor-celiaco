# Sistema de Ubicaciones Sin Gluten - Guatemala

## Descripción
Este proyecto es un sistema web que permite registrar, visualizar y consultar establecimientos que ofrecen opciones libres de gluten en Guatemala.

El sistema incluye funcionalidades de:
- Registro de establecimientos
- Visualización en mapa
- Edición y eliminación de registros
- Consulta por proximidad geográfica

## Tecnologías utilizadas
- Frontend: HTML, CSS, JavaScript, Leaflet
- Backend: FastAPI (Python)
- Base de datos: PostgreSQL + PostGIS
- Contenedores: Docker y Docker Compose
- Proxy: Nginx

## Arquitectura
El sistema está compuesto por tres servicios principales:

- API: Maneja la lógica del sistema y la conexión a la base de datos
- Base de datos: Almacena la información geoespacial
- Web: Interfaz gráfica para el usuario

Todos los servicios están orquestados con Docker Compose.

## Funcionalidades principales

### 1. Registro de establecimientos
Permite guardar:
- Nombre
- Categoría
- Descripción
- Latitud
- Longitud

### 2. Visualización
- Lista de registros
- Visualización en mapa con marcadores

### 3. Edición y eliminación
- Selección de registros
- Modificación de datos
- Eliminación de registros

### 4. Consulta por proximidad
Permite buscar establecimientos cercanos utilizando:
- Latitud
- Longitud
- Radio en metros

Se utilizan funciones geoespaciales de PostGIS como:
- ST_DWithin
- ST_Distance

## Ejecución del proyecto

1. Clonar el repositorio:
```bash
git clone https://github.com/heldriss99-dotcom/contenedor-celiaco.git
