import geopandas as gpd
import numpy as np
import polars as pl
from typing import Optional, Dict, Any, Tuple, Type


def validate_gdb_layer(
    clase_modelo: Type,
    ruta_archivo_gdb: str,
    correcciones_leyenda: Optional[Dict[str, str]] = None
) -> Tuple[Any, Any, Any]:
    """
    Validates a geographic or tabular layer from a Geodatabase
    using a provided Pydantic model.

    Args:
        clase_modelo (Type): The Pydantic model class to validate against.
        ruta_archivo_gdb (str): Path to the Geodatabase file.
        correcciones_leyenda (Optional[Dict[str, str]]): Dictionary for
            legend corrections.

    Returns:
        Tuple containing detected errors, validated records, and the GDF.
    """
    nombre_capa = clase_modelo.__name__

    if clase_modelo is None:
        print(f"⚠️ Error: La clase para '{nombre_capa}' no está definida.")
        return None, None, None

    print(f"➜ Procesando: {nombre_capa}...")
    try:
        capa_gdb = gpd.read_file(ruta_archivo_gdb, layer=nombre_capa)
    except (FileNotFoundError, ValueError) as error_lectura:
        print(f"⚠️ Error leyendo la capa '{nombre_capa}': {error_lectura}")
        return None, None, None

    # 1. Renombrar columnas
    capa_gdb = capa_gdb.rename(
        columns={'AREA_HA': 'AREA_ha', 'LONGITUD_M': 'LONGITUD_m'}
    )

    # 2. Corregir leyendas de cobertura
    if correcciones_leyenda:
        if 'N_COBERT' in capa_gdb.columns:
            capa_gdb['N_COBERT'] = capa_gdb['N_COBERT'].replace(
                correcciones_leyenda
            )

        # 2.1 Corregir leyendas en OBSERV *solo* para CoberturaTierra
        if 'OBSERV' in capa_gdb.columns and nombre_capa == 'CoberturaTierra':
            capa_gdb['OBSERV'] = capa_gdb['OBSERV'].replace(
                correcciones_leyenda
            )

    # 3. Reemplazar NaN con None
    cols_atributos = [col for col in capa_gdb.columns if col != 'geometry']
    capa_gdb[cols_atributos] = capa_gdb[cols_atributos].replace({np.nan: None})

    # Extracción y validación
    extraccion = clase_modelo.extract(capa_gdb)
    registros, errores = clase_modelo.validate_data()

    print("✅ Completado.\n")
    return errores, registros, capa_gdb


# 1. Diccionario de Relaciones Directas (Padre -> Hijos)
RELACIONES_ANLA = {
    "PuntoMuestreoFlora": {
        "llave_padre": "ID_MUEST",
        "llave_hija": "ID_MUEST",
        "hijos": [
            "MuestreoFloraFustalTB",
            "MuestreoFloraRegeneracionTB",
            "MuestreoFloraResultadosTB"
        ]
    },
    "PuntoMuestreoFauna": {
        "llave_padre": "ID_MUES_PT",
        "llave_hija": "ID_MUEST_PT",
        "hijos": ["MuestreoFaunaTB", "MuestreoFaunaResultadosTB"]
    },
    "TransectoMuestreoFauna": {
        "llave_padre": "ID_MUES_TR",
        "llave_hija": "ID_MUEST_TR",
        "hijos": ["MuestreoFaunaTB", "MuestreoFaunaResultadosTB"]
    }
}

# 2. Diccionario extraído de Dom_FC_Multimedia
MAPA_MULTIMEDIA = {
    1107.0: "MaterialesConstruccionPT",
    1108.0: "MaterialesConstruccionPG",
    1502.0: "OcupacionCauce",
    1503.0: "CaptacionAguaSuperPT",
    1504.0: "CaptacionAguaSuperLN",
    1505.0: "VertimientoPT",
    1506.0: "VertimientoLN",
    1507.0: "VertimientoVia",
    1508.0: "VertimientoSuelo",
    1509.0: "PuntoMuestreoAguaSuper",
    2003.0: "PuntoMuestreoFlora",
    2004.0: "PuntoMuestreoFauna",
    2005.0: "TransectoMuestreoFauna",
    2007.0: "AprovechaForestalPT"
}


def cross_validator_entities(ruta_gdb: str) -> Tuple[pl.DataFrame, Dict[str, Any]]:
    """
    Validación cruzada de llaves entre entidades y la tabla multimedia.

    Args:
        ruta_gdb (str): Ruta a la geodatabase (.gdb)

    Returns:
        Tuple[pl.DataFrame, dict]: Resumen tabular y IDs huérfanos.
    """
    print("🚀 Iniciando Motor de Validación Cruzada...\n")

    resultados_resumen = []
    huerfanos_detalle = {}

    # ==========================================
    # FASE 1: VALIDACIÓN DE RELACIONES DIRECTAS
    # ==========================================
    for capa_padre, datos_relacion in RELACIONES_ANLA.items():
        llave_padre = datos_relacion["llave_padre"]
        llave_hija = datos_relacion["llave_hija"]
        tablas_hijas = datos_relacion["hijos"]

        # 1. Cargar la Capa Padre
        try:
            df_padre = gpd.read_file(
                ruta_gdb, layer=capa_padre, columns=[llave_padre],
                engine="pyogrio"
            )
            pl_padre = pl.DataFrame(df_padre[[llave_padre]]).drop_nulls()
        except Exception as error_padre:
            print(f"⚠️ Error leyendo la capa padre '{capa_padre}': {error_padre}")
            continue

        for tabla_hija in tablas_hijas:
            try:
                # 2. Cargar tabla hija
                df_hija = gpd.read_file(
                    ruta_gdb, layer=tabla_hija, columns=[llave_hija],
                    engine="pyogrio"
                )
                pl_hija = pl.DataFrame(df_hija[[llave_hija]]).drop_nulls()

                # 3. CRUCE MÁGICO CON POLARS
                huerfanos = pl_hija.join(
                    pl_padre, left_on=llave_hija, right_on=llave_padre,
                    how="anti"
                )
                cantidad_huerfanos = huerfanos.shape[0]

                estado = "OK" if cantidad_huerfanos == 0 else "ERROR"

                resultados_resumen.append({
                    "Entidad_A (Padre)": capa_padre,
                    "Entidad_B (Hija)": tabla_hija,
                    "Llave_Cruce": f"{llave_padre} == {llave_hija}",
                    "Estado": estado,
                    "Huérfanos_en_B": cantidad_huerfanos
                })

                if cantidad_huerfanos > 0:
                    nombre_error = f"{tabla_hija}_sin_{capa_padre}"
                    huerfanos_detalle[nombre_error] = (
                        huerfanos.to_series().to_list()
                    )

            except Exception:
                # Silencioso para hijos inexistentes
                pass

    # ==========================================
    # FASE 2: VALIDACIÓN DE REGISTROS MULTIMEDIA
    # ==========================================
    print("📸 Validando RegistrosMultimediaTB...\n")
    try:
        df_multi = gpd.read_file(
            ruta_gdb, layer="RegistrosMultimediaTB",
            columns=["ID_REG_MUL", "FEAT_CLASS"], engine="pyogrio"
        )
        pl_multi = pl.DataFrame(df_multi).drop_nulls(
            subset=["ID_REG_MUL", "FEAT_CLASS"]
        )

        para_validar = pl_multi.group_by("FEAT_CLASS").agg(pl.col("ID_REG_MUL"))

        for fila in para_validar.iter_rows(named=True):
            codigo_capa = fila["FEAT_CLASS"]
            ids_fotos = fila["ID_REG_MUL"]

            nombre_capa_dest = MAPA_MULTIMEDIA.get(
                codigo_capa, f"Desconocida_{codigo_capa}"
            )

            if nombre_capa_dest.startswith("Desconocida"):
                continue

            try:
                df_destino = gpd.read_file(
                    ruta_gdb, layer=nombre_capa_dest, engine="pyogrio"
                )
                cols_id = [c for c in df_destino.columns if c.startswith("ID_")]

                if cols_id:
                    llave_destino = cols_id[0]
                    pl_destino = pl.DataFrame(df_destino[[llave_destino]])\
                        .drop_nulls().rename({llave_destino: "ID_REG_MUL"})

                    pl_fotos = pl.DataFrame({"ID_REG_MUL": ids_fotos})

                    # CRUCE (Anti-Join)
                    fotos_huerfanas = pl_fotos.join(
                        pl_destino, on="ID_REG_MUL", how="anti"
                    )
                    cant_malas = fotos_huerfanas.shape[0]

                    estado = "OK" if cant_malas == 0 else "ERROR"

                    resultados_resumen.append({
                        "Entidad_A (Padre)": nombre_capa_dest,
                        "Entidad_B (Hija)": "RegistrosMultimediaTB",
                        "Llave_Cruce": f"ID_REG_MUL -> {llave_destino}",
                        "Estado": estado,
                        "Huérfanos_en_B": cant_malas
                    })

                    if cant_malas > 0:
                        huerfanos_detalle[f"Fotos_Huerfanas_{nombre_capa_dest}"] = \
                            fotos_huerfanas.to_series().to_list()
            except Exception as error_cruce:
                print(f"⚠️ Error cruzando con {nombre_capa_dest}: {error_cruce}")

    except Exception as error_multi:
        print(f"⚠️ No se pudo procesar RegistrosMultimediaTB: {error_multi}")

    df_resumen = pl.DataFrame(resultados_resumen) if resultados_resumen \
        else pl.DataFrame()
    print("📊 MATRIZ DE VALIDACIÓN CRUZADA:\n")
    print(df_resumen)

    return df_resumen, huerfanos_detalle

