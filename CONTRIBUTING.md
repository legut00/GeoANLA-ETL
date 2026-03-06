# Guía de Contribución para GeoANLA-ETL

¡Gracias por tu interés en contribuir a GeoANLA-ETL! Este proyecto es un pipeline de ETL de alto rendimiento diseñado para la gestión de datos ambientales, combinando la flexibilidad de Python con la potencia bruta de Rust.

## Tabla de Contenidos

- [Alcance del Proyecto](#alcance-del-proyecto)
- [Convenciones de Idioma (Regla Bilingüe)](#convenciones-de-idioma-regla-bilingüe)
- [Estándares de Codificación](#estándares-de-codificación)
  - [Python (Pydantic y PEP 8)](#python-pydantic-y-pep-8)
  - [Rust (Seguridad y Rendimiento)](#rust-seguridad-y-rendimiento)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Flujo de Trabajo de Desarrollo](#flujo-de-trabajo-de-desarrollo)
- [Mensajes de Commit](#mensajes-de-commit)

---

## Alcance del Proyecto

GeoANLA-ETL se centra en la extracción, transformación y validación de capas GDB (Geodatabase) para el licenciamiento ambiental. Priorizamos:
- **Integridad Espacial**: Intersecciones y transformaciones de coordenadas precisas.
- **Rendimiento**: Procesamiento de datos a gran escala.
- **Validación**: Aplicación estricta de esquemas a través de modelos.

## Convenciones de Idioma (Regla Bilingüe)

Para mantener un flujo de trabajo profesional y avanzado, seguimos una estricta convención de doble idioma. **El incumplimiento de esta regla resultará en el rechazo del PR.**

### 🐍 Python
- **Inglés (Lógica Interna)**: Todas las funciones, métodos, clases, tipos y constantes internas deben estar en inglés.
  - *Correcto*: `def validate_intersection(self):`
  - *Incorrecto*: `def validar_interseccion(self):`
- **Español (Comunicación y Documentación)**: Las variables, atributos, comentarios y docstrings deben estar en español.
  - *Correcto*: `expediente_id = "2024-001"  # Identificador único del trámite`
  - *Incorrecto*: `record_id = "2024-001"  # Unique record identifier`

### 🦀 Rust
- **Inglés (Lógica Interna)**: Todas las variables, tipos, funciones y módulos deben estar en inglés.
  - *Correcto*: `let is_active: bool = true;`
  - *Incorrecto*: `let esta_activo: bool = true;`
- **Español (Comunicación y Logs)**: Los mensajes de log (`tracing::info!`), mensajes de error y documentación (`///`) deben estar en español.
  - *Correcto*: `tracing::info!("Conexión exitosa a la base de datos.");`
  - *Incorrecto*: `tracing::info!("Successful connection to the database.");`

---

## Estándares de Codificación

### Python (Pydantic y PEP 8)
- **Cumplimiento**: Seguir PEP 8 estrictamente (4 espacios, longitud de línea < 88).
- **Tipado**: Uso obligatorio de Pydantic para modelos y "type hints" para funciones.
- **Validadores**: Usar nombres en inglés para `field_validator` y `model_validator`.
- **Acceso a Propiedades**: Priorizar nombres de propiedades en inglés en los catálogos (ej. usar `.description` en lugar de `.descripcion`).

### Rust (Seguridad y Rendimiento)
- **Rust Idiomático**: Evitar `.clone()` innecesarios. Usar referencias y préstamos (borrowing).
- **Manejo de Errores**: Usar el operador `?` y `Result`. **Evitar explícitamente `.unwrap()` o `.expect()`** en manejadores o módulos de lógica.
- **Importaciones**: Agrupar importaciones en este orden: `std`, crates externos, módulos locales.
- **Rendimiento**: Aprovechar `eq_ignore_ascii_case` para operaciones que no distingan mayúsculas de minúsculas.

---

## Estructura del Proyecto

```text
GeoANLA-ETL/
├── src/geoanla/
│   ├── catalog/         # Enums de dominio y catálogos dinámicos
│   ├── core/            # Clases base de validación
│   ├── models/          # Modelos Pydantic para tablas GDB
│   └── utils/           # Ayudantes geográficos y taxonómicos
├── rust_tunnel/         # Microservicio Rust de alto rendimiento
│   ├── src/             # Manejadores Axum y lógica DuckDB
│   └── Cargo.toml
├── data/                # Muestras de datos y CSVs de referencia
└── CONTRIBUTING.md
```

## Flujo de Trabajo de Desarrollo

1. **Configuración**: Instalar dependencias de Python con `pip install -e .` y asegurar que Rust esté instalado.
2. **Ramas (Branching)**: Usar nombres descriptivos (`feature/`, `fix/`, `refactor/`).
3. **Compilación de Rust**: Verificar cambios en el túnel usando `cargo check`.
4. **Validación**: Asegurar que todos los modelos Pydantic pasen sus pruebas de validación local.

## Mensajes de Commit

Seguimos los [Commits Convencionales](https://www.conventionalcommits.org/):

- `feat`: Nueva funcionalidad (ej. `feat: agregar coordenadas al módulo utils`)
- `fix`: Corrección de error (ej. `fix: resolver la ruta de los municipios`)
- `refactor`: Cambio de código que no corrige un error ni añade funcionalidad
- `docs`: Cambios solo en la documentación

---

¡Gracias por hacer de GeoANLA-ETL un proyecto mejor!
