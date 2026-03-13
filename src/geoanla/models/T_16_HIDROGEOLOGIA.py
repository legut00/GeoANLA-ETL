from typing import Optional
from pydantic import Field, ConfigDict
from geoanla.core.base import BaseEV_Geo

class CaptacionAguaSubter(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class Inyeccion(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class PuntoHidrogeologico(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class PuntoMuestreoAguaSubter(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class SondeoElectricoVertical(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class UnidadHidrogeologica(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class VulneraAcuiferos(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class ZonasRecarga(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

