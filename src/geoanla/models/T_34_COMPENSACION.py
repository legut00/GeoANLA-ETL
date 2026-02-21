from datetime import date
from typing import Optional, Any
from pydantic import Field, ConfigDict, field_validator, model_validator
from geoanla.core.base import BaseEV_Geo
from geoanla.catalog import (
    Dom_CAR, 
    Dom_Tipo_Actadmin, 
    Dom_SubAct_Comp, 
    Dom_Otras_Comp,
    Dom_EstInver
)

class Compens_OTAutorPG(BaseEV_Geo):
    """
    Capa geográfica para compensación a otras autoridades.
    Geometría esperada: Polígono / MultiPolígono.
    """
    model_config = ConfigDict(
        use_enum_values=True,
        validate_assignment=True,
        populate_by_name=True
    )

    # === INFORMACIÓN ADMINISTRATIVA ===
    EXPEDIENTE: Optional[str] = Field(None, max_length=20, description="Condicional")
    OPERADOR: str = Field(..., max_length=100, description="Obligatorio")
    PROYECTO: str = Field(..., max_length=200, description="Obligatorio")
    EXP_AUT_AB: str = Field(..., max_length=20, description="Obligatorio")
    
    # === DOMINIOS ===
    AUT_AB: Dom_CAR = Field(..., description="Obligatorio")
    T_ACTO_OBL: Dom_Tipo_Actadmin = Field(..., description="Obligatorio")
    
    # === DETALLES TÉCNICOS Y FECHAS ===
    RES_OBL: int = Field(..., description="SmallInteger: Número de resolución")
    FE_OBL: date = Field(..., description="Fecha del acto administrativo")
    
    # === ACTIVIDADES Y COMPENSACIÓN ===
    ACTIVIDAD: Dom_SubAct_Comp = Field(..., description="Obligatorio")
    OTRA_ACT: Optional[str] = Field(None, max_length=255, description="Condicional si ACTIVIDAD es 'Otra'")
    
    AREA_PG_ha: float = Field(..., ge=0.0, description="Área en ha. (Double)")
    FECHA_INI: date = Field(...)
    FECHA_TER: date = Field(...)
    
    OT_COMP_NN: Dom_Otras_Comp = Field(..., description="Obligatorio")
    VAL_E_COM: float = Field(..., ge=0.0, description="Valor en COP (Double)")
    OBSER_COMP: Optional[str] = Field(None, max_length=255, description="Opcional")

    # === GEOMETRÍA ===
    geometry: Any = Field(..., description="Objeto Shapely Polygon/MultiPolygon")

    # ==========================================
    # VALIDACIONES DE NEGOCIO (REGLAS ANLA)
    # ==========================================

    @field_validator('geometry')
    @classmethod
    def validar_geometria(cls, v):
        """Valida que la geometría sea un Polígono o MultiPolígono."""
        tipo = v.geom_type if hasattr(v, 'geom_type') else str(type(v))
        if 'Polygon' not in tipo:
             raise ValueError(f"Geometría inválida. Se espera Polígono, se recibió: {tipo}")
        return v

    @model_validator(mode='after')
    def validar_condicion_otra_actividad(self) -> 'Compens_OTAutorPG':
        """
        Regla de integridad: Si la actividad es 'Otra' (código 1211.0), 
        el campo OTRA_ACT no puede estar vacío.
        """
        # Comparamos con el valor del Enum
        if self.ACTIVIDAD == 1211.0 and not self.OTRA_ACT:
            raise ValueError("Fallo de negocio: El campo 'OTRA_ACT' es obligatorio cuando 'ACTIVIDAD' es 'Otra' (1211.0)")
        return self

    @model_validator(mode='after')
    def validar_fechas_cronologicas(self) -> 'Compens_OTAutorPG':
        """Valida que la fecha de terminación no sea menor a la de inicio."""
        if self.FECHA_INI and self.FECHA_TER:
            if self.FECHA_TER < self.FECHA_INI:
                raise ValueError(f"Fallo cronológico: FECHA_TER ({self.FECHA_TER}) no puede ser anterior a FECHA_INI ({self.FECHA_INI})")
        return self

class OtraCompensacion(BaseEV_Geo):
    """
    Capa geográfica: Otras Compensaciones (OtraCompensacion)
    Geometría esperada: Polígono / MultiPolígono
    """
    model_config = ConfigDict(
        use_enum_values=True,
        validate_assignment=True,
        populate_by_name=True
    )

    # === INFORMACIÓN ADMINISTRATIVA ===
    EXPEDIENTE: Optional[str] = Field(None, max_length=20, description="Condicional")
    OPERADOR: str = Field(..., max_length=100, description="Obligatorio")
    PROYECTO: str = Field(..., max_length=200, description="Obligatorio")
    ID_OT_COMP: str = Field(..., max_length=20, description="Obligatorio")

    # Actos Administrativos (Condicionales)
    NO_ACTOAD: Optional[int] = Field(None, description="SmallInteger")
    FE_ACTOAD: Optional[date] = None
    T_ACTO_OBL: Optional[Dom_Tipo_Actadmin] = None
    RES_OBL: Optional[int] = Field(None, description="SmallInteger")
    FE_OBL: Optional[date] = None

    # === DETALLES DE LA COMPENSACIÓN ===
    AREA_COMP: float = Field(..., ge=0.0, description="Área total a compensar (ha)")
    ACTIVIDAD: Dom_SubAct_Comp = Field(..., description="Obligatorio")
    OTRA_ACT: Optional[str] = Field(None, max_length=255, description="Condicional")
    DESCRIPCIO: str = Field(..., max_length=255, description="Obligatorio")
    
    AREA_PG_ha: float = Field(..., ge=0.0, description="Área del polígono (ha)")
    ESTADO: Dom_EstInver = Field(..., description="Obligatorio")

    # Fechas proyectadas
    FECHA_INI: date = Field(..., description="Obligatorio")
    FECHA_TER: date = Field(..., description="Obligatorio")

    # Origen de la compensación
    OT_COMP_NN: Dom_Otras_Comp = Field(..., description="Obligatorio")
    OT_NN: Optional[str] = Field(None, max_length=150, description="Condicional")

    # === VALORES ECONÓMICOS ===
    PREC_SUELO: float = Field(..., ge=0.0, description="Precio tierra/ha (COP)")
    VAL_E_COM: float = Field(..., ge=0.0, description="Valor estimado total (COP)")
    VALOR_ACT: float = Field(..., ge=0.0, description="Valor destinado a subactividad (COP)")

    # === OBSERVACIONES Y GEOMETRÍA ===
    OBSER_COMP: Optional[str] = Field(None, max_length=255, description="Opcional")
    geometry: Any = Field(..., description="Objeto Shapely Polygon/MultiPolygon")

    # ==========================================
    # VALIDACIONES LÓGICAS Y ESPACIALES
    # ==========================================

    @field_validator('geometry')
    @classmethod
    def validar_geometria(cls, v):
        """Asegura que el Feature Class sea exclusivamente tipo Polígono."""
        tipo = v.geom_type if hasattr(v, 'geom_type') else str(type(v))
        if 'Polygon' not in tipo:
             raise ValueError(f"Geometría inválida. Se espera Polígono, se recibió: {tipo}")
        return v

    @model_validator(mode='after')
    def validar_campos_condicionales_otra(self) -> 'OtraCompensacion':
        """
        Garantiza que si se selecciona 'Otra' en los dominios, 
        el usuario esté obligado a especificar el nombre en el campo de texto.
        """
        # Condición 1: ACTIVIDAD == 1211.0 (Otra)
        if self.ACTIVIDAD == 1211.0 and not self.OTRA_ACT:
            raise ValueError("Regla de Negocio: 'OTRA_ACT' es obligatorio cuando 'ACTIVIDAD' es 'Otra' (1211.0)")

        # Condición 2: OT_COMP_NN == 20115.0 (Otra)
        if self.OT_COMP_NN == 20115.0 and not self.OT_NN:
            raise ValueError("Regla de Negocio: 'OT_NN' es obligatorio cuando 'OT_COMP_NN' es 'Otra' (20115.0)")
        return self

    @model_validator(mode='after')
    def validar_fechas_cronologicas(self) -> 'OtraCompensacion':
        """Asegura que las fechas de ejecución tengan sentido temporal."""
        if self.FECHA_INI and self.FECHA_TER:
            if self.FECHA_TER < self.FECHA_INI:
                raise ValueError(f"Fallo cronológico: FECHA_TER ({self.FECHA_TER}) no puede ser menor a FECHA_INI ({self.FECHA_INI})")
        return self

    @model_validator(mode='after')
    def validar_coherencia_areas(self) -> 'OtraCompensacion':
        """
        Validador avanzado: El área del polígono (AREA_PG_ha) no puede ser lógicamente 
        mayor que el área total a compensar reportada en la obligación (AREA_COMP).
        """
        if self.AREA_PG_ha is not None and self.AREA_COMP is not None:
            if self.AREA_PG_ha > self.AREA_COMP:
                raise ValueError(f"Coherencia espacial: El área del polígono ({self.AREA_PG_ha}) es mayor que el área total a compensar ({self.AREA_COMP})")
        return self
