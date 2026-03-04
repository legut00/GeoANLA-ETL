use axum::{
    extract::{Query, State},
    http::StatusCode,
    response::IntoResponse,
    routing::get,
    Json, Router,
};
use r2d2::Pool;
use r2d2_duckdb::DuckdbConnectionManager;
use serde::{Deserialize, Serialize};
use std::net::SocketAddr;
use tracing_subscriber;

// === 1. Tipos Compartidos (Estado y Conexiones) ===
// Mantenemos un pool de conexiones a DuckDB vivo para no abrir el origen por cada Request
type DbPool = Pool<DuckdbConnectionManager>;

// === 2. Modelos Pydantic <-> Rust (Serde) ===
// Lo que Python (Pydantic) nos preguntará: GET /api/taxon?genero=Tapirus&especie=terrestris
#[derive(Deserialize)]
struct TaxonQuery {
    genero: String,
    especie: String,
}

// Lo que Rust le devolverá a Python: JSON limpio
#[derive(Serialize)]
struct TaxonResponse {
    genero: String,
    especie: String,
    es_valido: bool,
    status_uicn: Option<String>,
}

// === 3. Rutas (Handlers) ===
// Endpoint de prueba rápida para que Python sepa si el servidor levantó
async fn health_check() -> &'static str {
    "El Túnel de Datos de GeoANLA-ETL en Rust está vivo y respirando."
}

// El Endpoint pesado: la consulta que reemplazaría la petición de red
async fn check_taxon(
    State(pool): State<DbPool>,
    Query(params): Query<TaxonQuery>,
) -> impl IntoResponse {
    // 3.1 Tomamos una conexión libre del Pool
    let conn = match pool.get() {
        Ok(c) => c,
        Err(e) => {
            tracing::error!("Error obteniendo conexión a DuckDB: {}", e);
            return (StatusCode::INTERNAL_SERVER_ERROR, Json(serde_json::json!({"error": "DB_POOL_ERROR"}))).into_response();
        }
    };

    // 3.2 Hacemos la consulta a Parquet ultra rápida (esto es un ejemplo simulado)
    // En el futuro cambiarás esto por la query real a tu parquet de GBIF/SiB.
    let genero_buscado = params.genero.to_lowercase();
    let especie_buscada = params.especie.to_lowercase();

    // Solo como demostración: simulamos que encontramos un Tapir
    let es_valido = genero_buscado == "tapirus" && especie_buscada == "terrestris";
    let status_uicn = if es_valido {
        Some("Vulnerable (VU)".to_string())
    } else {
        None
    };

    let respuesta = TaxonResponse {
        genero: params.genero,
        especie: params.especie,
        es_valido,
        status_uicn,
    };

    // 3.3 Devolvemos un OK (200) con el JSON puro hacia Python
    (StatusCode::OK, Json(respuesta)).into_response()
}


// === 4. Punto de Entrada (Main) ===
#[tokio::main]
async fn main() {
    // Inicializar logs coloridos
    tracing_subscriber::fmt::init();
    tracing::info!("Iniciando motor de DuckDB en memoria...");

    // 4.1 Configurar el motor analítico DuckDB
    // Por ahora en memoria. Luego puedes usar "./data/db_completa.duckdb" o simplemente leer parquets en memoria
    let manager = DuckdbConnectionManager::memory().unwrap();
    let pool = Pool::builder()
        .max_size(15) // Maneja 15 hilos concurrentes de Python consultando la DB sin sudar
        .build(manager)
        .expect("Revisa tu entorno, no se pudo crear el Pool de conexiones a DuckDB.");

    // 4.2 Armar el enrutador de Axum y compartirle el Pool (Estado) a las rutas
    let app = Router::new()
        .route("/health", get(health_check))
        .route("/api/taxon", get(check_taxon))
        .with_state(pool);

    // 4.3 Abrir el puerto y arrancar el servidor asíncrono
    let addr = SocketAddr::from(([127, 0, 0, 1], 8000));
    tracing::info!("🚀 ¡Túnel de Datos listo! Escuchando peticiones en HTTP://{}", addr);
    
    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
