import requests
import time
import pandas as pd
import geopandas as gpd
from typing import List, Dict, Any, Optional

def batch_elevation_lookup(
    gdf_puntos: gpd.GeoDataFrame,
    tamano_lote: int = 50,
    tiempo_espera: float = 0.5,
    crs_origen: str = "EPSG:9377"
) -> gpd.GeoDataFrame:
    """
    Consulta la API de Open Elevation para obtener la cota (elevación)
    de un GeoDataFrame de puntos.

    Args:
        gdf_puntos: GeoDataFrame con geometría de puntos.
        tamano_lote: Tamaño del lote para la API (default 50).
        tiempo_espera: Tiempo de espera entre peticiones (default 0.5s).
        crs_origen: CRS de origen si el GDF no tiene uno asignado.

    Returns:
        GeoDataFrame con una nueva columna 'COTA' (o actualizada).
    """
    df_copia = gdf_puntos.copy()

    # 1. Asegurar CRS y proyectar a WGS84 para la API
    if df_copia.crs is None:
        print(f"⚠️ Asignando {crs_origen} por defecto.")
        df_copia.set_crs(crs_origen, inplace=True)

    # Proyectamos temporalmente a Lat/Lon
    gdf_proyectado = df_copia.to_crs(epsg=4326)


    # Open-Meteo recibe arrays de latitudes y longitudes separados por coma
    latitudes = [str(punto.y) for punto in gdf_proyectado.geometry]
    longitudes = [str(punto.x) for punto in gdf_proyectado.geometry]

    # 2. Consulta a la API
    url_api = 'https://api.open-meteo.com/v1/elevation'
    elevaciones = []
    total_puntos = len(latitudes)

    print(f"🚀 Iniciando consulta de elevación para {total_puntos} puntos en Open-Meteo...")

    for i in range(0, total_puntos, tamano_lote):
        lat_lote = ",".join(latitudes[i : i + tamano_lote])
        lon_lote = ",".join(longitudes[i : i + tamano_lote])
        print(f"   Procesando lote {i} a {min(i + tamano_lote, total_puntos)}...")

        try:
            # Petición GET con parámetros de query
            respuesta = requests.get(
                url_api, 
                params={'latitude': lat_lote, 'longitude': lon_lote},
                timeout=30
            )
            
            if respuesta.status_code == 200:
                datos_respuesta = respuesta.json()
                # Open-Meteo devuelve la lista bajo la llave 'elevation'
                cotas_lote = datos_respuesta.get('elevation', [])
                elevaciones.extend(cotas_lote)
            else:
                msg_error = f"   ⚠️ Error de API (Status {respuesta.status_code})."
                print(f"{msg_error} Asignando None.")
                elevaciones.extend([None] * len(latitudes[i : i + tamano_lote]))
                
        except requests.exceptions.RequestException as error_red:
            print(f"   ❌ Error de conexión: {error_red}")
            elevaciones.extend([None] * len(latitudes[i : i + tamano_lote]))

        if i + tamano_lote < total_puntos:
            time.sleep(tiempo_espera)

    # 3. Asignar resultados
    df_copia['COTA'] = elevaciones
    print("✅ Proceso de elevación finalizado.")
    return df_copia
