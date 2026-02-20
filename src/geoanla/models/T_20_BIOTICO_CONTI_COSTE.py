from datetime import date
from typing import Optional, ClassVar, Set, Any
from pydantic import Field, ConfigDict, field_validator, model_validator
from shapely.geometry import Point
from geoanla.core.base import BaseEV_Geo
from geoanla.catalog import (
    Dom_Municipio, 
    Dom_Departamento, 
    Dom_TipoMuestreoFlo, 
    Dom_Temporada,
    Dom_CateCober,
    Dom_SubcatCober,
    Dom_Clas_Cober,
    Dom_Subclas_Cober,
    Dom_Nivel5_Cober,
    Dom_Nivel6_Cober,
    Dom_TipoMuestreoFau,
    Dom_TipoTransecto
)


class PuntoMuestreoFlora(BaseEV_Geo): # ✅ CORREGIDO: Hereda de BaseEV_Geo

    model_config = ConfigDict(
        use_enum_values=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        populate_by_name=True
    )

    # === INFORMACIÓN ADMINISTRATIVA ===
    EXPEDIENTE: Optional[str] = Field(None, max_length=20)
    OPERADOR: str = Field(..., max_length=100)
    PROYECTO: str = Field(..., max_length=200)
    NUM_ACT_AD: Optional[str] = Field(None, max_length=20)
    FEC_ACT_AD: Optional[date] = None
    ART_ACT_AD: Optional[str] = Field(None, max_length=50)

    # === LOCALIZACIÓN ===
    VEREDA: str = Field(..., max_length=100)

    # ✅ CORREGIDO: Eliminamos min/max length para evitar conflicto de tipos con el Enum
    # La validación de integridad la hace el propio Dom_Municipio
    MUNICIPIO: Dom_Municipio = Field(..., description="Código Divipola (Enum)")
    DEPTO: Dom_Departamento = Field(..., description="Código Depto (Enum)")

    NOMBRE: str = Field(..., max_length=100)

    # === IDENTIFICACIÓN Y COBERTURA ===
    ID_MUEST: str = Field(..., max_length=20)
    N_COBERT: str = Field(..., max_length=100)

    # Validamos Nomenclatura como Entero
    NOMENCLAT: int = Field(...)

    # === TÉCNICA DE MUESTREO ===
    T_MUEST: Dom_TipoMuestreoFlo = Field(...)
    AREA_UM_ha: Optional[float] = None
    LONGI_TR_m: Optional[float] = None
    CUERPO_AGU: Optional[str] = Field(None, max_length=100)
    PROFUND: Optional[float] = None
    DESCRIP: str = Field(..., max_length=255)

    # === TEMPORALIDAD Y ECOLOGÍA ===
    FEC_MUEST: date
    ESTACIONAL: Dom_Temporada = Field(...)
    LOCALIDAD: str = Field(..., max_length=250)

    # === GEOMETRÍA Y COORDENADAS ===
    COTA: float = Field(...)
    COOR_ESTE: float = Field(...)
    COOR_NORTE: float = Field(...)

    # Geometry hereda de BaseEV_Geo, pero reforzamos que sea Point
    geometry: Point = Field(...)

    # --- VALIDACIONES ESPECIALES ---

    _valores_validos: ClassVar[Set[int]] = {
        int(item.value)
        for dom in [
            Dom_CateCober, Dom_SubcatCober, Dom_Clas_Cober,
            Dom_Subclas_Cober, Dom_Nivel5_Cober, Dom_Nivel6_Cober
        ]
        for item in dom
    }

    @field_validator('NOMENCLAT')
    @classmethod
    def validar_nomenclatura_oficial(cls, v):
        if v not in cls._valores_validos:
            raise ValueError(f"El código {v} no es una cobertura válida CLC.")
        return v

    @field_validator('geometry')
    @classmethod
    def validar_geometria_punto(cls, v):
        if not isinstance(v, Point):
            raise ValueError(f"Se requiere un objeto Point, se recibió {type(v)}")
        if v.is_empty:
            raise ValueError("La geometría está vacía.")
        return v


class PuntoMuestreoVeda(BaseEV_Geo): # Hereda de BaseEV_Geo para soporte de geometría
    model_config = ConfigDict(
        use_enum_values=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        populate_by_name=True  # Permite usar el nombre del campo o el alias de la GDB
    )

    # === BLOQUE 1: INFORMACIÓN ADMINISTRATIVA ===
    EXPEDIENTE: Optional[str] = Field(None, max_length=20)
    OPERADOR: str = Field(..., max_length=100)
    PROYECTO: str = Field(..., max_length=200)

    # === BLOQUE 2: LOCALIZACIÓN ===
    VEREDA: str = Field(..., max_length=100)

    # ✅ Eliminados min/max length para que el Enum gestione la validación
    MUNICIPIO: Dom_Municipio = Field(..., description="Código Divipola")
    DEPTO: Dom_Departamento = Field(..., validation_alias="DEPARTAMENTO", description="Código Depto")

    # === BLOQUE 3: IDENTIFICACIÓN VEDA ===
    ID_VEDA: str = Field(..., max_length=20, description="ID Único del individuo en Veda")

    # === BLOQUE 4: COBERTURA ===
    # Mapeos automáticos para cuando el Excel/GDB viene con nombres largos
    N_COBERT: str = Field(..., validation_alias="N_COBERTURA", max_length=100)
    NOMENCLAT: int = Field(..., validation_alias="NOMENCLATURA", description="Código CLC")

    # === BLOQUE 5: DESCRIPCIÓN TÉCNICA ===
    DESCRIP: str = Field(..., validation_alias="DESCRIPCION", max_length=255)
    OBSERV: Optional[str] = Field(None, validation_alias="OBSERVACIONES", max_length=255)

    # === BLOQUE 6: TEMPORALIDAD ===
    FEC_MUEST: date = Field(..., validation_alias="FECHA_MUESTRA")

    # === BLOQUE 7: GEOMETRÍA ===
    COOR_ESTE: float = Field(..., validation_alias="ESTE")
    COOR_NORTE: float = Field(..., validation_alias="NORTE")

    # Heredado de BaseEV_Geo, pero forzamos que sea Point para Veda
    geometry: Point = Field(...)

    # ==========================================================================
    # VALIDACIONES ESPECIALES
    # ==========================================================================

    # 1. Registro de Diccionario Externo para Municipios (God Mode)
    # Se activará automáticamente si registraste el diccionario en la Clase Base

    # 2. Lógica de Nomenclatura (Reutilizada y optimizada)
    _valores_validos: ClassVar[Set[int]] = {
        int(item.value)
        for dom in [
            Dom_CateCober, Dom_SubcatCober, Dom_Clas_Cober,
            Dom_Subclas_Cober, Dom_Nivel5_Cober, Dom_Nivel6_Cober
        ]
        for item in dom
    }

    @field_validator('NOMENCLAT')
    @classmethod
    def validar_nomenclatura_oficial(cls, v):
        if v not in cls._valores_validos:
            raise ValueError(f"El código {v} no es una cobertura CLC válida.")
        return v

    @field_validator('geometry')
    @classmethod
    def validar_geometria(cls, v):
        if not isinstance(v, Point):
            raise ValueError(f"Se requiere Point, se recibió {type(v)}")
        if v.is_empty:
            raise ValueError("La geometría de la veda no puede estar vacía.")
        return v

class CoberturaTierra(BaseEV_Geo):
    model_config = ConfigDict(
        use_enum_values=True,
        validate_assignment=True,
        populate_by_name=True
    )

    # === IDENTIFICACIÓN ===
    EXPEDIENTE: Optional[str] = Field(None, max_length=20, description="Número de expediente ANLA")
    OPERADOR: str = Field(..., max_length=100, description="Empresa solicitante o titular")
    PROYECTO: str = Field(..., max_length=200, description="Nombre del proyecto")
    ID_COBERT: int = Field(..., description="Identificador único del polígono (Integer 4)")

    # === JERARQUÍA CORINE LAND COVER (Double 8 -> Dominios Decimales) ===
    N1_COBERT: Dom_CateCober = Field(..., description="Nivel 1: Categoría principal")
    N2_COBERT: Dom_SubcatCober = Field(..., description="Nivel 2: Subcategoría")
    N3_COBERT: Dom_Clas_Cober = Field(..., description="Nivel 3: Clase")

    # Niveles condicionales (Dependen del detalle de la caracterización)
    N4_COBERT: Optional[Dom_Subclas_Cober] = Field(None, description="Nivel 4: Subclase")
    N5_COBERT: Optional[Dom_Nivel5_Cober] = Field(None, description="Nivel 5: Detalle ecológico")
    N6_COBERT: Optional[Dom_Nivel6_Cober] = Field(None, description="Nivel 6: Detalle fisonómico")

    # === DATOS TÉCNICOS Y GEOMETRÍA ===
    NOMENCLAT: int = Field(..., description="Código Corine Land Cover del nivel más detallado")
    OBSERV: Optional[str] = Field(None, max_length=255)
    AREA_ha: float = Field(..., ge=0.0, description="Área en hectáreas (Double 8)")

    # --- VALIDACIONES LÓGICAS ---

    @model_validator(mode='after')
    def validar_nomenclatura_consistente(self):
        """
        Valida que el campo NOMENCLAT coincida con el nivel más profundo reportado.
        """
        # Lista de niveles de mayor a menor detalle
        niveles = [self.N6_COBERT, self.N5_COBERT, self.N4_COBERT, self.N3_COBERT]

        # El primer valor que no sea None es el nivel máximo de detalle
        nivel_detalle = next((n for n in niveles if n is not None), None)

        if nivel_detalle is not None and int(nivel_detalle) != self.NOMENCLAT:
             raise ValueError(
                f"La NOMENCLAT ({self.NOMENCLAT}) debe coincidir con el nivel más detallado "
                f"reportado ({int(nivel_detalle)})"
            )
        return self

    @model_validator(mode='after')
    def validar_jerarquia_coherente(self):
        """
        Opcional: Valida que el nivel superior sea el prefijo del nivel inferior.
        Ej: Si N3 es 311, N2 debe ser 31 y N1 debe ser 3.
        """
        n1 = str(int(self.N1_COBERT))
        n2 = str(int(self.N2_COBERT))
        n3 = str(int(self.N3_COBERT))

        if not n2.startswith(n1):
            raise ValueError(f"El Nivel 2 ({n2}) no es coherente con el Nivel 1 ({n1})")
        if not n3.startswith(n2):
            raise ValueError(f"El Nivel 3 ({n3}) no es coherente con el Nivel 2 ({n2})")
        return self

# --- CLASE MAESTRA: PuntoMuestreoFauna (CON GEOMETRÍA) ---
class PuntoMuestreoFauna(BaseEV_Geo):
    # 1. CONFIGURACIÓN (Idéntica a Flora)
    model_config = ConfigDict(
        use_enum_values=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        populate_by_name=True
    )

    # === BLOQUE 1: INFORMACIÓN ADMINISTRATIVA ===
    EXPEDIENTE: Optional[str] = Field(None, max_length=20)
    OPERADOR: str = Field(..., max_length=100)
    PROYECTO: str = Field(..., max_length=200)
    NUM_ACT_AD: Optional[str] = Field(None, max_length=20)
    FEC_ACT_AD: Optional[date] = None
    ART_ACT_AD: Optional[str] = Field(None, max_length=50)

    # === BLOQUE 2: LOCALIZACIÓN ===
    VEREDA: str = Field(..., max_length=100)
    MUNICIPIO: Dom_Municipio = Field(..., min_length=5, max_length=5, description="Código Divipola")
    DEPTO: Dom_Departamento = Field(..., min_length=2, max_length=2, description="Código Depto")
    NOMBRE: str = Field(..., max_length=100, description="Nombre del predio o lugar")

    # ¡OJO! Aquí cambia respecto a Flora:
    ID_MUES_PT: str = Field(..., max_length=20, description="ID Único del Punto de Fauna")

    # === BLOQUE 3: COBERTURA Y TÉCNICA ===
    N_COBERT: str = Field(..., max_length=100)
    NOMENCLAT: int = Field(..., description="Código CLC (Máx 4 dígitos)")

    # Dominio específico de fauna
    T_MUEST: Dom_TipoMuestreoFau = Field(..., description="Tipo de captura/observación")

    FEC_MUEST: date
    ESTACIONAL: Dom_Temporada  # Reusamos el dominio de temporada

    # === BLOQUE 4: DESCRIPCIÓN ECOLÓGICA ===
    HABITAT: str = Field(..., max_length=255, description="Descripción del entorno")
    DESCRIP: str = Field(..., max_length=255, description="Descripción del muestreo")
    CUERPO_AGU: Optional[str] = Field(None, max_length=100)

    # === BLOQUE 5: GEOMETRÍA Y COORDENADAS ===
    COTA: float = Field(..., description="msnm")
    COOR_ESTE: float = Field(..., description="Coordenada Este en Sistema Magna Sirgas")
    COOR_NORTE: float = Field(..., description="Coordenada Norte en Sistema Magna Sirgas")

    # Geometría Shapely
    geometry: Point = Field(..., description="Objeto geométrico Shapely (Debe ser un Punto)")

    # === VALIDACIONES PERSONALIZADAS ===

    @field_validator('MUNICIPIO')
    @classmethod
    def validar_municipio_existente(cls, v):
        # Asumiendo que DICCIONARIO_MUNICIPIOS está disponible en el contexto global
        if 'DICCIONARIO_MUNICIPIOS' in globals() and v not in globals()['DICCIONARIO_MUNICIPIOS']:
             raise ValueError(f"El municipio '{v}' no existe en el diccionario maestro.")
        return v

    # --- CORRECCIÓN: LÓGICA DE NOMENCLATURA ENCAPSULADA ---

    # Usamos una "Set Comprehension" (los corchetes {}).
    # Al hacerlo así, la variable 'dom' y 'item' solo existen dentro de los corchetes
    # y no confunden a Pydantic.
    _valores_validos: ClassVar[Set[int]] = {
        int(item.value)
        for dom in [
            Dom_CateCober,
            Dom_SubcatCober,
            Dom_Clas_Cober,
            Dom_Subclas_Cober,
            Dom_Nivel5_Cober,
            Dom_Nivel6_Cober
        ]
        for item in dom
    }

    @field_validator('NOMENCLAT')
    @classmethod
    def validar_nomenclatura_oficial(cls, v):
        if v not in cls._valores_validos:
            raise ValueError(
                f"El código {v} no es válido. No pertenece a ningún dominio de cobertura oficial."
            )
        return v

    @field_validator('geometry')
    @classmethod
    def validar_tipo_geometria(cls, v):
        if not isinstance(v, Point):
            raise ValueError(f"La geometría debe ser un Punto (Point), se recibió: {type(v)}")
        if v.is_empty:
            raise ValueError("La geometría no puede estar vacía.")
        return v

class TransectoMuestreoFauna(BaseEV_Geo):
    model_config = ConfigDict(
        use_enum_values=True,
        validate_assignment=True,
        populate_by_name=True
    )

    # === IDENTIFICACIÓN ===
    EXPEDIENTE: Optional[str] = Field(None, max_length=20)
    OPERADOR: str = Field(..., max_length=100)
    PROYECTO: str = Field(..., max_length=200)

    # Actos Administrativos (Condicionales)
    NUM_ACT_AD: Optional[str] = Field(None, max_length=20)
    FEC_ACT_AD: Optional[date] = None
    ART_ACT_AD: Optional[str] = Field(None, max_length=50)

    # === UBICACIÓN ===
    VEREDA: str = Field(..., max_length=100)
    MUNICIPIO: str = Field(..., max_length=5, description="Código Divipola (Ej: 76001)")
    DEPTO: str = Field(..., max_length=2, description="Código Divipola (Ej: 76)")
    NOMBRE: str = Field(..., max_length=100, description="Nombre del transecto o lugar")

    # ID ÚNICO (Debe coincidir con la tabla de registros de fauna)
    ID_MUES_TR: str = Field(..., max_length=20)

    # === DETALLES TÉCNICOS ===
    # Usamos el dominio creado anteriormente
    T_TRANSEC: Dom_TipoTransecto = Field(..., description="501:Fijo, 502:Variable, 503:Otro")
    OT_TRANSEC: Optional[str] = Field(None, max_length=50)

    # Cobertura y Hábitat
    N_COBERT: str = Field(..., max_length=100, description="Nombre Corine Land Cover")
    NOMENCLAT: int = Field(..., description="Código CLC (Ej: 311)")
    HABITAT: str = Field(..., max_length=250, description="Descripción del entorno")
    DESCRIP: str = Field(..., max_length=255, description="Descripción del muestreo")

    # Temporalidad
    FEC_MUEST: date = Field(...)
    ESTACIONAL: Dom_Temporada = Field(..., description="1:Lluvias, 2:Seca...")

    # === VARIABLES FÍSICAS ===
    CUERPO_AGU: Optional[str] = Field(None, max_length=100)
    COTA_MIN: float = Field(..., ge=0, description="Altura mínima msnm")
    COTA_MAX: float = Field(..., ge=0, description="Altura máxima msnm")

    # Geometría
    LONGITUD_m: float = Field(..., ge=0)
    geometry: Any = Field(exclude=True, description="Objeto LineString")

    # === VALIDACIONES ===

    @field_validator('geometry')
    @classmethod
    def validar_geometria(cls, v):
        tipo = v.geom_type if hasattr(v, 'geom_type') else str(type(v))
        if 'LineString' not in tipo:
             raise ValueError(f"Geometría inválida. Se espera Línea, se recibió: {tipo}")
        return v

    @model_validator(mode='after')
    def validar_consistencia_cotas(self):
        # Validar que la cota máxima no sea menor que la mínima
        if self.COTA_MAX < self.COTA_MIN:
            raise ValueError(f"Error lógico: COTA_MAX ({self.COTA_MAX}) es menor que COTA_MIN ({self.COTA_MIN})")
        return self