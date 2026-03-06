use std::net::SocketAddr;

use axum::{
    extract::{Query, State},
    http::StatusCode,
    response::IntoResponse,
    routing::get,
    Json, Router,
};
use duckdb::DuckdbConnectionManager;
use r2d2::Pool;
use serde::{Deserialize, Serialize};

/// === 1. Tipos Compartidos (Estado y Conexiones) ===
/// Mantenemos un pool de conexiones a DuckDB vivo para evitar la sobrecarga de apertura.
type DbPool = Pool<DuckdbConnectionManager>;

/// === 2. Modelos de Datos (Serde) ===
/// Estructura para capturar los parámetros de búsqueda de taxonomía.
#[derive(Deserialize)]
struct TaxonQuery {
    /// Género taxonómico (ej. Tapirus)
    genus: String,
    /// Especie taxonómica (ej. terrestris)
    species: String,
}

/// Respuesta estructurada para el cliente (Python/Pydantic).
#[derive(Serialize)]
struct TaxonResponse {
    genus: String,
    species: String,
    is_valid: bool,
    uicn_status: Option<String>,
}

/// === 3. Controladores (Handlers) ===
/// Endpoint básico para verificar la disponibilidad del microservicio.
async fn health_check() -> &'static str {
    "El Túnel de Datos de GeoANLA-ETL en Rust está activo."
}

/// Procesa consultas taxonómicas de alto rendimiento.
async fn check_taxon(
    State(pool): State<DbPool>,
    Query(params): Query<TaxonQuery>,
) -> impl IntoResponse {
    // 3.1 Adquisición de conexión desde el Pool
    let _conn = match pool.get() {
        Ok(c) => c,
        Err(e) => {
            tracing::error!("Error de conexión al pool de DuckDB: {}", e);
            return (
                StatusCode::INTERNAL_SERVER_ERROR,
                Json(serde_json::json!({"error": "DB_POOL_ERROR"})),
            )
                .into_response();
        }
    };

    // 3.2 Lógica de validación optimizada (sin asignaciones innecesarias de String)
    let is_tapir = params.genus.eq_ignore_ascii_case("tapirus") 
        && params.species.eq_ignore_ascii_case("terrestris");

    let uicn_status = if is_tapir {
        Some("Vulnerable (VU)".to_string())
    } else {
        None
    };

    let response = TaxonResponse {
        genus: params.genus,
        species: params.species,
        is_valid: is_tapir,
        uicn_status,
    };

    // 3.3 Respuesta en formato JSON
    (StatusCode::OK, Json(response)).into_response()
}

/// === 4. Inicialización del Servidor (Main) ===
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Configuración de telemetría y logs
    tracing_subscriber::fmt::init();
    tracing::info!("Iniciando motor analítico DuckDB...");

    // 4.1 Inicialización del Pool de Conexiones
    let manager = DuckdbConnectionManager::memory()?;
    let pool = Pool::builder()
        .max_size(15) // Soporta alta concurrencia para procesos ETL
        .build(manager)
        .map_err(|e| {
            tracing::error!("Fallo crítico al inicializar el pool: {}", e);
            e
        })?;

    // 4.2 Definición de rutas y estado compartido
    let app = Router::new()
        .route("/health", get(health_check))
        .route("/api/taxon", get(check_taxon))
        .with_state(pool);

    // 4.3 Configuración y arranque del servidor
    let addr = SocketAddr::from(([127, 0, 0, 1], 8000));
    tracing::info!("🚀 Servidor Rust listo en: http://{}", addr);

    let listener = tokio::net::TcpListener::bind(addr).await?;
    axum::serve(listener, app).await?;

    Ok(())
}
