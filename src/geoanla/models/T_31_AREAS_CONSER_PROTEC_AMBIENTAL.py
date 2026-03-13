from typing import Optional
from pydantic import Field, ConfigDict
from geoanla.core.base import BaseEV_Geo

class Internacional(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class Local(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class Nacional(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class Regional(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

