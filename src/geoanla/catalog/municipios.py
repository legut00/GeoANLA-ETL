import pandas as pd
from enum import Enum
import unicodedata
import os

# ---------------------------------------------------------------------------
# DOMINIO MUNICIPIO
# ---------------------------------------------------------------------------

# Los dominios de los municipios son muy largos entonces decidi crear un archivo para cada uno
# 1. Función auxiliar para limpiar nombres (Ej: "Tolú Viejo" -> "TOLU_VIEJO")
def normalizar_nombre(texto):
    # Descompone caracteres unicode (quita tildes)
    nfkd = unicodedata.normalize('NFKD', str(texto))
    texto_sin_tildes = "".join([c for c in nfkd if not unicodedata.combining(c)])
    # Reemplaza espacios y guiones por _ y pasa a mayúsculas
    nombre_limpio = texto_sin_tildes.upper().replace(' ', '_').replace('-', '_').replace('.', '')
    # Filtra solo caracteres alfanuméricos y guiones bajos
    return "".join(c for c in nombre_limpio if c.isalnum() or c == '_')



# 2. Cargar datos del CSV (NUEVA LÓGICA)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Ahora el archivo está en una subcarpeta 'data' dentro de 'catalog'
PATH_MUNICIPIOS = os.path.join(BASE_DIR, "data", "municipios_codigos.csv")

if not os.path.exists(PATH_MUNICIPIOS):
    # Intentar una ruta alternativa por si acaso (para desarrollo local)
    PATH_MUNICIPIOS_ALT = os.path.join(BASE_DIR, "..", "..", "..", "data", "raw", "municipios_codigos.csv")
    if os.path.exists(PATH_MUNICIPIOS_ALT):
        PATH_MUNICIPIOS = PATH_MUNICIPIOS_ALT
    else:
        raise FileNotFoundError(f"No se encontró el archivo en {PATH_MUNICIPIOS}")

df_mun = pd.read_csv(PATH_MUNICIPIOS, dtype={'id': str})

# Rellenamos ceros a la izquierda (ej. 5001 -> 05001)
df_mun['id'] = df_mun['id'].str.zfill(5)

# 3. Preparar Diccionarios para el Enum
# DICCIONARIO_DESCRIPCIONES: Se usará dentro de la @property descripcion
# Usamos freeze=True para que nadie lo pueda modificar después
DICCIONARIO_DESC_MUNICIPIOS = dict(zip(df_mun['id'], df_mun['nombre']))

# MIEMBROS DEL ENUM: {NOMBRE_CLAVE: VALOR}
# OJO: Como hay municipios con el mismo nombre en distintos deptos (ej. Buenavista),
# concatenamos el código al nombre para que la clave sea ÚNICA.
# Ej: BUENAVISTA_63130 = "63130"
miembros_enum = {}
for _, row in df_mun.iterrows():
    nombre_clave = f"{normalizar_nombre(row['nombre'])}_{row['id']}"
    miembros_enum[nombre_clave] = row['id']

# 4. Definir la Clase Base con la propiedad 'descripcion'
# Esto es necesario para que el Enum dinámico herede esta lógica
class MunicipioBase(str, Enum):
    """Clase base para el Enum dinámico de Municipios"""
    @property
    def descripcion(self):
        return DICCIONARIO_DESC_MUNICIPIOS.get(self.value, "Desconocido")

# 5. CREACIÓN MÁGICA DEL ENUM
# Enum(NombreClase, DiccionarioMiembros, TipoBase)
Dom_Municipio = Enum('Dom_Municipio', miembros_enum, type=MunicipioBase)