import os
import requests
from dotenv import load_dotenv
from typing import Optional, Union, List, Dict
from pygbif import occurrences

# Cargar variables de entorno (por si el usuario tiene un .env local)
load_dotenv()
from pygbif import occurrences

# Importar los dominios desde el catálogo oficial
from geoanla.catalog.corineland import (
    Dom_CateCober,
    Dom_SubcatCober,
    Dom_Clas_Cober,
    Dom_Subclas_Cober,
    Dom_Nivel5_Cober,
    Dom_Nivel6_Cober
)
from geoanla.catalog.domains import Dom_Amenaza

def search_corine_land_cover(
    NOMENCLAT: Optional[Union[int, float]] = None,
    q: Optional[str] = None
) -> List[Dict[str, Union[float, str]]]:
    """
    Busca en el catálogo de Corine Land Cover por código (NOMENCLAT) o por texto (q).
    
    :param NOMENCLAT: [int/float] Código numérico de la cobertura (e.g., 111, 311.0).
    :param q: [str] Palabra clave o frase para buscar en las leyendas.
    :return: Una lista de diccionarios con las coincidencias encontradas.
    """
    # Recopilar todos los dominios oficiales
    dominios = [
        Dom_CateCober,
        Dom_SubcatCober,
        Dom_Clas_Cober,
        Dom_Subclas_Cober,
        Dom_Nivel5_Cober,
        Dom_Nivel6_Cober
    ]
    
    # Crear un diccionario maestro
    catalogo = {}
    for dominio in dominios:
        for item in dominio:
            if item.description:
                catalogo[item.value] = item.description

    resultados = []

    # 1. Búsqueda por NOMENCLAT exacto
    if NOMENCLAT is not None:
        try:
            codigo = float(NOMENCLAT)
            if codigo in catalogo:
                resultados.append({
                    "NOMENCLAT": codigo,
                    "leyenda": catalogo[codigo]
                })
        except ValueError:
            pass
        return resultados
    
    # 2. Búsqueda por texto (q)
    if q is not None:
        q_lower = q.lower().strip()
        
        # Primero buscar coincidencias parciales directas (substring)
        for cod, desc in catalogo.items():
            if q_lower in desc.lower():
                resultados.append({
                    "NOMENCLAT": cod,
                    "leyenda": desc
                })
        
        # Si no hay coincidencias directas, buscar por similitud usando difflib
        if not resultados:
            descripciones_inv = {desc: cod for cod, desc in catalogo.items()}
            # get_close_matches recibe (word, possibilities, n, cutoff)
            matches = difflib.get_close_matches(q, descripciones_inv.keys(), n=5, cutoff=0.4)
            for match in matches:
                resultados.append({
                    "NOMENCLAT": descripciones_inv[match],
                    "leyenda": match
                })
                
    return resultados

def search_occurrences_gbif(nombre_original: Optional[str] = None) -> Dict[str, Optional[str]]:
    """
    Busca la jerarquía taxonómica completa en GBIF a partir del nombre original.
    
    :param nombre_original: [str] Nombre de la especie a buscar.
    :return: Diccionario con la información taxonómica correspondiente (DIVISION, CLASE, ORDEN, FAMILIA, GENERO, ESPECIE).
    """
    if not isinstance(nombre_original, str) or not nombre_original.strip():
        return {"ESPECIE_GBIF": "NO ENCONTRADO"}
        
    try:
        response = occurrences.search(q=nombre_original, limit=1)

        if response and response.get('results'):
            registro = response['results'][0]
            
            # Extraemos toda la jerarquía usando las llaves del JSON de GBIF
            # GBIF suele usar 'phylum' para lo que referimos como 'DIVISION'
            return {
                "DIVISION_GBIF": registro.get('phylum'), 
                "CLASE_GBIF": registro.get('class'),
                "ORDEN_GBIF": registro.get('order'),
                "FAMILIA_GBIF": registro.get('family'),
                "GENERO_GBIF": registro.get('genus'),
                "ESPECIE_GBIF": registro.get('species', registro.get('scientificName', 'NO ENCONTRADO'))
            }
        else:
            return {"ESPECIE_GBIF": "NO ENCONTRADO"}

    except Exception as e:
        return {"ESPECIE_GBIF": f"Error: {str(e)}"}

def get_uicn_category_description(api_code: str) -> str:
    """Mapea el código corto de la UICN al dominio de amenaza oficial en GeoANLA."""
    for item in Dom_Amenaza:
        if item.description and item.description.endswith(f"({api_code})"):
            return item.description
    return Dom_Amenaza.NO_EVALUADO.description

def search_uicn_api(nombre_cientifico: Optional[str] = None) -> Dict[str, str]:
    """
    Busca la categoría de amenaza de una especie en la API de la UICN de forma segura.
    Retorna la sigla de la API y la descripción oficial mapeada a los dominios del proyecto.
    
    :param nombre_cientifico: [str] Nombre científico de la especie (ej. "Tremarctos ornatus").
    :return: Diccionario con la sigla y su equivalencia en el catálogo.
    """
    if not isinstance(nombre_cientifico, str) or not nombre_cientifico.strip():
        return {"SIGLA_UICN_API": "NE", "CATEG_UICN": Dom_Amenaza.NO_EVALUADO.description}
    
    parts = nombre_cientifico.strip().split()
    if len(parts) < 2:
        return {"SIGLA_UICN_API": "NE", "CATEG_UICN": Dom_Amenaza.NO_EVALUADO.description}
        
    genus = parts[0]
    species = parts[1]
    
    token = os.getenv("UICN_API_TOKEN")
    if not token:
        # En vez de romper ejecución masiva, devolvemos error claro.
        return {"SIGLA_UICN_API": "ERROR_TOKEN", "CATEG_UICN": "Sin Token en .env"}

    headers = {
        "accept": "application/json",
        "Authorization": token
    }
    
    url = "https://api.iucnredlist.org/api/v4/taxa/scientific_name"
    params = {
        "genus_name": genus,
        "species_name": species
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code == 404:
            sigla = "NE"
        elif response.status_code != 200:
            sigla = f"HTTP_{response.status_code}"
        else:
            data = response.json()
            lista_evaluaciones = data.get('assessments', [])
            
            if not lista_evaluaciones:
                sigla = "NE"
            else:
                reporte_actual = next((item for item in lista_evaluaciones if item.get('latest') is True), None)
                if reporte_actual:
                    sigla = reporte_actual.get('red_list_category_code', 'NE')
                else:
                    sigla = "NE"
                    
    except requests.exceptions.RequestException:
        sigla = "ERROR_CONEXION"
    except Exception:
        sigla = "ERROR"

    if sigla in ["NE", "ERROR", "ERROR_CONEXION", "ERROR_TOKEN"] or sigla.startswith("HTTP"):
        desc_oficial = Dom_Amenaza.NO_EVALUADO.description if sigla == "NE" else f"Error: {sigla}"
    else:
        desc_oficial = get_uicn_category_description(sigla)

    return {
        "SIGLA_UICN_API": sigla,
        "CATEG_UICN": desc_oficial
    }
