from typing import Optional
from pydantic import Field, ConfigDict, model_validator
from geoanla.core.base import BaseEV_Geo
from geoanla.catalog import (
    Dom_Departamento,
    Dom_Municipio,
    Dom_Tenencia
)


class Predios(BaseEV_Geo):
    """
    Feature Class: Predios (Polígono)
    Descripción: Presenta los predios identificados en el área de influencia
        del proyecto y su caracterización.
    """
    model_config = ConfigDict(
        use_enum_values=True,
        validate_assignment=True,
        populate_by_name=True
    )

    # === IDENTIFICACIÓN Y PROPIEDAD ===
    EXPEDIENTE: Optional[str] = Field(None, max_length=20)
    NOM_PREDIO: Optional[str] = Field(None, max_length=100)
    ID_PREDIO: str = Field(..., max_length=30)
    NOM_PROPIE: Optional[str] = Field(None, max_length=100)

    # === LOCALIZACIÓN POLÍTICO-ADMINISTRATIVA ===
    VEREDA: str = Field(..., max_length=100)
    # Los dominios de DANE suelen ser Strings
    MUNICIPIO: Dom_Municipio = Field(...)
    DEPTO: Dom_Departamento = Field(...)

    # === CARACTERIZACIÓN JURÍDICA ===
    TENENCIA: Optional[Dom_Tenencia] = Field(None)
    TENE_COLEC: Optional[str] = Field(None, max_length=150)

    # === INFORMACIÓN GEOMÉTRICA Y NOTAS ===
    OBSERV: Optional[str] = Field(None, max_length=255)
    AREA_ha: float = Field(..., ge=0.0)

    # --- VALIDACIONES LÓGICAS (CONDICIONALES) ---

    @model_validator(mode='after')
    def validate_collective_tenancy(self) -> 'Predios':
        """
        Si la tenencia es 'Propiedad colectiva' (código correspondiente),
        el campo TENE_COLEC es obligatorio.
        """
        # Verifica que el código 2.0 sea el correcto para Propiedad Colectiva
        if self.TENENCIA == 2.0:
            if not self.TENE_COLEC:
                raise ValueError(
                    "Fallo de integridad: Cuando la tenencia es 'Propiedad "
                    "colectiva', debe identificar el tipo en TENE_COLEC."
                )
        return self
class EstructuraPropiedad(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class PoblacionReasentar(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class PoblacionReceptora(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class RutaMovilizacion(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

