import difflib
from typing import Optional, Union, List, Dict

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
