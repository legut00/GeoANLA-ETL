import pandas as pd
from enum import Enum
import unicodedata
import os

# ---------------------------------------------------------------------------
# DOMINIO MUNICIPIO
# ---------------------------------------------------------------------------

# Los dominios de los municipios son muy largos entonces decidi crear un archivo para cada uno
# 1. Función auxiliar para limpiar nombres (Ej: "Tolú Viejo" -> "TOLU_VIEJO")
def normalize_name(texto):
    """Limpia nombres para ser usados como claves de Enum."""
    # Descompone caracteres unicode (quita tildes)
    nfkd = unicodedata.normalize('NFKD', str(texto))
    texto_sin_tildes = "".join(
        [c for c in nfkd if not unicodedata.combining(c)]
    )
    # Reemplaza espacios y guiones por _ y pasa a mayúsculas
    nombre_limpio = texto_sin_tildes.upper().replace(' ', '_')\
        .replace('-', '_').replace('.', '')
    # Filtra solo caracteres alfanuméricos y guiones bajos
    return "".join(c for c in nombre_limpio if c.isalnum() or c == '_')


# 2. Cargar datos del CSV (NUEVA LÓGICA)
DIR_BASE = os.path.dirname(os.path.abspath(__file__))
# Ahora el archivo está en una subcarpeta 'data' dentro de 'catalog'
RUTA_MUNICIPIOS = os.path.join(DIR_BASE, "data", "municipios_codigos.csv")

if not os.path.exists(RUTA_MUNICIPIOS):
    # Intentar una ruta alternativa por si acaso (para desarrollo local)
    RUTA_MUN_ALT = os.path.join(
        DIR_BASE, "..", "..", "..", "data", "raw", "municipios_codigos.csv"
    )
    if os.path.exists(RUTA_MUN_ALT):
        RUTA_MUNICIPIOS = RUTA_MUN_ALT
    else:
        raise FileNotFoundError(
            f"No se encontró el archivo en {RUTA_MUNICIPIOS}"
        )

df_mun = pd.read_csv(RUTA_MUNICIPIOS, dtype={'id': str})

# Rellenamos ceros a la izquierda (ej. 5001 -> 05001)
df_mun['id'] = df_mun['id'].str.zfill(5)

# 3. Preparar Diccionarios para el Enum
DICCIONARIO_DESC_MUNICIPIOS = dict(zip(df_mun['id'], df_mun['nombre']))

# MIEMBROS DEL ENUM: {NOMBRE_CLAVE: VALOR}
miembros_enum = {}
for _, fila in df_mun.iterrows():
    nombre_clave = f"{normalize_name(fila['nombre'])}_{fila['id']}"
    miembros_enum[nombre_clave] = fila['id']


# 4. Definir la Clase Base con la propiedad 'description'
class MunicipioBase(str, Enum):
    """Clase base para el Enum dinámico de Municipios"""
    @property
    def description(self):
        return DICCIONARIO_DESC_MUNICIPIOS.get(self.value, "Desconocido")


# 5. CREACIÓN MÁGICA DEL ENUM
Dom_Municipio = Enum('Dom_Municipio', miembros_enum, type=MunicipioBase)