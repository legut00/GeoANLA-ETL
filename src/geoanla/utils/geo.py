import requests
import time
import pandas as pd
import geopandas as gpd
from typing import List, Dict, Any, Optional

def batch_elevation_lookup(
    gdf: gpd.GeoDataFrame, 
    batch_size: int = 50, 
    sleep_time: float = 0.5,
    source_crs: str = "EPSG:9377"
) -> gpd.GeoDataFrame:
    """
    Consulta la API de Open Elevation para obtener la cota (elevación) 
    de un GeoDataFrame de puntos.
    
    Args:
        gdf: GeoDataFrame con geometría de puntos.
        batch_size: Tamaño del lote para la API (default 50).
        sleep_time: Tiempo de espera entre peticiones (default 0.5s).
        source_crs: CRS de origen si el GDF no tiene uno asignado.
        
    Returns:
        GeoDataFrame con una nueva columna 'COTA' (o actualizada).
    """
    df = gdf.copy()
    
    # 1. Asegurar CRS y proyectar a WGS84 para la API
    if df.crs is None:
        print(f"⚠️ Asignando {source_crs} por defecto.")
        df.set_crs(source_crs, inplace=True)
    
    # Proyectamos temporalmente a Lat/Lon
    gdf_wgs84 = df.to_crs(epsg=4326)
    locations = [{"latitude": p.y, "longitude": p.x} for p in gdf_wgs84.geometry]
    
    # 2. Consulta a la API
    url = 'https://api.open-elevation.com/api/v1/lookup'
    elevaciones = []
    total_puntos = len(locations)
    
    print(f"🚀 Iniciando consulta de elevación para {total_puntos} puntos...")
    
    for i in range(0, total_puntos, batch_size):
        batch = locations[i : i + batch_size]
        print(f"   Procesando lote {i} a {min(i + batch_size, total_puntos)}...")
        
        try:
            response = requests.post(url, json={'locations': batch}, timeout=30)
            if response.status_code == 200:
                data_resp = response.json()
                batch_elevs = [item['elevation'] for item in data_resp['results']]
                elevaciones.extend(batch_elevs)
            else:
                print(f"   ⚠️ Error de API (Status {response.status_code}). Asignando None.")
                elevaciones.extend([None] * len(batch))
        except Exception as e:
            print(f"   ❌ Error de conexión: {e}")
            elevaciones.extend([None] * len(batch))
            
        if i + batch_size < total_puntos:
            time.sleep(sleep_time)
            
    # 3. Asignar resultados
    df['COTA'] = elevaciones
    print("✅ Proceso de elevación finalizado.")
    return df
