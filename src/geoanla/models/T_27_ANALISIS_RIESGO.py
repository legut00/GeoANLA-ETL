from typing import Optional
from pydantic import Field, ConfigDict
from geoanla.core.base import BaseEV_Geo

class RiesgoAmbiental_AD(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class RiesgoAmbiental_AI(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class RiesgoIndividual_AD(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class RiesgoIndividual_AI(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class RiesgoSocial_AD(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class RiesgoSocial_AI(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class RiesgoSocioeconomico_AD(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class RiesgoSocioeconomico_AI(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

