# src/geoanla/catalog/__init__.py

# 1. Importamos los dominios manuales (los que están en domains.py)
from .domains import *

# 2. Importamos el dominio dinámico de municipios
from .municipios import Dom_Municipio

# 3. Importamos los niveles de Corine Land Cover
from .corineland import (
    Dom_CateCober,
    Dom_SubcatCober,
    Dom_Clas_Cober,
    Dom_Subclas_Cober,
    Dom_Nivel5_Cober,
    Dom_Nivel6_Cober
)

# Definimos el __all__ para tener un control de qué se exporta 
# al usar "from geoanla.catalog import *"
__all__ = [
    "Dom_Municipio",
    "Dom_CateCober",
    "Dom_SubcatCober",
    "Dom_Clas_Cober",
    "Dom_Subclas_Cober",
    "Dom_Nivel5_Cober",
    "Dom_Nivel6_Cober",
    # Agrega aquí los nombres de las clases de domains.py si quieres ser estricto
]