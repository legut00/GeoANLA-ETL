from datetime import date
from typing import Optional, Union


from pydantic import ConfigDict, Field, field_validator
from shapely.geometry import LineString, MultiLineString, Polygon, MultiPolygon


from geoanla.catalog import Dom_Sector
from geoanla.core.base import BaseEV_Geo

class Abscisas(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class AlternaProyectoLN(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class AlternaProyectoPG(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class AreaInfluencia(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class AreaProyecto(BaseEV_Geo):
    """
    Feature Class: AreaProyecto (Polígono)
    Área del proyecto objeto de solicitud de licencia.
    Ej.: Campo, Bloque, Área de Interés, Estación o Refinería, Puerto, Aeropuerto, etc.
    """
    model_config = ConfigDict(
        use_enum_values=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        populate_by_name=True
    )

    # === INFORMACIÓN ADMINISTRATIVA ===
    EXPEDIENTE: Optional[str] = Field(None, max_length=20, description="Número de expediente asignado por la ANLA")
    NUM_ACT_AD: Optional[str] = Field(None, max_length=20, description="Número de la resolución o acto administrativo")
    FEC_ACT_AD: Optional[date] = Field(None, description="Fecha de la resolución o acto administrativo")
    ART_ACT_AD: Optional[str] = Field(None, max_length=50, description="Artículo, parágrafo y/o numeral de la resolución")
    
    # === DATOS DEL PROYECTO ===
    SECTOR: Dom_Sector = Field(..., description="Identifica el sector al que corresponde el proyecto (Enum)")
    OPERADOR: str = Field(..., max_length=100, description="Empresa solicitante o titular de la licencia")
    PROYECTO: str = Field(..., max_length=200, description="Nombre del proyecto objeto de licenciamiento o licenciado")
    CONTRATO: Optional[str] = Field(None, max_length=100, description="Contrato o título asociado al proyecto (ANH, ANM, UPME, ANI, etc.)")
    
    # === CARACTERÍSTICAS TÉCNICAS ===
    DESCRIP: str = Field(..., max_length=255, description="Descripción breve de las características generales o relevantes del proyecto")
    NOMENCLAT: str = Field(..., max_length=20, description="Nomenclatura para el área del proyecto")
    OBSERV: Optional[str] = Field(None, max_length=255, description="Observaciones pertinentes para el elemento")
    AREA_ha: float = Field(..., description="Área en hectáreas (ha) de cada uno de los polígonos")

    # === GEOMETRÍA ===
    geometry: Union[Polygon, MultiPolygon] = Field(...)

    # --- VALIDACIONES ---

    @field_validator('AREA_ha')
    @classmethod
    def validate_positive_area(cls, v):
        """Valida que el área del polígono sea un número estrictamente positivo."""
        if v <= 0:
            raise ValueError(f"El área (AREA_ha) debe ser mayor a 0, se recibió {v}")
        return v

    @field_validator('geometry')
    @classmethod
    def validate_polygon_geometry(cls, v):
        """Valida que la geometría sea un Polygon o MultiPolygon válido y no esté vacía."""
        if not isinstance(v, (Polygon, MultiPolygon)):
            raise ValueError(f"Se esperaba un objeto Polygon o MultiPolygon, se recibió {type(v)}")
        
        if v.is_empty:
            raise ValueError("La geometría del área no puede estar vacía.")
            
        return v

class AreaSolicitadaSustraer(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class CaracterizaDragado(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class DisposicionResiduosSolidos(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class DragadoyDisposicion(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class InfraProyectoLN(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class InfraProyectoPG(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class InfraProyectoPT(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class LineaProyecto(BaseEV_Geo):
    """
    Feature Class: LineaProyecto (Línea)
    Línea que representa el proyecto objeto de solicitud de licencia.
    Ej.: Oleoducto, Línea de Transmisión Eléctrica, Vía, Vía Férrea, etc.
    """
    model_config = ConfigDict(
        use_enum_values=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        populate_by_name=True
    )

    # === INFORMACIÓN ADMINISTRATIVA ===
    EXPEDIENTE: Optional[str] = Field(None, max_length=20, description="Número de expediente asignado por la ANLA")
    NUM_ACT_AD: Optional[str] = Field(None, max_length=20, description="Número de la resolución o acto administrativo")
    FEC_ACT_AD: Optional[date] = Field(None, description="Fecha de la resolución o acto administrativo")
    ART_ACT_AD: Optional[str] = Field(None, max_length=50, description="Artículo, parágrafo y/o numeral de la resolución")
    
    # === DATOS DEL PROYECTO ===
    SECTOR: Dom_Sector = Field(..., description="Identifica el sector al que corresponde el proyecto (Enum)")
    OPERADOR: str = Field(..., max_length=100, description="Empresa solicitante o titular de la licencia")
    PROYECTO: str = Field(..., max_length=200, description="Nombre del proyecto objeto de licenciamiento o licenciado")
    CONTRATO: str = Field(..., max_length=100, description="Contrato asociado al proyecto (ANH, UPME, ANI, etc.)")
    
    # === CARACTERÍSTICAS TÉCNICAS ===
    DESCRIP: str = Field(..., max_length=255, description="Descripción breve de las características generales")
    NOMENCLAT: str = Field(..., max_length=20, description="Nomenclatura para la línea del proyecto")
    OBSERV: Optional[str] = Field(None, max_length=255, description="Observaciones pertinentes para el elemento")
    LONGITUD_m: float = Field(..., description="Longitud en metros (m) de cada una de las líneas")

    # === GEOMETRÍA ===
    geometry: Union[LineString, MultiLineString] = Field(...)

    # --- VALIDACIONES ---

    @field_validator('LONGITUD_m')
    @classmethod
    def validate_positive_length(cls, v):
        """Valida que la longitud de la línea sea un número estrictamente positivo."""
        if v <= 0:
            raise ValueError(f"La longitud (LONGITUD_m) debe ser mayor a 0, se recibió {v}")
        return v

    @field_validator('geometry')
    @classmethod
    def validate_line_geometry(cls, v):
        """Valida que la geometría sea un LineString o MultiLineString válido y no esté vacía."""
        if not isinstance(v, (LineString, MultiLineString)):
            raise ValueError(f"Se esperaba un objeto LineString o MultiLineString, se recibió {type(v)}")
        
        if v.is_empty:
            raise ValueError("La geometría de la línea no puede estar vacía.")
            
        return v

class Zodmes(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

class ZonaPrestamoLateral(BaseEV_Geo):
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)
    pass

