import geopandas as gpd
import numpy as np
from typing import Optional, Dict, Any, Tuple, Type

def validate_gdb_layer(
    model_class: Type,
    gdb_file_path: str,
    legend_corrections: Optional[Dict[str, str]] = None
) -> Tuple[Any, Any, Any]:
    """
    Validates a geographic or tabular layer from a Geodatabase using a provided Pydantic model.
    
    Args:
        model_class (Type): The Pydantic model class to validate against. The class name will be used to locate the layer in the GDB.
        gdb_file_path (str): Path to the Geodatabase file.
        legend_corrections (Optional[Dict[str, str]]): Dictionary for legend corrections to be applied on 'N_COBERT' and 'OBSERV'.

    Returns:
        Tuple containing detected errors, validated records, and the extracted GeoDataFrame.
    """
    layer_name = model_class.__name__
    
    if model_class is None:
        print(f"⚠️ Error: The class for '{layer_name}' is not defined.")
        return None, None, None

    print(f"➜ Processing: {layer_name}...")
    try:
        layer_gdb = gpd.read_file(gdb_file_path, layer=layer_name)
    except Exception as e:
        print(f"⚠️ Error reading layer '{layer_name}': {e}")
        return None, None, None

    # 1. Rename columns
    layer_gdb = layer_gdb.rename(columns={'AREA_HA': 'AREA_ha', 'LONGITUD_M': 'LONGITUD_m'})

    # 2. Correct cover legends
    if legend_corrections:
        if 'N_COBERT' in layer_gdb.columns:
            layer_gdb['N_COBERT'] = layer_gdb['N_COBERT'].replace(legend_corrections)

        # 2.1 Correct legends in OBSERV *only* for CoberturaTierra
        if 'OBSERV' in layer_gdb.columns and layer_name == 'CoberturaTierra':
            layer_gdb['OBSERV'] = layer_gdb['OBSERV'].replace(legend_corrections)

    # 3. Replace NaN with None (Clean approach)
    # Select all columns except geometry to avoid damaging it
    cols_atributos = [col for col in layer_gdb.columns if col != 'geometry']
    layer_gdb[cols_atributos] = layer_gdb[cols_atributos].replace({np.nan: None})

    # Extraction and validation
    test = model_class.extract(layer_gdb)
    errores, registros = model_class.validate_data()

    print("✅ Completed.\n")
    return errores, registros, layer_gdb

import polars as pl

# 1. Diccionario de Relaciones Directas (Padre -> Hijos)
relaciones_anla = {
    "PuntoMuestreoFlora": {
        "llave_padre": "ID_MUEST",
        "llave_hija": "ID_MUEST",
        "hijos": ["MuestreoFloraFustalTB", "MuestreoFloraRegeneracionTB", "MuestreoFloraResultadosTB"]
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
mapa_multimedia = {
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

def cross_validator_entities(gdb_path: str) -> Tuple[pl.DataFrame, Dict[str, Any]]:
    """
    Validación cruzada de llaves entre entidades y la tabla de registros multimedia.
    
    Args:
        gdb_path (str): Ruta a la geodatabase (.gdb)
        
    Returns:
        Tuple[pl.DataFrame, dict]: Resumen tabular y diccionario de IDs huérfanos.
    """
    print("🚀 Iniciando Motor de Validación Cruzada...\n")

    resultados_resumen = []
    huerfanos_detalle = {}

    # ==========================================
    # FASE 1: VALIDACIÓN DE RELACIONES DIRECTAS
    # ==========================================
    for capa_padre, info in relaciones_anla.items():
        llave_padre = info["llave_padre"]
        llave_hija = info["llave_hija"]
        hijos = info["hijos"]

        # 1. Cargar la Capa Padre con su llave específica
        try:
            df_padre = gpd.read_file(gdb_path, layer=capa_padre, columns=[llave_padre], engine="pyogrio")
            pl_padre = pl.DataFrame(df_padre[[llave_padre]]).drop_nulls()
        except Exception as e:
            print(f"⚠️ Error leyendo la capa padre '{capa_padre}': {e}")
            continue

        for tabla_hija in hijos:
            try:
                # 2. Cargar tabla hija con su llave específica
                df_hija = gpd.read_file(gdb_path, layer=tabla_hija, columns=[llave_hija], engine="pyogrio")
                pl_hija = pl.DataFrame(df_hija[[llave_hija]]).drop_nulls()

                # 3. CRUCE MÁGICO CON POLARS (left_on y right_on)
                # Buscamos los IDs de la hija que NO están en el padre
                huerfanos = pl_hija.join(pl_padre, left_on=llave_hija, right_on=llave_padre, how="anti")
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
                    huerfanos_detalle[nombre_error] = huerfanos.to_series().to_list()

            except Exception as e:
                # Si la tabla hija no existe o no tiene la columna, la ignoramos silenciosamente
                pass

    # ==========================================
    # FASE 2: VALIDACIÓN DE REGISTROS MULTIMEDIA
    # ==========================================
    print("📸 Validando RegistrosMultimediaTB...\n")
    try:
        df_multi = gpd.read_file(gdb_path, layer="RegistrosMultimediaTB", columns=["ID_REG_MUL", "FEAT_CLASS"], engine="pyogrio")
        pl_multi = pl.DataFrame(df_multi).drop_nulls(subset=["ID_REG_MUL", "FEAT_CLASS"])

        para_validar = pl_multi.group_by("FEAT_CLASS").agg(pl.col("ID_REG_MUL"))

        for row in para_validar.iter_rows(named=True):
            codigo_capa = row["FEAT_CLASS"]
            ids_fotos = row["ID_REG_MUL"]

            nombre_capa_destino = mapa_multimedia.get(codigo_capa, f"Desconocida_{codigo_capa}")

            if nombre_capa_destino.startswith("Desconocida"):
                continue

            try:
                df_destino = gpd.read_file(gdb_path, layer=nombre_capa_destino, engine="pyogrio")
                cols_id = [c for c in df_destino.columns if c.startswith("ID_")]

                if cols_id:
                    llave_destino = cols_id[0]
                    pl_destino = pl.DataFrame(df_destino[[llave_destino]]).drop_nulls().rename({llave_destino: "ID_REG_MUL"})

                    pl_fotos = pl.DataFrame({"ID_REG_MUL": ids_fotos})

                    # CRUCE (Anti-Join)
                    fotos_huerfanas = pl_fotos.join(pl_destino, on="ID_REG_MUL", how="anti")
                    cant_fotos_malas = fotos_huerfanas.shape[0]

                    estado = "OK" if cant_fotos_malas == 0 else "ERROR"

                    resultados_resumen.append({
                        "Entidad_A (Padre)": nombre_capa_destino,
                        "Entidad_B (Hija)": "RegistrosMultimediaTB",
                        "Llave_Cruce": f"ID_REG_MUL -> {llave_destino}",
                        "Estado": estado,
                        "Huérfanos_en_B": cant_fotos_malas
                    })

                    if cant_fotos_malas > 0:
                        huerfanos_detalle[f"Fotos_Huerfanas_{nombre_capa_destino}"] = fotos_huerfanas.to_series().to_list()
            except Exception as e:
                print(f"⚠️ Error cruzando con {nombre_capa_destino}: {e}")

    except Exception as e:
        print(f"⚠️ No se pudo procesar RegistrosMultimediaTB: {e}")

    df_resumen = pl.DataFrame(resultados_resumen) if resultados_resumen else pl.DataFrame()
    print("📊 MATRIZ DE VALIDACIÓN CRUZADA:\n")
    print(df_resumen)

    return df_resumen, huerfanos_detalle

