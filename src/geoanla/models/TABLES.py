from datetime import date, datetime
from typing import ClassVar, Optional
import math

from pydantic import ConfigDict, Field, field_validator, model_validator

from geoanla.catalog import (
    Dom_Amenaza,
    Dom_Apendice,
    Dom_Boolean,
    Dom_CAR,
    Dom_Deter,
    Dom_Dieta,
    Dom_EntidadVeda,
    Dom_EstInver,
    Dom_FC_Multimedia,
    Dom_Habito,
    Dom_ModInterv,
    Dom_Otras_Comp,
    Dom_Regeneracion,
    Dom_SubAct_Comp,
    Dom_Tipo_Actadmin,
    Dom_Tipo_Distribu,
    Dom_Tipo_Migra,
    Dom_Uso_Fauna,
    Dom_Uso_Flora,
    Dom_Veda,
    Dom_Vigencia
)
from geoanla.core.base import BaseEV


class MuestreoFloraFustalTB(BaseEV):
    """
    Tabla de Muestreo de Flora - Fustales (Individuos con DAP >= 10cm).
    Esta tabla no contiene geometría y se relaciona con PuntoMuestreoFlora mediante ID_MUEST.
    """
    model_config = ConfigDict(
        use_enum_values=True,
        validate_assignment=True,
        populate_by_name=True
    )

    # === BLOQUE 1: IDENTIFICACIÓN Y RELACIONES ===
    # ID_MUEST debe cruzar con la capa PuntoMuestreoFlora
    EXPEDIENTE: Optional[str] = Field(None, max_length=20)
    ID_MUEST: str = Field(..., max_length=20)
    ID_S_MUEST: Optional[str] = Field(None, max_length=20)
    ID_INDV_MU: str = Field(..., max_length=20)

    # === BLOQUE 2: TAXONOMÍA (Obligatorios) ===
    DIVISION: str = Field(..., max_length=50)
    CLASE: str = Field(..., max_length=50)
    ORDEN: str = Field(..., max_length=50)
    FAMILIA: str = Field(..., max_length=50)
    GENERO: str = Field(..., max_length=50)
    ESPECIE: str = Field(..., max_length=50)
    N_COMUN: str = Field(..., max_length=50)

    # === BLOQUE 3: MÉTRICAS ALOMÉTRICAS Y VARIABLES (Single 4 -> float) ===
    DAP_INDIV: float = Field(..., ge=0.0)    # Diámetro a la altura del pecho (m)
    AB_INDIV: float = Field(..., ge=0.0)     # Área basal (m2)
    H_TOTAL: float = Field(..., ge=0.0)      # Altura total (m)
    H_FUSTE: float = Field(..., ge=0.0)      # Altura comercial (m)
    VOL_TOTAL: float = Field(..., ge=0.0)    # Volumen total (m3)
    VOL_COM: float = Field(..., ge=0.0)      # Volumen comercial (m3)
    BIOM_INDIV: float = Field(..., ge=0.0)   # Biomasa (kg)
    CARB_INDIV: float = Field(..., ge=0.0)   # Carbono (kg)

    OBSERV: Optional[str] = Field(None, max_length=255)

    # --- VALIDACIONES DE CAMPO (FIELD VALIDATORS) ---

    @field_validator(
        'DAP_INDIV', 'AB_INDIV', 'H_TOTAL', 'H_FUSTE',
        'VOL_TOTAL', 'VOL_COM', 'BIOM_INDIV', 'CARB_INDIV'
    )
    @classmethod
    def validate_fustal_metrics(cls, v):
        """Asegura que los valores sean positivos, no nulos y redondeados."""
        if v is None or (isinstance(v, float) and math.isnan(v)):
            raise ValueError("Las variables métricas no pueden ser NaN.")
        return round(float(v), 8)

    # --- VALIDACIONES LÓGICAS (MODEL VALIDATORS) ---

    @model_validator(mode='after')
    def validate_height_consistency(self):
        """La altura comercial no puede ser mayor a la total."""
        if self.H_FUSTE > self.H_TOTAL:
            raise ValueError(
                f"Inconsistencia: H_FUSTE ({self.H_FUSTE}) > "
                f"H_TOTAL ({self.H_TOTAL})"
            )
        return self


class MuestreoFloraResultadosTB(BaseEV):
    """
    Tabla de Muestreo de Flora - Resultados de Caracterización.
    Consolida información taxonómica, estructural y estado de conservación.
    """
    model_config = ConfigDict(
        use_enum_values=True,
        validate_assignment=True,
        populate_by_name=True
    )

    CAMPO_LEYENDA: ClassVar[str] = "N_COBERT"

    # === IDENTIFICACIÓN ===
    EXPEDIENTE: Optional[str] = Field(None, max_length=20)
    PROYECTO: str = Field(..., max_length=200)

    # === LOCALIZACIÓN Y COBERTURA ===
    N_COBERT: str = Field(..., max_length=100)
    NOMENCLAT: int = Field(...)
    ECOSISTEMA: Optional[str] = Field(None, max_length=255)

    # === TAXONOMÍA ===
    DIVISION: str = Field(..., max_length=50)
    CLASE: str = Field(..., max_length=50)
    ORDEN: str = Field(..., max_length=50)
    FAMILIA: str = Field(..., max_length=50)
    GENERO: str = Field(..., max_length=50)
    ESPECIE: str = Field(..., max_length=50)
    N_COMUN: str = Field(..., max_length=50)
    INDIVIDUOS: int = Field(..., ge=0)

    # === ESTADO DE CONSERVACIÓN Y DISTRIBUCIÓN (Double 8 -> float) ===
    CATEG_CIT: Dom_Apendice = Field(...)
    CATEG_UICN: Dom_Amenaza = Field(...)
    CATE_MINIS: Dom_Amenaza = Field(...)
    T_DISTRIB: Dom_Tipo_Distribu = Field(...)

    # === VEDAS (Double 8 -> float) ===
    VEDA: Optional[Dom_Veda] = Field(None)
    RESOLUCION: Optional[str] = Field(None, max_length=20)
    ENTID_VEDA: Optional[Dom_EntidadVeda] = Field(None)
    VIGEN_VEDA: Optional[Dom_Vigencia] = Field(None)

    # === PARÁMETROS ESTRUCTURALES ===
    ABUNDANCIA: float = Field(..., ge=0.0)
    ABUND_REL: float = Field(..., ge=0.0, le=100.0)
    FRECUENCIA: float = Field(..., ge=0.0)
    FRECU_REL: float = Field(..., ge=0.0, le=100.0)
    DOMINANCIA: float = Field(..., ge=0.0)
    DOMIN_REL: float = Field(..., ge=0.0, le=100.0)
    IVI: float = Field(..., ge=0.0, le=300.0)

    # === RASGOS FUNCIONALES Y MADERA ===
    USO: Dom_Uso_Flora = Field(...)
    TIPO_HAB: Dom_Habito = Field(...)
    DEN_MADERA: float = Field(..., ge=0)
    MET_DENSID: str = Field(..., max_length=50)

    # === VOLUMEN Y BIOMASA ===
    VOL_COM: float = Field(..., ge=0)
    VOL_TOTAL: float = Field(..., ge=0)
    BIOM_TOT: float = Field(..., ge=0)
    CARB_TOT: float = Field(..., ge=0)

    # === TEMPORALIDAD ===
    FECHA_IMUE: date = Field(...)
    FECHA_FMUE: date = Field(...)
    OBSERV: Optional[str] = Field(None, max_length=255)

    # --- VALIDACIONES DE CAMPO (FIELD VALIDATORS) ---

    @field_validator(
        'ABUNDANCIA', 'ABUND_REL', 'FRECUENCIA', 'FRECU_REL',
        'DOMINANCIA', 'DOMIN_REL', 'IVI', mode='before'
    )
    @classmethod
    def validate_structure_and_cleanup(cls, v):
        """Bloquea nulos y garantiza precisión."""
        if v is None or (isinstance(v, float) and math.isnan(v)):
            raise ValueError("Campo estructural obligatorio no puede ser NaN.")
        return round(float(v), 8)

    # --- VALIDACIONES LÓGICAS (MODEL VALIDATORS) ---

    @model_validator(mode='after')
    def validate_dates(self) -> 'MuestreoFloraResultadosTB':
        """Valida que la fecha inicio no sea posterior a la fin."""
        if self.FECHA_IMUE > self.FECHA_FMUE:
            raise ValueError("Fallo cronológico en fechas de muestreo.")
        return self

    @model_validator(mode='after')
    def validate_conditional_veda(self) -> 'MuestreoFloraResultadosTB':
        """Valida campos obligatorios si hay veda."""
        if self.VEDA is not None:
            errores = []
            if not self.RESOLUCION:
                errores.append("RESOLUCION")
            if self.ENTID_VEDA is None:
                errores.append("ENTID_VEDA")
            if self.VIGEN_VEDA is None:
                errores.append("VIGEN_VEDA")
            if errores:
                raise ValueError(f"Campos veda requeridos: {', '.join(errores)}")
        return self

class MuestreoFloraRegeneracionTB(BaseEV):
    """
    Tabla: MuestreoFloraRegeneracionTB
    Descripción: Detalla la información de regeneración natural y otros tipos de vegetación.
    """
    model_config = ConfigDict(
        use_enum_values=True,
        validate_assignment=True,
        populate_by_name=True
    )

    # === BLOQUE 1: IDENTIFICACIÓN Y RELACIONES ===
    EXPEDIENTE: Optional[str] = Field(None, max_length=20, description="Número de expediente ANLA")
    ID_MUEST: str = Field(..., max_length=20, description="ID del Punto de Muestreo (Debe coincidir con PuntoMuestreoFlora)")
    ID_S_MUEST: Optional[str] = Field(None, max_length=20, description="ID de la subunidad de muestreo")

    # === BLOQUE 2: TAXONOMÍA ===
    DIVISION: str = Field(..., max_length=50)
    CLASE: str = Field(..., max_length=50)
    ORDEN: str = Field(..., max_length=50)
    FAMILIA: str = Field(..., max_length=50)
    GENERO: str = Field(..., max_length=50)
    ESPECIE: str = Field(..., max_length=50)
    N_COMUN: str = Field(..., max_length=50)

    # === BLOQUE 3: ESTADO DE CONSERVACIÓN Y DISTRIBUCIÓN (Double 8) ===
    CATEG_CIT: Dom_Apendice = Field(..., description="Apéndice CITES")
    CATEG_UICN: Dom_Amenaza = Field(..., description="Categoría UICN")
    CATE_MINIS: Dom_Amenaza = Field(..., description="Categoría Resolución 192 de 2014")
    T_DISTRIB: Dom_Tipo_Distribu = Field(..., description="Categoría de distribución")

    # === BLOQUE 4: VEDAS (Double 8 / String 20) ===
    VEDA: Optional[Dom_Veda] = Field(None, description="Nivel de veda si aplica")
    RESOLUCION: Optional[str] = Field(None, max_length=20, description="Número de resolución de veda")
    ENTID_VEDA: Optional[Dom_EntidadVeda] = Field(None, description="Entidad que establece la veda")
    VIGEN_VEDA: Optional[Dom_Vigencia] = Field(None, description="Vigencia de la veda")

    # === BLOQUE 5: VARIABLES DE REGENERACIÓN Y CONTEO ===
    T_REGEN: Dom_Regeneracion = Field(..., description="Categoría de tamaño (SmallInteger 2)")
    TIPO_HAB: Dom_Habito = Field(..., description="Hábito de crecimiento (Double 8)")
    INDIVIDUOS: int = Field(..., ge=0, description="Número de individuos (Integer 4)")

    OBSERV: Optional[str] = Field(None, max_length=255)

    # --- VALIDACIONES LÓGICAS (MODEL VALIDATORS) ---

    @model_validator(mode='after')
    def validate_conditional_veda_regeneration(self) -> 'MuestreoFloraRegeneracionTB':
        """Valida campos de veda si aplica."""
        if self.VEDA is not None:
            errores = []
            if not self.RESOLUCION:
                errores.append("RESOLUCION")
            if self.ENTID_VEDA is None:
                errores.append("ENTID_VEDA")
            if self.VIGEN_VEDA is None:
                errores.append("VIGEN_VEDA")
            if errores:
                raise ValueError(f"Falta info de veda: {', '.join(errores)}")
        return self

class Seg_CompensacionesTB(BaseEV):
    """
    Tabla alfanumérica: Seguimiento actividades de Compensación (Seg_CompensacionesTB)
    Sin geometría. Relacionada mediante ID_COMP o ID_OT_COMP.
    """
    model_config = ConfigDict(
        use_enum_values=True,
        validate_assignment=True,
        populate_by_name=True
    )

    # === INFORMACIÓN ADMINISTRATIVA ===
    EXPEDIENTE: str = Field(..., max_length=20, description="Obligatorio")
    OPERADOR: str = Field(..., max_length=100, description="Obligatorio")
    PROYECTO: str = Field(..., max_length=200, description="Obligatorio")

    # === LLAVES FORÁNEAS (Relación espacial) ===
    ID_COMP: Optional[str] = Field(None, max_length=20, description="Condicional (Compensación Biodiversidad)")
    ID_OT_COMP: Optional[str] = Field(None, max_length=20, description="Condicional (Otra Compensación)")

    # === ACTOS ADMINISTRATIVOS ===
    NO_ACTOAD: int = Field(..., description="SmallInteger: Obligatorio")
    FE_ACTOAD: date = Field(..., description="Obligatorio")
    T_ACTO_OBL: Dom_Tipo_Actadmin = Field(..., description="Obligatorio")
    RES_OBL: int = Field(..., description="SmallInteger: Obligatorio")
    FE_OBL: date = Field(..., description="Obligatorio")

    # Acto que da por cumplida la obligación
    NO_ACT_CUM: Optional[int] = Field(None, description="Condicional (SmallInteger)")
    FE_ACT_CUM: Optional[date] = Field(None, description="Condicional")

    # === ESTADO Y CRONOGRAMA DE ACTIVIDADES ===
    ESTADO: Dom_EstInver = Field(..., description="Obligatorio")
    FEC_INI_AC: date = Field(..., description="Obligatorio")
    FEC_TER_AC: date = Field(..., description="Obligatorio")

    # === REPORTE ICA Y PERIODO EVALUADO ===
    ID_ICA: Optional[int] = Field(None, description="Condicional (SmallInteger)")
    FECHA_INI: date = Field(..., description="Obligatorio")
    FECHA_FIN: date = Field(..., description="Obligatorio")

    # === VALORES ECONÓMICOS ===
    PREC_SUELO: float = Field(..., ge=0.0, description="Precio tierra/ha (COP)")
    EJ_ACU_ACT: float = Field(..., ge=0.0, description="Ejecución acumulada (COP)")
    V_INV_EJ: float = Field(..., ge=0.0, description="Valor inversión periodo (COP)")

    # === OBSERVACIONES ===
    OBS_CP: Optional[str] = Field(None, max_length=255, description="Opcional")

    # ==========================================
    # VALIDACIONES LÓGICAS (REGLAS DE NEGOCIO)
    # ==========================================

    @model_validator(mode='after')
    def validate_compensation_relation(self) -> 'Seg_CompensacionesTB':
        """Valida vínculo a capa geográfica."""
        if not self.ID_COMP and not self.ID_OT_COMP:
            raise ValueError("Debe vincularse a ID_COMP o ID_OT_COMP.")
        return self

    @model_validator(mode='after')
    def validate_chronological_dates(self) -> 'Seg_CompensacionesTB':
        """Valida coherencia temporal."""
        if self.FEC_TER_AC < self.FEC_INI_AC:
            raise ValueError("FEC_TER_AC no puede ser anterior a FEC_INI_AC.")
        if self.FECHA_FIN < self.FECHA_INI:
            raise ValueError("FECHA_FIN no puede ser anterior a FECHA_INI.")
        return self

    @model_validator(mode='after')
    def validate_compliance(self) -> 'Seg_CompensacionesTB':
        """Valida consistencia en acto de cumplimiento."""
        if self.FE_ACT_CUM and not self.NO_ACT_CUM:
             raise ValueError("Falta NO_ACT_CUM para la fecha de cumplimiento.")
        return self

class Seg_IndicadoresTB(BaseEV):
    """
    Tabla alfanumérica: Indicadores para el seguimiento de actividades (Seg_IndicadoresTB)
    Sin geometría. Relacionada mediante múltiples IDs a Compensación o Inversión 1%.
    """
    model_config = ConfigDict(
        use_enum_values=True,
        validate_assignment=True,
        populate_by_name=True
    )

    # === INFORMACIÓN ADMINISTRATIVA ===
    EXPEDIENTE: str = Field(..., max_length=20, description="Obligatorio")

    # === LLAVES FORÁNEAS (Condicionales, pero al menos una debe existir) ===
    ID_INVER: Optional[str] = Field(None, max_length=20, description="Relación con Inversion1PorCientoTB")
    ID_INV_PT: Optional[str] = Field(None, max_length=20, description="Relación con Inversion1PorCientoPT")
    ID_INV_PG: Optional[str] = Field(None, max_length=20, description="Relación con Inversion1PorCientoPG")
    ID_INV_LN: Optional[str] = Field(None, max_length=20, description="Relación con Inversion1PorCientoLN")
    ID_COMP: Optional[str] = Field(None, max_length=20, description="Relación con CompensacionBiodiversidad")
    ID_OT_COMP: Optional[str] = Field(None, max_length=20, description="Relación con OtraCompensacion")

    # === REPORTE Y PERIODO ===
    ID_ICA: Optional[int] = Field(None, description="SmallInteger: Número de ICA")
    FECHA_INI: date = Field(..., description="Fecha inicial del periodo reportado")
    FECHA_FIN: date = Field(..., description="Fecha final del periodo reportado")

    # === INDICADORES TÉCNICOS ===
    IND_EF_GES: str = Field(..., max_length=255, description="Indicador de eficiencia de gestión")
    VAL_NOPUM: float = Field(..., description="Single: Valor del indicador de eficiencia técnica")
    
    # OJO: Mantenemos el error tipográfico "OBSEVACIO" tal como lo dicta el diccionario ANLA
    OBSEVACIO: Optional[str] = Field(None, max_length=255, description="Opcional")

    # --- VALIDACIONES LÓGICAS ---

    @model_validator(mode='after')
    def validate_foreign_key(self) -> 'Seg_IndicadoresTB':
        """Garantiza que no sea un registro huérfano."""
        ids = [
            self.ID_INVER, self.ID_INV_PT, self.ID_INV_PG, 
            self.ID_INV_LN, self.ID_COMP, self.ID_OT_COMP
        ]
        if not any(bool(i) for i in ids):
            raise ValueError("El indicador debe estar atado a una inversión.")
        return self

    @model_validator(mode='after')
    def validate_chronological_dates(self) -> 'Seg_IndicadoresTB':
        """Asegura la coherencia del periodo."""
        if self.FECHA_FIN < self.FECHA_INI:
            raise ValueError("Periodo de reporte inválido.")
        return self

class Seg_EspSembradaTB(BaseEV):
    """
    Tabla: Seg_EspSembradaTB
    Descripción: Seguimiento Especies Sembradas en Compensaciones e inversiones 1%.
    Determina las especies sembradas en las áreas de compensación o inversión.
    """
    model_config = ConfigDict(
        use_enum_values=True,
        validate_assignment=True,
        populate_by_name=True
    )

    # === BLOQUE 1: IDENTIFICACIÓN Y RELACIONES ===
    EXPEDIENTE: str = Field(..., max_length=20)
    ID_COMP: Optional[str] = Field(None, max_length=20)
    ID_OT_COMP: Optional[str] = Field(None, max_length=20)
    ID_INVER: Optional[str] = Field(None, max_length=20)
    ID_INV_PG: Optional[str] = Field(None, max_length=20)

    # === BLOQUE 2: DETALLES DE SIEMBRA ===
    FECHA_SIEM: date = Field(...)
    ESPEC_SEMB: str = Field(..., max_length=100)
    AREA_ESPEC: float = Field(..., ge=0.0)
    ALTUR_SEMB: float = Field(..., ge=0.0)
    DAP_SEMB: float = Field(..., ge=0.0)
    DEN_MADERA: Optional[float] = Field(None, ge=0.0)
    INDIV_SEMB: float = Field(..., ge=0.0)
    DEN_SIEMB: float = Field(..., ge=0.0)

    # === BLOQUE 3: ESTRATEGIA DE INTERVENCIÓN ===
    MOD_INTERV: Dom_ModInterv = Field(...)
    OT_MOD_INT: Optional[str] = Field(None, max_length=100)

    # === BLOQUE 4: SUPERVIVENCIA ===
    # Le agregamos le=100.0 directo en el Field porque la tabla exige que sean porcentajes (0-100)
    SUPERV: float = Field(..., ge=0.0, le=100.0)
    TOT_IN_SMB: float = Field(..., ge=0.0)
    TOT_SUPERV: float = Field(..., ge=0.0, le=100.0)

    # === BLOQUE 5: MANTENIMIENTO ===
    T_MANTENIM: float = Field(..., ge=0.0)
    MANT_PER: int = Field(..., ge=0)
    MANT_TOT: str = Field(..., max_length=20)
    FREC_MANT: str = Field(..., max_length=50)
    FEC_MANT: Optional[date] = Field(None)
    ACT_MANT: str = Field(..., max_length=100)

    # === BLOQUE 6: CONTROL ===
    FECHA_INFO: date = Field(...)
    OBSERV: Optional[str] = Field(None, max_length=255)

    # ==========================================
    # VALIDACIONES LÓGICAS (REGLAS DE NEGOCIO)
    # ==========================================

    # --- VALIDACIONES LÓGICAS ---

    @model_validator(mode='after')
    def validate_foreign_key(self) -> 'Seg_EspSembradaTB':
        """Garantiza vínculo a inversión o compensación."""
        ids = [self.ID_COMP, self.ID_OT_COMP, self.ID_INVER, self.ID_INV_PG]
        if not any(bool(i) for i in ids):
            raise ValueError("Requiere vínculo a ID_COMP, ID_INVER, etc.")
        return self

    @model_validator(mode='after')
    def validate_conditional_other_strategy(self) -> 'Seg_EspSembradaTB':
        """Valida que se especifique 'Otra estrategia'."""
        if self.MOD_INTERV == 22.0 and not self.OT_MOD_INT:
            raise ValueError("Debe especificar 'OT_MOD_INT'.")
        return self

    @model_validator(mode='after')
    def validate_chronological_dates(self) -> 'Seg_EspSembradaTB':
        """Valida cronología entre siembra y mantenimiento."""
        if self.FEC_MANT and self.FEC_MANT < self.FECHA_SIEM:
            raise ValueError("Mantenimiento anterior a siembra.")
        return self

class MuestreoFaunaResultadosTB(BaseEV):
    """
    Tabla de Muestreo de Fauna - Resultados.
    Relaciona y detalla las especies encontradas en el muestreo de fauna a nivel de taxonomía y coberturas.
    """
    model_config = ConfigDict(
        use_enum_values=True,
        validate_assignment=True,
        populate_by_name=True
    )

    CAMPO_LEYENDA: ClassVar[str] = "N_COBERT"

    # === BLOQUE 1: IDENTIFICACIÓN ===
    EXPEDIENTE: Optional[str] = Field(None, max_length=20)
    PROYECTO: str = Field(..., max_length=200)

    # === BLOQUE 2: LOCALIZACIÓN Y COBERTURA ===
    N_COBERT: str = Field(..., max_length=100)
    NOMENCLAT: int = Field(...)

    # === BLOQUE 3: TAXONOMÍA ===
    DIVISION: str = Field(..., max_length=50)
    CLASE: str = Field(..., max_length=50)
    ORDEN: str = Field(..., max_length=50)
    FAMILIA: str = Field(..., max_length=50)
    GENERO: str = Field(..., max_length=50)
    ESPECIE: str = Field(..., max_length=50)
    N_COMUN: str = Field(..., max_length=50)

    # === BLOQUE 4: ESTADO DE CONSERVACIÓN Y DISTRIBUCIÓN ===
    CATEG_CIT: 'Dom_Apendice' = Field(...)
    CATEG_UICN: 'Dom_Amenaza' = Field(...)
    CATE_MINIS: 'Dom_Amenaza' = Field(...)
    T_DISTRIB: 'Dom_Tipo_Distribu' = Field(...)
    MIGRACION: 'Dom_Boolean' = Field(...)
    TIPO_MIGR: Optional['Dom_Tipo_Migra'] = Field(None)

    # === BLOQUE 5: VEDAS ===
    VEDA: Optional['Dom_Veda'] = Field(None)
    RESOLUCION: Optional[str] = Field(None, max_length=20)
    ENTID_VEDA: Optional['Dom_EntidadVeda'] = Field(None)
    VIGEN_VEDA: Optional['Dom_Vigencia'] = Field(None)

    # === BLOQUE 6: ABUNDANCIA Y ECOLOGÍA ===
    ABUND_ABS: float = Field(..., ge=0.0)
    ABUND_REL: float = Field(..., ge=0.0, le=100.0)
    USO: 'Dom_Uso_Fauna' = Field(...)
    DIETA: 'Dom_Dieta' = Field(...)
    DISTR_ALT: str = Field(..., max_length=20)

    # === BLOQUE 7: TEMPORALIDAD Y OBSERVACIONES ===
    FECHA_IMUE: date = Field(...)
    FECHA_FMUE: date = Field(...)
    OBSERV: Optional[str] = Field(None, max_length=255)

    # ==========================================
    # VALIDACIONES DE CAMPO (FIELD VALIDATORS)
    # ==========================================

    @field_validator('ABUND_ABS', 'ABUND_REL', mode='before')
    @classmethod
    def validate_structure_and_cleanup(cls, v):
        """Bloquea nulos/NaNs and garantiza el casteo a float con precisión."""
        if v is None or (isinstance(v, float) and math.isnan(v)):
            raise ValueError("El campo de abundancia es obligatorio y no puede estar vacío (NaN/Null)")
        return round(float(v), 8)

    # ==========================================
    # VALIDACIONES LÓGICAS (MODEL VALIDATORS)
    # ==========================================

    @model_validator(mode='after')
    def validate_dates(self) -> 'MuestreoFaunaResultadosTB':
        """Asegura la coherencia temporal de los muestreos."""
        if self.FECHA_IMUE and self.FECHA_FMUE:
            if self.FECHA_IMUE > self.FECHA_FMUE:
                raise ValueError(f"Cronología: La Fecha Inicio ({self.FECHA_IMUE}) no puede ser posterior a la Fecha Fin ({self.FECHA_FMUE})")
        return self

    @model_validator(mode='after')
    def validate_conditional_veda(self) -> 'MuestreoFaunaResultadosTB':
        """
        Si VEDA tiene un código asignado, los campos relacionados
        pasan de ser opcionales a obligatorios.
        """
        if self.VEDA is not None:
            errores = []
            if not self.RESOLUCION: errores.append("RESOLUCION")
            if self.ENTID_VEDA is None: errores.append("ENTID_VEDA")
            if self.VIGEN_VEDA is None: errores.append("VIGEN_VEDA")

            if errores:
                raise ValueError(f"Fallo de integridad: Si la especie tiene VEDA, los campos {', '.join(errores)} son obligatorios.")
        return self

    @model_validator(mode='after')
    def validate_conditional_migration(self) -> 'MuestreoFaunaResultadosTB':
        """
        Garantiza que si la especie es migratoria, se especifique el tipo de migración.
        """
        # Suponiendo que el valor afirmativo en Dom_Boolean es 1.0 o True
        if self.MIGRACION == 1.0 or self.MIGRACION is True:
            if self.TIPO_MIGR is None:
                raise ValueError("Inconsistencia: Si 'MIGRACION' es afirmativa, debe diligenciar el campo 'TIPO_MIGR'.")
        return self

class RegistrosMultimediaTB(BaseEV):
    """
    Tabla: RegistrosMultimediaTB
    Descripción: Relaciona la ubicación y características de los registros multimedia
    asociados a los elementos de las diferentes capas temáticas.
    """
    model_config = ConfigDict(
        use_enum_values=True,
        validate_assignment=True,
        populate_by_name=True
    )

    # === BLOQUE 1: IDENTIFICACIÓN ===
    EXPEDIENTE: Optional[str] = Field(None, max_length=20, description="Número de expediente asignado por la ANLA")
    # Este identificador debe coincidir con el ID del feature class correspondiente
    ID_REG_MUL: str = Field(..., max_length=20, description="Identificador del elemento al cual pertenece el registro multimedia")

    # === BLOQUE 2: ASOCIACIÓN GEOGRÁFICA ===
    FEAT_CLASS: Dom_FC_Multimedia = Field(..., description="Feature class o capa geográfica asociada (Double 8)")

    # === BLOQUE 3: ARCHIVO Y TEMPORALIDAD ===
    UBIC_ARCHI: str = Field(..., max_length=255, description="Ruta relativa hasta el nombre o identificación del archivo")
    FEC_TOMA: date = Field(..., description="Fecha a la que corresponde el registro multimedia (Date 8)")

    # === BLOQUE 4: NOTAS ===
    OBSERV: Optional[str] = Field(None, max_length=255, description="Observaciones pertinentes para el elemento")

    # --- VALIDACIONES DE CAMPO ---

    @field_validator('FEC_TOMA', mode='before')
    @classmethod
    def normalize_catch_date(cls, v):
        """
        Asegura que la fecha no contenga horas (Double 8),
        especialmente útil cuando se carga desde Pandas.
        """
        if isinstance(v, datetime):
            return v.date()
        return v


class MuestreoFaunaTB(BaseEV):
    model_config = ConfigDict(
        use_enum_values=True,
        validate_assignment=True,
        populate_by_name=True
    )

    # === IDENTIFICACIÓN ===
    EXPEDIENTE: Optional[str] = Field(None, max_length=20)

    # RELACIÓN ESPACIAL (Condicionales: Debe existir al menos uno)
    ID_MUES_PT: Optional[str] = Field(None, max_length=20, description="ID del Punto (si aplica)")
    ID_MUES_TR: Optional[str] = Field(None, max_length=20, description="ID del Transecto (si aplica)")

    # === DETALLES DEL REGISTRO ===
    DETERM: Dom_Deter = Field(..., description="411:Captura, 413:Vista, 415:Oido...")
    OT_DETERM: Optional[str] = Field(None, max_length=50, description="Obligatorio si DETERM es Otro")

    # === TAXONOMÍA (Obligatoria) ===
    DIVISION: str = Field(..., max_length=50)
    CLASE: str = Field(..., max_length=50)
    ORDEN: str = Field(..., max_length=50)
    FAMILIA: str = Field(..., max_length=50)
    GENERO: str = Field(..., max_length=50)
    ESPECIE: str = Field(..., max_length=50)
    N_COMUN: str = Field(..., max_length=50)

    # === CANTIDAD ===
    # Aunque son individuos (enteros), ANLA pide Double (float).
    ABUND_ABS: float = Field(..., ge=0, description="Número de individuos registrados")

    # === OTROS ===
    OBSERV: Optional[str] = Field(None, max_length=255)

    # --- VALIDACIONES DE NEGOCIO ---

    @model_validator(mode='after')
    def validate_record_origin(self):
        """Valida que el registro esté asociado a un Punto O a un Transecto."""
        pt = getattr(self, 'ID_MUES_PT', None)
        tr = getattr(self, 'ID_MUES_TR', None)

        # Verificar si ambos son Nulos/Vacíos
        if not pt and not tr:
            raise ValueError("El registro debe estar asociado a un Punto (ID_MUES_PT) o a un Transecto (ID_MUES_TR). Ambos no pueden ser nulos.")
        return self

    @model_validator(mode='after')
    def validate_other_determination(self):
        """Si DETERM es 419 (Otro), OT_DETERM es obligatorio."""
        # 419 es el código asumiendo que es "Otro", según el contexto.
        if self.DETERM == 419.0 and not self.OT_DETERM:
            raise ValueError("Seleccionó 'Otro' en DETERM, debe especificar en OT_DETERM.")
        return self
