import polars as pl
import pandas as pd
import geopandas as gpd
import numpy as np
from pydantic import BaseModel, ValidationError, ConfigDict, Field, model_validator
from typing import Optional, List, Dict, Any, Union, ClassVar, get_type_hints, get_origin, get_args, Annotated
from enum import Enum
import types
from geoanla.catalog import (
    Dom_CateCober, Dom_SubcatCober, Dom_Clas_Cober,
    Dom_Subclas_Cober, Dom_Nivel5_Cober, Dom_Nivel6_Cober
)

# === CATÁLOGO OFICIAL CLC (Nivel de módulo, fuera de Pydantic) ===
CATALOGO_CLC = {
    int(item.value): item.description
    for dom in [
        Dom_CateCober, Dom_SubcatCober, Dom_Clas_Cober,
        Dom_Subclas_Cober, Dom_Nivel5_Cober, Dom_Nivel6_Cober
    ]
    for item in dom
}

class BaseEV(BaseModel):
    # Aceptamos explícitamente Polars, Pandas o GeoPandas
    _data: Optional[Union[pl.DataFrame, pd.DataFrame, gpd.GeoDataFrame]] = None
    _dominios_externos: ClassVar[Dict[str, Dict[str, str]]] = {}

    model_config = ConfigDict(arbitrary_types_allowed=True)

    # --- 0. VALIDACIÓN DE LEYENDA vs NOMENCLATURA (UNIVERSAL) ---

    @model_validator(mode='after')
    def validate_legend_nomenclature(self):
        """
        Validador Universal: Compara código NOMENCLAT vs texto descriptivo 
        dinámicamente dependiendo de lo que declare CAMPO_LEYENDA en la subclase.
        """
        # 1. Obtenemos el nombre de la columna que tiene el texto
        campo_texto = getattr(self.__class__, 'CAMPO_LEYENDA', None)
        
        # Si la clase no definió CAMPO_LEYENDA o no tiene NOMENCLAT, no hacemos nada
        if not campo_texto or not hasattr(self, 'NOMENCLAT'):
            return self

        # 2. Extraemos los valores de la fila actual
        texto_ingresado = getattr(self, campo_texto, None)
        codigo_nomenclat = self.NOMENCLAT

        # 3. Validamos contra el catálogo maestro
        if texto_ingresado is not None and codigo_nomenclat is not None:
            descripcion_oficial = CATALOGO_CLC.get(codigo_nomenclat)
            
            # Limpiamos strings (minúsculas, sin espacios extra) para hacer una comparación fuerte
            if descripcion_oficial and texto_ingresado.strip().lower() != descripcion_oficial.lower():
                raise ValueError(
                    f"Inconsistencia CLC: El código NOMENCLAT '{codigo_nomenclat}' "
                    f"exige el texto exacto '{descripcion_oficial}', "
                    f"pero en la columna '{campo_texto}' se reportó '{texto_ingresado}'."
                )
        return self

    # --- 1. MÉTODOS DE INTELIGENCIA DE DOMINIOS ---
    @classmethod
    def register_domain(cls, nombre_campo: str, diccionario: Dict[Any, str]):
        cls._dominios_externos[nombre_campo] = diccionario

    @classmethod
    def get_domains(cls) -> Dict[str, Any]:
        dominios = {}
        try: type_hints = get_type_hints(cls, globalns=globals())
        except: type_hints = {k: f.annotation for k, f in cls.model_fields.items()}

        def buscar_enum(t):
            if isinstance(t, type) and issubclass(t, Enum): return t
            origin = get_origin(t)
            args = get_args(t)
            if origin in (Union, Annotated, list, types.UnionType):
                for arg in args:
                    res = buscar_enum(arg)
                    if res: return res
            return None

        for nombre, tipo in type_hints.items():
            if nombre.startswith('_'): continue
            res = buscar_enum(tipo)
            if res: dominios[nombre] = res

        for campo in cls._dominios_externos:
            dominios[campo] = "Diccionario Externo"
        return dominios

    @classmethod
    def get_enum_code(cls, valor: Any, referencia: Union[Any, str]) -> Optional[int]:
        clase_enum = None
        if isinstance(referencia, type) and issubclass(referencia, Enum):
            clase_enum = referencia
        elif isinstance(referencia, str):
            dominios = cls.get_domains()
            if referencia in dominios: clase_enum = dominios[referencia]
            else:
                for d in dominios.values():
                    if isinstance(d, type) and d.__name__ == referencia:
                        clase_enum = d; break

        if clase_enum is None: return None
        if valor is None or str(valor).strip().lower() in ['', 'nan', 'none', '0', '0.0']: return None

        # 1. Verificar si el valor ya es el código final del Enum
        # Intentamos casteo flotante primero por si viene de Pandas como 1.0 en vez de 1
        try:
            val_num = float(valor)
            if val_num.is_integer():
                val_int = int(val_num)
                if val_int in [m.value for m in clase_enum]:
                    return val_int
        except (ValueError, TypeError):
            pass

        # Si el Enum usa valores string también validamos
        if valor in [m.value for m in clase_enum]:
            return valor

        # 2. Si no es el código directo, buscamos por la descripción o el nombre del Enum
        texto = str(valor).strip().lower()
        for m in clase_enum:
            if (hasattr(m, 'description') and str(m.description).lower() == texto) or m.name.lower() == texto:
                return m.value
                
        return None

    @classmethod
    def translate_data(cls, df: Union[pl.DataFrame, pd.DataFrame, gpd.GeoDataFrame]) -> Any:
        """
        Traducción vectorizada de alta velocidad. Mapea valores de texto 
        o nombres de Enum a sus códigos numéricos respectivos.
        """
        dominios = cls.get_domains()
        columnas_disponibles = set(df.columns)
        
        # --- CASO A: POLARS (MÁXIMA VELOCIDAD EN RUST) ---
        if isinstance(df, pl.DataFrame):
            expresiones = []
            for campo, clase_enum in dominios.items():
                if campo not in columnas_disponibles or not isinstance(clase_enum, type):
                    continue
                
                # 1. Detectar tipo nativo del Enum para el casting final
                ejemplo = next(iter(clase_enum)).value
                dtype = pl.Int64 if isinstance(ejemplo, int) else pl.Float64
                
                # 2. Pre-calcular mapeo solo para valores únicos presentes
                unique_vals = df.get_column(campo).drop_nulls().unique().to_list()
                mapping = {v: cls.get_enum_code(v, campo) for v in unique_vals}
                
                # 3. Construir expresión vectorizada
                expr = (
                    pl.col(campo)
                    .replace_strict(mapping, default=pl.col(campo))
                    .cast(dtype)
                    .alias(campo)
                )
                expresiones.append(expr)
            
            return df.with_columns(expresiones) if expresiones else df

        # --- CASO B: PANDAS / GEOPANDAS ---
        else:
            df_out = df.copy()
            
            # Limpieza universal preventiva: Convertir NaN a None clásico de Python.
            # Esto evita que Pandas convierta columnas enteramente a float64.
            df_out = df_out.replace({np.nan: None})
            
            for campo, clase_enum in dominios.items():
                if campo not in columnas_disponibles or not isinstance(clase_enum, type):
                    continue
                
                unique_vals = df_out[campo].dropna().unique()
                mapping = {v: cls.get_enum_code(v, campo) for v in unique_vals}
                
                # Reemplazo vectorizado en Pandas
                df_out[campo] = df_out[campo].replace(mapping)
                
                # Intento de casteo a numérico si el Enum es numérico
                ejemplo = next(iter(clase_enum)).value
                if isinstance(ejemplo, int):
                    # Forzamos tipo entero que soporta Nulls en Pandas
                    df_out[campo] = pd.to_numeric(df_out[campo], errors='coerce').astype('Int64')
                elif isinstance(ejemplo, float):
                    df_out[campo] = pd.to_numeric(df_out[campo], errors='coerce')
                    
            return df_out

    @classmethod
    def translate_code_to_text(cls, df: Union[pl.DataFrame, pd.DataFrame, gpd.GeoDataFrame]) -> Any:
        """
        Traducción inversa vectorizada. Mapea códigos numéricos a sus 
        textos descriptivos oficiales (o nombres de Enum) para facilitar el análisis humano.
        """
        dominios = cls.get_domains()
        columnas_disponibles = set(df.columns)
        
        # --- CASO A: POLARS ---
        if isinstance(df, pl.DataFrame):
            expresiones = []
            for campo, clase_enum in dominios.items():
                if campo not in columnas_disponibles or not isinstance(clase_enum, type):
                    continue
                
                # Obtenemos el diccionario {código: texto}
                mapping = cls.domain(campo)
                if not mapping:
                    continue
                    
                # Convertimos las llaves a string para evitar conflictos de tipado estricto en Polars 
                # (una columna no puede tener ints y strings al mismo tiempo durante el replace)
                mapping_str = {str(k): str(v) for k, v in mapping.items() if pd.notnull(k)}
                
                expr = (
                    pl.col(campo).cast(pl.Utf8)  # Castear la columna original a texto
                    .replace(mapping_str, default=pl.col(campo).cast(pl.Utf8))
                    .alias(campo)
                )
                expresiones.append(expr)
            
            return df.with_columns(expresiones) if expresiones else df

        # --- CASO B: PANDAS / GEOPANDAS ---
        else:
            df_out = df.copy()
            
            for campo, clase_enum in dominios.items():
                if campo not in columnas_disponibles or not isinstance(clase_enum, type):
                    continue
                
                mapping = cls.domain(campo)
                if not mapping:
                    continue
                
                # 'map' traduce usando el diccionario. Deja 'NaN' en los valores que no encuentre.
                serie_mapeada = df_out[campo].map(mapping)
                # 'fillna' permite conservar el valor numérico original en caso de que un valor no existiese en el Enum
                df_out[campo] = serie_mapeada.fillna(df_out[campo])
                    
            return df_out

    @classmethod
    def domain(cls, nombre_campo: str) -> Dict[Any, str]:
        if nombre_campo in cls._dominios_externos: return cls._dominios_externos[nombre_campo]
        doms = cls.get_domains()
        if nombre_campo in doms and isinstance(doms[nombre_campo], type):
            val = doms[nombre_campo]
            return {m.value: (m.description if hasattr(m, 'description') else m.name) for m in val}
        return {}

    # --- 2. EXTRACCIÓN SIMPLE ---
    @classmethod
    def extract(cls, df: Union[pl.DataFrame, pd.DataFrame, gpd.GeoDataFrame]):
        cls._data = df
        columnas_df = set(df.columns)
        campos_modelo = set(cls.model_fields.keys())
        print(f"\n--- 🛠️ Fase de Extracción: {cls.__name__} ---")
        print(f"📥 Tipo de datos detectado: {type(df).__name__}")
        faltantes = list(campos_modelo - columnas_df)
        if faltantes:
          print(f"⚠️ Columnas faltantes: {faltantes}")
        else:
          print(f"✅ Estructura íntegra. {len(campos_modelo)} columnas listas.")
          print(f"📋 Campos del modelo: {cls.model_fields.keys()}")
        return {"faltantes": faltantes}

    # --- 3. VALIDACIÓN HÍBRIDA (CORREGIDA) ---
    @classmethod
    def validate_data(cls, offset: int = 0):
        if cls._data is None:
            raise ValueError(f"❌ No hay datos en {cls.__name__}.")

        validos, errores = [], []
        print(f"🚀 Validando {len(cls._data)} registros...")

        # Iterador Adaptativo
        iterator = []
        if isinstance(cls._data, pl.DataFrame):
            iterator = enumerate(cls._data.iter_rows(named=True))
        elif isinstance(cls._data, (pd.DataFrame, gpd.GeoDataFrame)):
            df_temp = cls._data.where(pd.notnull(cls._data), None)
            iterator = enumerate(df_temp.to_dict('records'))
        else:
            raise TypeError(f"Tipo de datos {type(cls._data)} no soportado.")

        for index, datos_fila in iterator:
            datos_fila = {k: v for k, v in datos_fila.items() if v is not None}
            id_piezas = [str(datos_fila.get(c)) for c in ['ID_MUEST', 'ID_MUES_PT', 'EXPEDIENTE'] if datos_fila.get(c)]
            identificador = " ".join(id_piezas) if id_piezas else f"Registro {index}"

            try:
                objeto = cls(**datos_fila)
                validos.append(objeto.model_dump())
            except ValidationError as e:
                # Extraemos el mensaje de forma segura. Los errores de @model_validator no tienen 'loc'
                error_info = {"Fila": index + offset, "ID": identificador}
                for err in e.errors():
                    campo = err['loc'][0] if 'loc' in err and len(err['loc']) > 0 else 'Registro/Modelo'
                    error_info[campo] = err['msg']
                
                errores.append(error_info)

        print("\n" + "="*50 + f"\n📊 RESULTADO FINAL - {cls.__name__}\n" + "="*50)
        print(f"✅ Aprobados: {len(validos)}\n❌ Rechazados: {len(errores)}")

        if errores:
            try: from IPython.display import display; display(pd.DataFrame(errores))
            except: print(errores)
        else: print("\n🎉 ¡Todo perfecto!")


        return validos, errores


# ==========================================
# CLASE BASE 2: Componente Geográfico (Simplificada)
# ==========================================
class BaseEV_Geo(BaseEV):
    model_config = ConfigDict(arbitrary_types_allowed=True, use_enum_values=True, populate_by_name=True)
    geometry: Any = Field(..., description="Atributo geométrico oficial")

    # Ya no necesitas extract_gdf obligatoriamente, pero lo dejamos por compatibilidad
    @classmethod
    def extract_gdf(cls, gdf: gpd.GeoDataFrame):
        return cls.extract(gdf)