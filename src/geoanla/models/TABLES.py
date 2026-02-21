from typing import Optional
from datetime import date
from pydantic import Field, ConfigDict, field_validator, model_validator
from geoanla.core.base import BaseEV
from geoanla.catalog import (
    Dom_Apendice,
    Dom_Amenaza,
    Dom_Tipo_Distribu,
    Dom_Veda,
    Dom_EntidadVeda,
    Dom_Vigencia,
    Dom_Uso_Flora,
    Dom_Habito,
    Dom_Regeneracion,
    Dom_Tipo_Actadmin,
    Dom_EstInver
)
import math

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
    def validar_metricas_fustales(cls, v):
        """Asegura que los valores Single sean positivos, no nulos y redondeados."""
        if v is None or (isinstance(v, float) and math.isnan(v)):
            raise ValueError("Las variables métricas son obligatorias y no pueden ser NaN.")
        # Redondeo a 8 decimales para precisión en GDB
        return round(float(v), 8)

    # --- VALIDACIONES LÓGICAS (MODEL VALIDATORS) ---

    @model_validator(mode='after')
    def validar_consistencia_alturas(self):
        """La altura comercial (H_FUSTE) no puede ser mayor a la total (H_TOTAL)."""
        if self.H_FUSTE > self.H_TOTAL:
            raise ValueError(
                f"Inconsistencia en alturas: H_FUSTE ({self.H_FUSTE}) no puede superar a H_TOTAL ({self.H_TOTAL})"
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

    @field_validator('ABUNDANCIA', 'ABUND_REL', 'FRECUENCIA', 'FRECU_REL', 'DOMINANCIA', 'DOM_REL', 'IVI', mode='before')
    @classmethod
    def validar_estructura_y_limpieza(cls, v):
        # 1. BLOQUEO DE NULOS Y VACÍOS:
        if v is None or (isinstance(v, float) and math.isnan(v)):
            raise ValueError("Este campo estructural es obligatorio y no puede estar vacío (NaN/Null)")
        # 2. GARANTÍA DE FLOAT Y PRECISIÓN (8 decimales para GDB):
        return round(float(v), 8)

    # --- VALIDACIONES LÓGICAS (MODEL VALIDATORS) ---

    @model_validator(mode='after')
    def validar_fechas(self) -> 'MuestreoFloraResultadosTB':
        if self.FECHA_IMUE > self.FECHA_FMUE:
            raise ValueError(f"La Fecha Inicio ({self.FECHA_IMUE}) no puede ser posterior a la Fecha Fin ({self.FECHA_FMUE})")
        return self

    @model_validator(mode='after')
    def validar_condicional_veda(self) -> 'MuestreoFloraResultadosTB':
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
                raise ValueError(f"Si hay veda, los campos {', '.join(errores)} son obligatorios.")
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
    def validar_condicional_veda_regen(self) -> 'MuestreoFloraRegeneracionTB':
        """
        Si VEDA tiene un código asignado, los campos relacionados
        deben ser obligatorios según la lógica de condicionalidad.
        """
        if self.VEDA is not None:
            errores = []
            if not self.RESOLUCION: errores.append("RESOLUCION")
            if self.ENTID_VEDA is None: errores.append("ENTID_VEDA")
            if self.VIGEN_VEDA is None: errores.append("VIGEN_VEDA")

            if errores:
                raise ValueError(f"Si la especie está en VEDA, los campos {', '.join(errores)} son obligatorios.")
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
    def validar_relacion_compensacion(self) -> 'Seg_CompensacionesTB':
        """
        Regla de Integridad Relacional: La tabla debe vincularse obligatoriamente 
        a una de las dos capas geográficas (Compensación por pérdida u Otra compensación).
        """
        if not self.ID_COMP and not self.ID_OT_COMP:
            raise ValueError("Fallo de integridad: Debe diligenciarse obligatoriamente 'ID_COMP' o 'ID_OT_COMP' para establecer la relación espacial.")
        return self

    @model_validator(mode='after')
    def validar_fechas_cronologicas(self) -> 'Seg_CompensacionesTB':
        """Asegura la coherencia temporal de las fechas de la actividad y del reporte."""
        errores = []
        if self.FEC_INI_AC and self.FEC_TER_AC:
            if self.FEC_TER_AC < self.FEC_INI_AC:
                errores.append(f"Cronología Actividad: FEC_TER_AC ({self.FEC_TER_AC}) no puede ser menor a FEC_INI_AC ({self.FEC_INI_AC})")

        if self.FECHA_INI and self.FECHA_FIN:
            if self.FECHA_FIN < self.FECHA_INI:
                errores.append(f"Cronología Reporte: FECHA_FIN ({self.FECHA_FIN}) no puede ser menor a FECHA_INI ({self.FECHA_INI})")

        if errores:
            raise ValueError(" | ".join(errores))

        return self

    @model_validator(mode='after')
    def validar_cumplimiento(self) -> 'Seg_CompensacionesTB':
        """Si se reporta una fecha de acto de cumplimiento, debe existir el número del acto."""
        if self.FE_ACT_CUM and not self.NO_ACT_CUM:
             raise ValueError("Inconsistencia: Si se registra fecha de cumplimiento ('FE_ACT_CUM'), es obligatorio reportar el número del acto en 'NO_ACT_CUM'")
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

    # ==========================================
    # VALIDACIONES LÓGICAS DE NEGOCIO
    # ==========================================

    @model_validator(mode='after')
    def validar_llave_foranea(self) -> 'Seg_IndicadoresTB':
        """
        Garantiza que el indicador esté atado a por lo menos una inversión o compensación.
        Si todos los ID están vacíos, es un registro huérfano.
        """
        ids_relacionales = [
            self.ID_INVER, self.ID_INV_PT, self.ID_INV_PG, 
            self.ID_INV_LN, self.ID_COMP, self.ID_OT_COMP
        ]
        
        # Verifica si al menos uno de los IDs tiene contenido (no es None ni string vacío)
        if not any(bool(identificador) for identificador in ids_relacionales):
            raise ValueError(
                "Fallo de integridad: Un indicador no puede quedar huérfano. "
                "Debe diligenciar al menos uno de los campos de relación (ID_INVER, ID_INV_PG, ID_COMP, etc.)."
            )
        return self

    @model_validator(mode='after')
    def validar_fechas_cronologicas(self) -> 'Seg_IndicadoresTB':
        """Asegura la coherencia del periodo reportado."""
        if self.FECHA_INI and self.FECHA_FIN:
            if self.FECHA_FIN < self.FECHA_INI:
                raise ValueError(
                    f"Cronología de periodo inválida: FECHA_FIN ({self.FECHA_FIN}) "
                    f"no puede ser anterior a FECHA_INI ({self.FECHA_INI})."
                )
        return self
