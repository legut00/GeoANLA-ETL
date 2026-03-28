import difflib
from typing import Optional, Union, List, Dict
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
