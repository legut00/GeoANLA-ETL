import polars as pl
import pandas as pd
import geopandas as gpd
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
    int(item.value): item.descripcion
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

    # Subclases sobreescriben con "N_COBERT" o "OBSERV" para activar validación de leyenda.
    # Sin anotación de tipo → Pydantic lo ignora completamente.
    CAMPO_LEYENDA = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    # --- 0. VALIDACIÓN DE LEYENDA vs NOMENCLATURA (OPT-IN) ---
    @model_validator(mode='after')
    def validar_leyenda_nomenclatura(self):
        """
        Valida que la leyenda coincida EXACTAMENTE con la descripción oficial
        del código NOMENCLAT según el catálogo Corine Land Cover.
        Solo se activa si la subclase define CAMPO_LEYENDA.
        """
        campo = self.__class__.CAMPO_LEYENDA
        if campo is None:
            return self

        leyenda = getattr(self, campo, None)
        nomenclat = getattr(self, 'NOMENCLAT', None)

        if leyenda is not None and nomenclat is not None:
            descripcion_oficial = CATALOGO_CLC.get(nomenclat)
            if descripcion_oficial is not None and leyenda != descripcion_oficial:
                raise ValueError(
                    f"La leyenda '{leyenda}' (campo {campo}) no corresponde al código "
                    f"NOMENCLAT {nomenclat}. La descripción oficial es: '{descripcion_oficial}'"
                )
        return self

    # --- 1. MÉTODOS DE INTELIGENCIA DE DOMINIOS ---
    @classmethod
    def registrar_dominio(cls, nombre_campo: str, diccionario: Dict[Any, str]):
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
    def obtener_codigo_enum(cls, valor: Any, referencia: Union[Any, str]) -> Optional[int]:
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

        if isinstance(valor, (int, float)):
            try:
                if int(valor) in [m.value for m in clase_enum]: return int(valor)
            except: pass

        texto = str(valor).strip().lower()
        for m in clase_enum:
            if (hasattr(m, 'descripcion') and str(m.descripcion).lower() == texto) or m.name.lower() == texto:
                return m.value
        return None

    @classmethod
    def domain(cls, nombre_campo: str) -> Dict[Any, str]:
        if nombre_campo in cls._dominios_externos: return cls._dominios_externos[nombre_campo]
        doms = cls.get_domains()
        if nombre_campo in doms and isinstance(doms[nombre_campo], type):
            val = doms[nombre_campo]
            return {m.value: (m.descripcion if hasattr(m, 'descripcion') else m.name) for m in val}
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
                msg = "; ".join([f"[{err['loc'][0]}]: {err['msg']}" for err in e.errors()])
                errores.append({"Fila": index + offset, "ID": identificador, "Errores": msg})

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