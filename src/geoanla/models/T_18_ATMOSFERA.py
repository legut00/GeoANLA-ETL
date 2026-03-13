from typing import Optional
from pydantic import Field, ConfigDict
from geoanla.core.base import BaseEV_Geo

class CalidadAire(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class FuenteDispersaEmisionPG(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class FuenteDispersaEmisionPT(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class FuenteDispersaOlores(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class FuenteEmisionRuido(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class FuenteFijaEmision(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class FuenteFijaOlores(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class FuenteLinealEmision(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class IsofonaRAmbDiurnoFestivo(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class IsofonaRAmbDiurnoHabil(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class IsofonaRAmbNocturnoFestivo(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class IsofonaRAmbNocturnoHabil(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class IsolineaSobrepresion(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class IsolineaVibraciones(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class MonitoreoRuidoAmbiental(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class MonitoreoVibraciones(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

