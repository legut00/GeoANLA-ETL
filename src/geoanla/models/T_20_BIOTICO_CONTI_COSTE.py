from datetime import date
from typing import Optional, ClassVar, Set, Any
from pydantic import Field, ConfigDict, field_validator, model_validator
from shapely.geometry import Point
from geoanla.core.base import BaseEV_Geo
from geoanla.catalog import (
    Dom_Amenaza,
    Dom_Apendice,
    Dom_Boolean,
    Dom_CateCober,
    Dom_Clas_Cober,
    Dom_Departamento,
    Dom_Dieta,
    Dom_EntidadVeda,
    Dom_Municipio,
    Dom_Nivel5_Cober,
    Dom_Nivel6_Cober,
    Dom_SubcatCober,
    Dom_Subclas_Cober,
    Dom_Temporada,
    Dom_Tipo_Distribu,
    Dom_Tipo_Migra,
    Dom_TipoMuestreoFlo,
    Dom_TipoMuestreoFau,
    Dom_TipoTransecto,
    Dom_Uso_Fauna,
    Dom_Veda,
    Dom_Vigencia
)


class PuntoMuestreoFlora(BaseEV_Geo):
    """
    Feature Class: PuntoMuestreoFlora (Punto)
    """
    model_config = ConfigDict(
        use_enum_values=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        populate_by_name=True
    )

    CAMPO_LEYENDA: ClassVar[str] = "N_COBERT"

    # === INFORMACIÓN ADMINISTRATIVA ===
    EXPEDIENTE: Optional[str] = Field(None, max_length=20)
    OPERADOR: str = Field(..., max_length=100)
    PROYECTO: str = Field(..., max_length=200)
    NUM_ACT_AD: Optional[str] = Field(None, max_length=20)
    FEC_ACT_AD: Optional[date] = None
    ART_ACT_AD: Optional[str] = Field(None, max_length=50)

    # === LOCALIZACIÓN ===
    VEREDA: str = Field(..., max_length=100)
    MUNICIPIO: Dom_Municipio = Field(..., description="Código Divipola (Enum)")
    DEPTO: Dom_Departamento = Field(..., description="Código Depto (Enum)")

    NOMBRE: str = Field(..., max_length=100)

    # === IDENTIFICACIÓN Y COBERTURA ===
    ID_MUEST: str = Field(..., max_length=20)
    N_COBERT: str = Field(..., max_length=100)
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
    def validate_official_nomenclature(cls, v):
        """Valida que la nomenclatura pertenezca a un dominio CLC."""
        if v not in cls._valores_validos:
            raise ValueError(f"El código {v} no es una cobertura válida CLC.")
        return v

    @field_validator('geometry')
    @classmethod
    def validate_point_geometry(cls, v):
        """Valida que la geometría sea un punto no vacío."""
        if not isinstance(v, Point):
            raise ValueError(f"Se requiere objeto Point, se recibió {type(v)}")
        if v.is_empty:
            raise ValueError("La geometría está vacía.")
        return v


class PuntoMuestreoVeda(BaseEV_Geo):
    """
    Feature Class: PuntoMuestreoVeda (Punto)
    """
    model_config = ConfigDict(
        use_enum_values=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        populate_by_name=True
    )

    CAMPO_LEYENDA: ClassVar[str] = "N_COBERT"

    # === BLOQUE 1: INFORMACIÓN ADMINISTRATIVA ===
    EXPEDIENTE: Optional[str] = Field(None, max_length=20)
    OPERADOR: str = Field(..., max_length=100)
    PROYECTO: str = Field(..., max_length=200)

    # === BLOQUE 2: LOCALIZACIÓN ===
    VEREDA: str = Field(..., max_length=100)
    MUNICIPIO: Dom_Municipio = Field(..., description="Código Divipola")
    DEPTO: Dom_Departamento = Field(
        ..., validation_alias="DEPARTAMENTO", description="Código Depto"
    )

    # === BLOQUE 3: IDENTIFICACIÓN VEDA ===
    ID_VEDA: str = Field(..., max_length=20)

    # === BLOQUE 4: COBERTURA ===
    N_COBERT: str = Field(..., validation_alias="N_COBERTURA", max_length=100)
    NOMENCLAT: int = Field(..., validation_alias="NOMENCLATURA")

    # === BLOQUE 5: DESCRIPCIÓN TÉCNICA ===
    DESCRIP: str = Field(..., validation_alias="DESCRIPCION", max_length=255)
    OBSERV: Optional[str] = Field(
        None, validation_alias="OBSERVACIONES", max_length=255
    )

    # === BLOQUE 6: TEMPORALIDAD ===
    FEC_MUEST: date = Field(..., validation_alias="FECHA_MUESTRA")

    # === BLOQUE 7: GEOMETRÍA ===
    COOR_ESTE: float = Field(..., validation_alias="ESTE")
    COOR_NORTE: float = Field(..., validation_alias="NORTE")
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
    def validate_official_nomenclature(cls, v):
        """Valida que la nomenclatura sea oficial CLC."""
        if v not in cls._valores_validos:
            raise ValueError(f"El código {v} no es una cobertura CLC válida.")
        return v

    @field_validator('geometry')
    @classmethod
    def validate_geometry(cls, v):
        """Valida la geometría del punto de veda."""
        if not isinstance(v, Point):
            raise ValueError(f"Se requiere Point, se recibió {type(v)}")
        if v.is_empty:
            raise ValueError("La geometría de la veda no puede estar vacía.")
        return v


class CoberturaTierra(BaseEV_Geo):
    """
    Feature Class: CoberturaTierra (Polígono)
    """
    model_config = ConfigDict(
        use_enum_values=True,
        validate_assignment=True,
        populate_by_name=True
    )

    CAMPO_LEYENDA: ClassVar[str] = "OBSERV"

    # === IDENTIFICACIÓN ===
    EXPEDIENTE: Optional[str] = Field(None, max_length=20)
    OPERADOR: str = Field(..., max_length=100)
    PROYECTO: str = Field(..., max_length=200)
    ID_COBERT: int = Field(..., description="ID único polígono")

    # === JERARQUÍA CORINE LAND COVER ===
    N1_COBERT: Dom_CateCober = Field(..., description="Nivel 1")
    N2_COBERT: Dom_SubcatCober = Field(..., description="Nivel 2")
    N3_COBERT: Dom_Clas_Cober = Field(..., description="Nivel 3")

    N4_COBERT: Optional[Dom_Subclas_Cober] = Field(None, description="Nivel 4")
    N5_COBERT: Optional[Dom_Nivel5_Cober] = Field(None, description="Nivel 5")
    N6_COBERT: Optional[Dom_Nivel6_Cober] = Field(None, description="Nivel 6")

    # === DATOS TÉCNICOS Y GEOMETRÍA ===
    NOMENCLAT: int = Field(..., description="Código CLC detallado")
    OBSERV: Optional[str] = Field(None, max_length=255)
    AREA_ha: float = Field(..., ge=0.0)

    # --- SANITIZACIÓN DE DATOS ---

    @field_validator('N4_COBERT', 'N5_COBERT', 'N6_COBERT', mode='before')
    @classmethod
    def sanitize_zero_level(cls, v):
        """Convierte 0.0 a None para niveles opcionales."""
        if v is not None and float(v) == 0.0:
            return None
        return v

    # --- VALIDACIONES LÓGICAS ---

    @model_validator(mode='after')
    def validate_consistent_nomenclature(self):
        """Valida consistencia entre NOMENCLAT y niveles detallados."""
        niveles = [
            self.N6_COBERT, self.N5_COBERT, self.N4_COBERT, self.N3_COBERT
        ]
        nivel_detalle = next((n for n in niveles if n is not None), None)

        if nivel_detalle is not None and int(nivel_detalle) != self.NOMENCLAT:
            raise ValueError(
                f"La NOMENCLAT ({self.NOMENCLAT}) debe coincidir con el "
                f"nivel reportado ({int(nivel_detalle)})"
            )
        return self

    @model_validator(mode='after')
    def validate_coherent_hierarchy(self):
        """Valida que la jerarquía CLC sea coherente."""
        n1 = str(int(self.N1_COBERT))
        n2 = str(int(self.N2_COBERT))
        n3 = str(int(self.N3_COBERT))

        if not n2.startswith(n1):
            raise ValueError(f"Nivel 2 ({n2}) incoherente con Nivel 1 ({n1})")
        if not n3.startswith(n2):
            raise ValueError(f"Nivel 3 ({n3}) incoherente con Nivel 2 ({n2})")

        if self.N4_COBERT is not None:
            n4 = str(int(self.N4_COBERT))
            if not n4.startswith(n3):
                raise ValueError(f"Nivel 4 ({n4}) incoherente")

            if self.N5_COBERT is not None:
                n5 = str(int(self.N5_COBERT))
                if not n5.startswith(n4):
                    raise ValueError(f"Nivel 5 ({n5}) incoherente")

                if self.N6_COBERT is not None:
                    n6 = str(int(self.N6_COBERT))
                    if not n6.startswith(n5):
                        raise ValueError(f"Nivel 6 ({n6}) incoherente")

        return self


class PuntoMuestreoFauna(BaseEV_Geo):
    """
    Feature Class: PuntoMuestreoFauna (Punto)
    """
    model_config = ConfigDict(
        use_enum_values=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        populate_by_name=True
    )

    CAMPO_LEYENDA: ClassVar[str] = "N_COBERT"

    # === BLOQUE 1: INFORMACIÓN ADMINISTRATIVA ===
    EXPEDIENTE: Optional[str] = Field(None, max_length=20)
    OPERADOR: str = Field(..., max_length=100)
    PROYECTO: str = Field(..., max_length=200)
    NUM_ACT_AD: Optional[str] = Field(None, max_length=20)
    FEC_ACT_AD: Optional[date] = None
    ART_ACT_AD: Optional[str] = Field(None, max_length=50)

    # === BLOQUE 2: LOCALIZACIÓN ===
    VEREDA: str = Field(..., max_length=100)
    MUNICIPIO: Dom_Municipio = Field(..., description="Código Divipola")
    DEPTO: Dom_Departamento = Field(..., description="Código Depto")
    NOMBRE: str = Field(..., max_length=100)

    ID_MUES_PT: str = Field(..., max_length=20)

    # === BLOQUE 3: COBERTURA Y TÉCNICA ===
    N_COBERT: str = Field(..., max_length=100)
    NOMENCLAT: int = Field(...)

    T_MUEST: Dom_TipoMuestreoFau = Field(...)

    FEC_MUEST: date
    ESTACIONAL: Dom_Temporada

    # === BLOQUE 4: DESCRIPCIÓN ECOLÓGICA ===
    HABITAT: str = Field(..., max_length=255)
    DESCRIP: str = Field(..., max_length=255)
    CUERPO_AGU: Optional[str] = Field(None, max_length=100)

    # === BLOQUE 5: GEOMETRÍA Y COORDENADAS ===
    COTA: float = Field(...)
    COOR_ESTE: float = Field(...)
    COOR_NORTE: float = Field(...)
    geometry: Point = Field(...)


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
    def validate_official_nomenclature(cls, v):
        """Valida nomenclatura CLC."""
        if v not in cls._valores_validos:
            raise ValueError(f"El código {v} no es válido.")
        return v

    @field_validator('geometry')
    @classmethod
    def validate_geometry_type(cls, v):
        """Valida que sea objeto Point."""
        if not isinstance(v, Point):
            raise ValueError(f"Debe ser Punto (Point), se recibió: {type(v)}")
        if v.is_empty:
            raise ValueError("La geometría no puede estar vacía.")
        return v


class TransectoMuestreoFauna(BaseEV_Geo):
    """
    Feature Class: TransectoMuestreoFauna (Línea)
    """
    model_config = ConfigDict(
        use_enum_values=True,
        validate_assignment=True,
        populate_by_name=True
    )

    CAMPO_LEYENDA: ClassVar[str] = "N_COBERT"

    # === IDENTIFICACIÓN ===
    EXPEDIENTE: Optional[str] = Field(None, max_length=20)
    OPERADOR: str = Field(..., max_length=100)
    PROYECTO: str = Field(..., max_length=200)

    NUM_ACT_AD: Optional[str] = Field(None, max_length=20)
    FEC_ACT_AD: Optional[date] = None
    ART_ACT_AD: Optional[str] = Field(None, max_length=50)

    # === UBICACIÓN ===
    VEREDA: str = Field(..., max_length=100)
    MUNICIPIO: str = Field(..., max_length=5)
    DEPTO: str = Field(..., max_length=2)
    NOMBRE: str = Field(..., max_length=100)

    ID_MUES_TR: str = Field(..., max_length=20)

    # === DETALLES TÉCNICOS ===
    T_TRANSEC: Dom_TipoTransecto = Field(...)
    OT_TRANSEC: Optional[str] = Field(None, max_length=50)

    N_COBERT: str = Field(..., max_length=100)
    NOMENCLAT: int = Field(...)
    HABITAT: str = Field(..., max_length=250)
    DESCRIP: str = Field(..., max_length=255)

    FEC_MUEST: date = Field(...)
    ESTACIONAL: Dom_Temporada = Field(...)

    # === VARIABLES FÍSICAS ===
    CUERPO_AGU: Optional[str] = Field(None, max_length=100)
    COTA_MIN: float = Field(..., ge=0)
    COTA_MAX: float = Field(..., ge=0)

    # Geometría
    LONGITUD_m: float = Field(..., ge=0)
    geometry: Any = Field(exclude=True)

    # === VALIDACIONES ===

    @field_validator('geometry')
    @classmethod
    def validate_geometry(cls, v):
        """Valida que la geometría sea LineString."""
        tipo = v.geom_type if hasattr(v, 'geom_type') else str(type(v))
        if 'LineString' not in tipo:
             raise ValueError(f"Geometría inválida se recibió: {tipo}")
        return v

    @model_validator(mode='after')
    def validate_elevation_consistency(self):
        """Valida que la cota máxima sea mayor o igual a la mínima."""
        if self.COTA_MAX < self.COTA_MIN:
            raise ValueError(
                f"La cota máxima ({self.COTA_MAX}) es menor que la "
                f"mínima ({self.COTA_MIN})"
            )
        return self