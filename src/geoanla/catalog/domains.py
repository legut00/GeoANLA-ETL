from enum import Enum

class Dom_FC_Multimedia(float, Enum):
    """
    Dominio: Dom_FC_Multimedia
    Descripción: Capa geográfica asociada al registro multimedia.
    Tipo en GDB: Double 8
    """
    MATERIALES_CONSTRUCCION_PT = 1107.0
    MATERIALES_CONSTRUCCION_PG = 1108.0
    OCUPACION_CAUCE = 1502.0
    CAPTACION_AGUA_SUPER_PT = 1503.0
    CAPTACION_AGUA_SUPER_LN = 1504.0
    VERTIMIENTO_PT = 1505.0
    VERTIMIENTO_LN = 1506.0
    VERTIMIENTO_VIA = 1507.0
    VERTIMIENTO_SUELO = 1508.0
    PUNTO_MUESTREO_AGUA_SUPER = 1509.0
    PUNTO_MUESTREO_FLORA = 2003.0
    PUNTO_MUESTREO_FAUNA = 2004.0
    TRANSECTO_MUESTREO_FAUNA = 2005.0
    APROVECHA_FORESTAL_PT = 2007.0

    @property
    def descripcion(self):
        descripciones = {
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
        return descripciones.get(self.value)

class Dom_Departamento(str, Enum):
    """
    Dominio: Dom_Departamento
    Descripción: División político-administrativa (Nivel Departamento).
    Tipo en GDB: Text (Length 2) - Conserva ceros a la izquierda.
    """
    AMAZONAS = "91"
    ANTIOQUIA = "05"
    ARAUCA = "81"
    SAN_ANDRES = "88"
    ATLANTICO = "08"
    BOGOTA = "11"
    BOLIVAR = "13"
    BOYACA = "15"
    CALDAS = "17"
    CAQUETA = "18"
    CASANARE = "85"
    CAUCA = "19"
    CESAR = "20"
    CHOCO = "27"
    CORDOBA = "23"
    CUNDINAMARCA = "25"
    GUAINIA = "94"
    GUAVIARE = "95"
    HUILA = "41"
    LA_GUAJIRA = "44"
    MAGDALENA = "47"
    META = "50"
    NARINO = "52"
    NORTE_SANTANDER = "54"
    PUTUMAYO = "86"
    QUINDIO = "63"
    RISARALDA = "66"
    SANTANDER = "68"
    SUCRE = "70"
    TOLIMA = "73"
    VALLE_DEL_CAUCA = "76"
    VAUPES = "97"
    VICHADA = "99"

    @property
    def descripcion(self):
        descripciones = {
            "91": "Amazonas",
            "05": "Antioquia",
            "81": "Arauca",
            "88": "Archipiélago de San Andrés, Providencia y Santa Catalina",
            "08": "Atlántico",
            "11": "Bogotá, D.C.",
            "13": "Bolívar",
            "15": "Boyacá",
            "17": "Caldas",
            "18": "Caquetá",
            "85": "Casanare",
            "19": "Cauca",
            "20": "Cesar",
            "27": "Chocó",
            "23": "Córdoba",
            "25": "Cundinamarca",
            "94": "Guainía",
            "95": "Guaviare",
            "41": "Huila",
            "44": "La Guajira",
            "47": "Magdalena",
            "50": "Meta",
            "52": "Nariño",
            "54": "Norte de Santander",
            "86": "Putumayo",
            "63": "Quindio",
            "66": "Risaralda",
            "68": "Santander",
            "70": "Sucre",
            "73": "Tolima",
            "76": "Valle del Cauca",
            "97": "Vaupés",
            "99": "Vichada"
        }
        return descripciones.get(self.value)

class Dom_Tenencia(float, Enum):
    """
    Dominio: Dom_Tenencia
    Descripción: Forma de tenencia de la propiedad.
    Tipo en GDB: Double 8 (Decimal)
    """
    PROPIEDAD_PRIVADA = 1.0
    PROPIEDAD_COLECTIVA = 2.0
    POSESION_SIN_TITULO = 3.0
    OCUPANTE = 4.0
    ARRENDATARIO = 5.0
    MEJORATARIO = 6.0
    USUFRUCTO_O_APARCERO = 7.0

    @property
    def descripcion(self):
        descripciones = {
            1.0: "Propiedad privada",
            2.0: "Propiedad colectiva",
            3.0: "Posesión sin título (baldíos o ejidos)",
            4.0: "Ocupante (bienes de uso público)",
            5.0: "Arrendatario",
            6.0: "Mejoratario",
            7.0: "Usufructo o aparcero"
        }
        return descripciones.get(self.value)

class Dom_TipoMuestreoFlo(float, Enum):
    """
    Dominio: Dom_TipoMuestreoFlo
    Descripción: Indica el tipo de diseño de muestreo utilizado en campo.
    """
    PUNTUAL = 311.0
    PARCELA = 312.0
    TRANSECTO = 313.0

    @property
    def descripcion(self):
        descripciones = {
            311.0: "Puntual",
            312.0: "Parcela",
            313.0: "Transecto"
        }
        return descripciones.get(self.value)

class Dom_Temporada(float, Enum):
    """
    Dominio: Dom_Temporada
    Descripción: Corresponde a la temporada climática en la que se realizó el muestreo.
    """
    SECO = 301.0
    HUMEDO = 302.0
    MEDIO = 303.0
    TODO_EL_ANNIO = 304.0

    @property
    def descripcion(self):
        descripciones = {
            301.0: "Seco",
            302.0: "Húmedo",
            303.0: "Medio",
            304.0: "Todo el año"
        }
        return descripciones.get(self.value)

class Dom_Apendice(float, Enum):
    """
    Dominio: Dom_Apendice
    Descripción: Apéndice en el que se encuentra la especie según la Convención sobre el Comercio Internacional de Especies Amenazadas de Fauna
    y Flora Silvestres (CITES).
    """
    APENDICE_I = 100.0
    APENDICE_II = 200.0
    APENDICE_III = 300.0
    NO_APLICA = 400.0

    @property
    def descripcion(self):
        descripciones = {
            100.0: "Apendice I",
            200.0: "Apendice II",
            300.0: "Apendice III",
            400.0: "No aplica"
        }
        return descripciones.get(self.value)

class Dom_Amenaza(float, Enum):
    """
    Dominio: Dom_Amenaza
    Descripción: Categoría de amenaza en la que se encuentra la especie según la UICN o el Ministerio de Ambiente.
    """
    PREOCUPACION_MENOR = 321.0
    CASI_AMENAZADA = 322.0
    VULNERABLE = 323.0
    EN_PELIGRO = 324.0
    PELIGRO_CRITICO = 325.0
    EXTINTO_EN_ESTADO_SILVESTRE = 326.0
    EXTINTO = 327.0
    DATOS_INSUFICIENTES = 328.0
    NO_EVALUADO = 329.0
    NO_APLICA = 330.0

    @property
    def descripcion(self):
        descripciones = {
            321.0: "Preocupación Menor (LC)",
            322.0: "Casi Amenazada (NT)",
            323.0: "Vulnerable (VU)",
            324.0: "Peligro (EN)",
            325.0: "Peligro Crítico (CR)",
            326.0: "Extinto en estado silvestre (EW)",
            327.0: "Extinto (EX)",
            328.0: "Datos insuficientes (DD)",
            329.0: "No Evaluado (NE)",
            330.0: "No aplica"
        }
        return descripciones.get(self.value)

class Dom_Tipo_Distribu(float, Enum):
    """
    Dominio: Dom_Tipo_Distribu
    Descripción: Categoría de distribución geográfica de la especie.
    """
    COSMOPOLITA = 331.0
    RESTRINGIDA = 332.0
    CASI_ENDEMICA = 333.0
    ENDEMICA = 334.0

    @property
    def descripcion(self):
        descripciones = {
            331.0: "Cosmopolita",
            332.0: "Restringida",
            333.0: "Casi endémica",
            334.0: "Endémica"
        }
        return descripciones.get(self.value)

class Dom_EntidadVeda(float, Enum):
    """
    Dominio: Dom_EntidadVeda
    Descripción: Entidad administrativa o ambiental que establece la veda.
    Campo GDB: ENTID_VEDA (Double 8)
    """
    # Ministerios e Institutos Nacionales
    INDERENA = 2040.0
    INCODER = 2041.0
    MADS = 2042.0  # Ministerio de Ambiente y Desarrollo Sostenible
    INCORA = 2043.0
    INPA = 2044.0
    MADR = 2045.0  # Ministerio de Agricultura y Desarrollo Rural
    MAVDT = 2039.0 # Min Ambiente Vivienda y Des. Terr.

    # Corporaciones Autónomas y de Desarrollo
    AMVA = 2081.0
    CAM = 2047.0
    CAR = 2048.0
    CARDER = 2049.0
    CARDIQUE = 2050.0
    CARSUCRE = 2051.0
    CAS = 2052.0
    CDMB = 2053.0
    CORANTIOQUIA = 2054.0
    CORNARE = 2055.0
    CORPAMAG = 2056.0
    CORPOBOYACA = 2057.0
    CORPOCALDAS = 2058.0
    CORPOCESAR = 2059.0
    CORPOCHIVOR = 2060.0
    CORPOGUAJIRA = 2061.0
    CORPOGUAVIO = 2062.0
    CORPONARINO = 2063.0
    CORPONOR = 2064.0
    CORPORINOQUIA = 2065.0
    CORTOLIMA = 2066.0
    CRA = 2067.0
    CRC = 2068.0
    CRQ = 2069.0
    CSB = 2070.0
    CVC = 2071.0
    CVS = 2072.0
    CDA = 2073.0
    CODECHOCO = 2074.0
    CORALINA = 2075.0
    CORMACARENA = 2076.0
    CORPOAMAZONIA = 2077.0
    CORPOMOJANA = 2078.0
    CORPOURABA = 2079.0

    # Autoridades Ambientales Urbanas
    SDA = 2080.0   # Bogotá
    DAGMA = 2082.0 # Cali
    DAMAB = 2083.0 # Barranquilla
    DADMA = 2084.0 # Santa Marta
    EPA = 2085.0   # Cartagena

    # Otros
    OTRA = 2046.0

    @property
    def descripcion(self):
        descripciones = {
            2081.0: "AMVA - Área Metropolitana del Valle de Aburrá – Medellín",
            2047.0: "CAM - Corporación Autónoma Regional del Alto Magdalena",
            2048.0: "CAR - Corporación Autónoma Regional de Cundinamarca",
            2049.0: "CARDER - Corporación Autónoma Regional de Risaralda",
            2050.0: "CARDIQUE - Corporación Autónoma Regional del Canal Del Dique",
            2051.0: "CARSUCRE - Corporación Autónoma Regional de Sucre",
            2052.0: "CAS - Corporación Autónoma Regional de Santander",
            2073.0: "CDA - Corporación para el Desarrollo Sostenible del Norte y el Oriente Amazónico",
            2053.0: "CDMB - Corporación Autónoma Regional para la Defensa de la Meseta de Bucaramanga",
            2074.0: "CODECHOCO - Corporación Autónoma Regional para el Desarrollo Sostenible del Chocó",
            2075.0: "CORALINA - Corporación para el Desarrollo Sostenible del Archipiélago de San Andrés, Providencia y Santa Catalina",
            2054.0: "CORANTIOQUIA - Corporación Autónoma Regional del Centro de Antioquia",
            2076.0: "CORMACARENA - Corporación para el Desarrollo Sostenible del Área de Manejo Especial de La Macarena",
            2055.0: "CORNARE - Corporación Autónoma Regional de las Cuencas de los Ríos Negro y Nare",
            2056.0: "CORPAMAG - Corporación Autónoma Regional del Magdalena",
            2077.0: "CORPOAMAZONIA - Corporación para el Desarrollo Sostenible del Sur de la Amazonia",
            2057.0: "CORPOBOYACA - Corporación Autónoma Regional de Boyacá",
            2058.0: "CORPOCALDAS - Corporación Autónoma Regional de Caldas",
            2059.0: "CORPOCESAR - Corporación Autónoma Regional del Cesar",
            2060.0: "CORPOCHIVOR - Corporación Autónoma Regional de Chivor",
            2061.0: "CORPOGUAJIRA - Corporación Autónoma Regional de La Guajira",
            2062.0: "CORPOGUAVIO - Corporación Autónoma Regional del Guavio",
            2078.0: "CORPOMOJANA - Corporación para el Desarrollo Sostenible de La Mojana y El San Jorge",
            2063.0: "CORPONARIÑO - Corporación Autónoma Regional de Nariño",
            2064.0: "CORPONOR - Corporación Autónoma Regional de la Frontera Nororiental",
            2065.0: "CORPORINOQUIA - Corporación Autónoma Regional de la Orinoquia",
            2079.0: "CORPOURABA - Corporación para el Desarrollo Sostenible del Urabá",
            2066.0: "CORTOLIMA - Corporación Autónoma Regional del Tolima",
            2067.0: "CRA - Corporación Autónoma Regional del Atlántico",
            2068.0: "CRC - Corporación Autónoma Regional del Cauca",
            2069.0: "CRQ - Corporación Autónoma Regional del Quindío",
            2070.0: "CSB - Corporación Autónoma Regional del Sur de Bolívar",
            2071.0: "CVC - Corporación Autónoma Regional del Valle del Cauca",
            2072.0: "CVS - Corporación Autónoma Regional de los Valles del Sinú y del San Jorge",
            2084.0: "DADMA - Departamento Administrativo Distrital del Medio Ambiente de Santa Marta",
            2082.0: "DAGMA - Departamento Administrativo de Gestión del Medio Ambiente – Cali",
            2083.0: "DAMAB - Departamento Técnico Administrativo del Medio Ambiente de Barranquilla",
            2085.0: "EPA - Establecimiento Público Ambiental – Cartagena",
            2041.0: "INCODER - Instituto Colombiano de Desarrollo Rural",
            2043.0: "INCORA - Instituto Colombiano de la Reforma Agraria",
            2040.0: "INDERENA - Instituto Nacional de Recursos Naturales Renovables y del Ambiente",
            2044.0: "INPA - Instituto Nacional de Pesca y Acuicultura",
            2045.0: "MADR - MInisterio de Agricultura y Desarrollo Rural",
            2042.0: "MADS - Ministerio de Ambiente y Desarrollo Sostenible",
            2039.0: "MAVDT - Ministerio de Ambiente, Vivienda y Desarrollo Territorial",
            2046.0: "Otra",
            2080.0: "SDA - Secretaría Distrital de Ambiente – Bogotá"
        }
        return descripciones.get(self.value)

class Dom_Vigencia(float, Enum):
    """
    Dominio: Dom_Vigencia
    Descripción: Determina si la veda establecida tiene un plazo definido o es permanente.
    """
    TEMPORAL = 2030.0
    INDEFINIDA = 2031.0

    @property
    def descripcion(self):
        descripciones = {
            2030.0: "Temporal",
            2031.0: "Indefinida"
        }
        return descripciones.get(self.value)

class Dom_Uso_Flora(float, Enum):
    """
    Dominio: Dom_Uso_Flora
    Descripción: Categoría de uso reportado para la especie de flora.
    """
    ACTIVIDADES_PRODUCTIVAS = 351.0
    ASEO = 353.0
    USO_CULTURAL = 355.0
    CULTIVO = 356.0
    SUBSISTENCIA = 359.0
    HABITACION = 361.0
    OTRO = 362.0

    @property
    def descripcion(self):
        descripciones = {
            351.0: "Actividades Productivas",
            353.0: "Aseo",
            355.0: "Uso Cultural",
            356.0: "Cultivo",
            359.0: "Subsistencia",
            361.0: "Habitación",
            362.0: "Otro"
        }
        return descripciones.get(self.value)


class Dom_Habito(float, Enum):
    """
    Dominio: Dom_Habito
    Descripción: Hábito de crecimiento de la especie.
    """
    ARBOL = 371.0
    ARBUSTO = 372.0
    HIERBA = 373.0
    SUFRUTICE = 374.0
    ENREDADERA = 375.0
    LIANA = 376.0
    EPIFITA = 377.0
    HEMIPARASITA = 378.0
    SUCULENTAS = 379.0
    OTRO = 380.0

    @property
    def descripcion(self):
        descripciones = {
            371.0: "Arbol",
            372.0: "Arbusto",
            373.0: "Hierba",
            374.0: "Sufrútice",
            375.0: "Enredadera",
            376.0: "Liana",
            377.0: "Epífita",
            378.0: "Hemiparásita",
            379.0: "Suculentas",
            380.0: "Otro"
        }
        return descripciones.get(self.value)

class Dom_Veda(float, Enum):
    """
    Dominio: Dom_Veda
    Descripción: Si la especie se encuentra en veda, indica el nivel administrativo correspondiente.
    """
    NACIONAL = 341.0
    REGIONAL = 342.0

    @property
    def descripcion(self):
        descripciones = {
            341.0: "Nacional",
            342.0: "Regional"
        }
        return descripciones.get(self.value)

class Dom_TipoTransecto(int, Enum):
    """
    Dominio: Dom_TipoTransecto
    Descripción: Tipo de ancho del transecto utilizado para el levantamiento de información.
    """
    ANCHO_FIJO = 501
    ANCHO_VARIABLE = 502
    OTRO = 503

    @property
    def descripcion(self):
        descripciones = {
            501: "Ancho fijo",
            502: "Ancho variable",
            503: "Otro"
        }
        return descripciones.get(self.value)

# --- DOMINIOS DE ECOLOGÍA ---

class Dom_Tipo_Migra(int, Enum):
    """Dominio para Tipo de Migración (TIPO_MIGR)"""
    INTRAGENERACIONAL = 101
    INTERGENERACIONAL = 102
    CICLICA = 103
    UNIDIRECCIONAL = 104
    ESTACIONAL = 105
    IRRUPCION_POBLACIONAL = 106
    NOMADISMO = 107
    LATITUDINAL = 108
    LONGITUDINAL = 109
    ALTITUDINAL = 110

    @property
    def descripcion(self):
        descripciones = {
            101: "Intrageneracional",
            102: "Intergeneracional",
            103: "Cíclica",
            104: "Unidireccional",
            105: "Estacional",
            106: "Irrupción Poblacional",
            107: "Nomadismo",
            108: "Latitudinal",
            109: "Longitudinal",
            110: "Altitudinal"
        }
        return descripciones.get(self.value)

class Dom_Uso_Fauna(int, Enum):
    """Dominio para Uso de la Especie (USO)"""
    ACTIVIDADES_PRODUCTIVAS = 301
    MASCOTAS = 302
    USO_CULTURAL = 303
    SUBSISTENCIA = 304
    OTRO = 305

    @property
    def descripcion(self):
        descripciones = {
            301: "Actividades Productivas",
            302: "Mascotas",
            303: "Uso Cultural",
            304: "Subsistencia",
            305: "Otro"
        }
        return descripciones.get(self.value)

class Dom_Dieta(int, Enum):
    """
    Dominio: Dom_Dieta
    Fuente: Documento Oficial ANLA
    """
    FRUGIVORO = 401     # Frugívoro
    HERBIVORO = 402     # Herbívoro
    INSECTIVORO = 403   # Insectivoro (Sin tilde en norma)
    OMNIVORO = 404      # Omnivoro (Sin tilde en norma)
    CARNIVORO = 405     # Carnivoro (Sin tilde en norma)
    OTRO = 406

    @property
    def descripcion(self):
        descripciones = {
            401: "Frugívoro",  # Con tilde
            402: "Herbívoro",  # Con tilde
            403: "Insectivoro",
            404: "Omnivoro",
            405: "Carnivoro",
            406: "Otro"
        }
        return descripciones.get(self.value)

class Dom_Sector(float, Enum):
    """
    Dominio: Dom_Sector
    Descripción: Identifica el sector económico al que corresponde el proyecto licenciado.
    """
    ENERGIA = 1.0
    INFRAESTRUCTURA = 2.0
    MINERIA = 3.0
    HIDROCARBUROS = 4.0
    AGROQUIMICOS = 5.0
    OTRO = 6.0

    @property
    def descripcion(self):
        descripciones = {
            1.0: "Energía",
            2.0: "Infraestructura",
            3.0: "Minería",
            4.0: "Hidrocarburos",
            5.0: "Agroquímicos",
            6.0: "Otro"
        }
        return descripciones.get(self.value)


class Dom_TipoTransecto(int, Enum):
    """
    Dominio: Dom_TipoTransecto
    Descripción: Define la metodología de ancho del transecto utilizado.
    """
    ANCHO_FIJO = 501
    ANCHO_VARIABLE = 502
    OTRO = 503

    @property
    def descripcion(self):
        """Devuelve la descripción textual del código."""
        descripciones = {
            501: "Ancho fijo",
            502: "Ancho variable",
            503: "Otro"
        }
        return descripciones.get(self.value, "Desconocido")

class Dom_Boolean(float, Enum):
    """
    Dominio: Dom_Boolean
    Descripción: Indica la afirmación (1) o negación (2) ante una condición específica.
    """
    SI = 1.0
    NO = 2.0

    @property
    def descripcion(self):
        descripciones = {
            1.0: "Sí",
            2.0: "No"
        }
        return descripciones.get(self.value)



class Dom_TipoMuestreoFau(float, Enum):
    """
    Dominio: Dom_TipoMuestreoFau
    Descripción: Tipo de metodología de muestreo utilizada para el levantamiento de fauna (Puntual o Parcela).
    """
    PUNTUAL = 411.0
    PARCELA = 412.0

    @property
    def descripcion(self):
        descripciones = {
            411.0: "Puntual",
            412.0: "Parcela"
        }
        return descripciones.get(self.value)

class Dom_Deter(float, Enum):
    """
    Dominio: Dom_Deter
    Descripción: Forma o evidencia técnica mediante la cual fue determinada la presencia de la especie.
    """
    CAPTURA = 411.0
    OBSERVACION = 413.0
    MARCAS = 414.0
    DETECCION_AUDITIVA = 415.0
    HUELLAS = 416.0
    HECES = 417.0
    PELOS = 418.0
    OTRO = 419.0

    @property
    def descripcion(self):
        descripciones = {
            411.0: "Captura de individuos",
            413.0: "Observación",
            414.0: "Marcas de Individuos",
            415.0: "Detección auditiva",
            416.0: "Huellas",
            417.0: "Heces",
            418.0: "Pelos",
            419.0: "Otro"
        }
        return descripciones.get(self.value)

class Dom_Regeneracion(int, Enum):
    """
    Dominio: Dom_Regeneracion
    Descripción: Categoría de tamaño para la regeneración natural.
    Tipo en GDB: SmallInteger 2 (Entero puro).
    """
    RENUEVO_O_PLANTULA = 1
    BRINZAL = 2
    LATIZAL = 3

    @property
    def descripcion(self):
        descripciones = {
            1: "Renuevo o plántula",
            2: "Brinzal",
            3: "Latizal"
        }
        return descripciones.get(self.value)

class Dom_CAR(float, Enum):
    """
    Dominio: Dom_CAR
    Descripción: Autoridades ambientales (Corporaciones Autónomas Regionales y otras).
    Tipo en GDB: Double 8
    """
    AMVA = 1001.0
    CAM = 1002.0
    CAR = 1003.0
    CARDER = 1004.0
    CARDIQUE = 1005.0
    CARSUCRE = 1006.0
    CAS = 1007.0
    CDA = 1008.0
    CDMB = 1009.0
    CODECHOCO = 1010.0
    CORALINA = 1011.0
    CORANTIOQUIA = 1012.0
    CORMACARENA = 1013.0
    CORNARE = 1014.0
    CORPAMAG = 1015.0
    CORPOAMAZONIA = 1016.0
    CORPOBOYACA = 1017.0
    CORPOCALDAS = 1018.0
    CORPOCESAR = 1019.0
    CORPOCHIVOR = 1020.0
    CORPOGUAJIRA = 1021.0
    CORPOGUAVIO = 1022.0
    CORPOMOJANA = 1023.0
    CORPONARINO = 1024.0
    CORPONOR = 1025.0
    CORPORINOQUIA = 1026.0
    CORPOURABA = 1027.0
    CORTOLIMA = 1028.0
    CRA = 1029.0
    CRC = 1030.0
    CRQ = 1031.0
    CSB = 1032.0
    CVC = 1033.0
    CVS = 1034.0
    DADMA = 1035.0
    DAGMA = 1036.0
    DAMAB = 1037.0
    EPA = 1038.0
    SDA = 1039.0
    MADS = 1040.0
    SPNN = 1041.0

    @property
    def descripcion(self):
        descripciones = {
            1001.0: "AMVA",
            1002.0: "CAM",
            1003.0: "CAR",
            1004.0: "CARDER",
            1005.0: "CARDIQUE",
            1006.0: "CARSUCRE",
            1007.0: "CAS",
            1008.0: "CDA",
            1009.0: "CDMB",
            1010.0: "CODECHOCO",
            1011.0: "CORALINA",
            1012.0: "CORANTIOQUIA",
            1013.0: "CORMACARENA",
            1014.0: "CORNARE",
            1015.0: "CORPAMAG",
            1016.0: "CORPOAMAZONIA",
            1017.0: "CORPOBOYACA",
            1018.0: "CORPOCALDAS",
            1019.0: "CORPOCESAR",
            1020.0: "CORPOCHIVOR",
            1021.0: "CORPOGUAJIRA",
            1022.0: "CORPOGUAVIO",
            1023.0: "CORPOMOJANA",
            1024.0: "CORPONARIÑO",
            1025.0: "CORPONOR",
            1026.0: "CORPORINOQUIA",
            1027.0: "CORPOURABA",
            1028.0: "CORTOLIMA",
            1029.0: "CRA",
            1030.0: "CRC",
            1031.0: "CRQ",
            1032.0: "CSB",
            1033.0: "CVC",
            1034.0: "CVS",
            1035.0: "DADMA",
            1036.0: "DAGMA",
            1037.0: "DAMAB",
            1038.0: "EPA",
            1039.0: "SDA",
            1040.0: "MADS",
            1041.0: "SPNN"
        }
        return descripciones.get(self.value)

class Dom_Tipo_Actadmin(float, Enum):
    """
    Dominio: Dom_Tipo_Actadmin
    Descripción: Tipo de acto administrativo (Auto o Resolución).
    Tipo en GDB: Double 8
    """
    AUTO = 1.0
    RESOLUCION = 2.0

    @property
    def descripcion(self):
        descripciones = {
            1.0: "Auto",
            2.0: "Resolución"
        }
        return descripciones.get(self.value)

class Dom_SubAct_Comp(float, Enum):
    """
    Dominio: Dom_SubAct_Comp
    Descripción: Subactividades asociadas a las medidas de compensación.
    Tipo en GDB: Double 8
    """
    APOYO_AREAS_PUBLICAS = 1201.0
    CREAR_AREAS_PRIVADAS = 1202.0
    ACUERDOS_CONSERVACION = 1203.0
    RESTAURACION_ECOLOGICA = 1204.0
    REHABILITACION = 1205.0
    RECUPERACION = 1206.0
    REFORESTACION_PROTECTORA = 1207.0
    HERRAMIENTAS_MANEJO_PAISAJE = 1208.0
    SANEAMIENTO_PREDIAL = 1209.0
    AMPLIACION_RESTAURACION = 1210.0
    OTRA = 1211.0

    @property
    def descripcion(self):
        descripciones = {
            1201.0: "Apoyo creación nuevas áreas protegidas publicas y su plan de manejo ambiental",
            1202.0: "Crear nuevas áreas protegidas privadas y su plan de manejo ambiental",
            1203.0: "Establecer acuerdos de conservación, servidumbre ecológicas, Incentivos para mantenimiento y conservación de las áreas",
            1204.0: "Restauración ecológica",
            1205.0: "Rehabilitación",
            1206.0: "Recuperación",
            1207.0: "Reforestación protectora",
            1208.0: "Herramienta de manejo de paisaje, proyectos silvopastoriles, agroforestales, silviculturales, etc) en áreas agrícolas y ganaderas",
            1209.0: "Saneamientos predial/restauración ecológica",
            1210.0: "Ampliación y restauración ecológica",
            1211.0: "Otra"
        }
        return descripciones.get(self.value)


class Dom_Otras_Comp(float, Enum):
    """
    Dominio: Dom_Otras_Comp
    Descripción: Otras medidas de compensación u obligaciones.
    Tipo en GDB: Double 8
    """
    APROVECHAMIENTO_FORESTAL = 20101.0
    CONCESION_AGUAS = 20102.0
    CONTINGENCIAS = 20103.0
    EMISIONES_ATMOSFERICAS = 20104.0
    LEVANTAMIENTO_VEDAS = 20105.0
    MULTAS_SANCIONES = 20106.0
    OCUPACION_CAUCE = 20107.0
    PAISAJE = 20108.0
    TALA_PODA = 20110.0
    VERTIMIENTO = 20111.0
    RESIDUOS_SOLIDOS = 20112.0
    SUSTRACCION_RESERVAS = 20113.0
    CAMBIO_COBERTURA_USO = 20114.0
    OTRA = 20115.0

    @property
    def descripcion(self):
        descripciones = {
            20101.0: "Aprovechamiento forestal",
            20102.0: "Concesión de aguas",
            20103.0: "Contingencias",
            20104.0: "Emisiones atmosféricas",
            20105.0: "Levantamiento de vedas",
            20106.0: "Multas o sanciones",
            20107.0: "Ocupación de cauce",
            20108.0: "Paisaje",
            20110.0: "Permiso de tala y poda",
            20111.0: "Permiso de vertimiento",
            20112.0: "Residuos sólidos",
            20113.0: "Sustracción de áreas en las reservas forestales (la Ley 2ª de 1959)",
            20114.0: "Cambio de cobertura y uso del suelo",
            20115.0: "Otra"
        }
        return descripciones.get(self.value)

class Dom_EstInver(float, Enum):
    """
    Dominio: Dom_EstInver
    Descripción: Estado de la inversión (usualmente para la Inversión del 1%).
    Tipo en GDB: Double 8
    """
    EVALUACION = 35001.0
    APROBADO_POR_EJECUTAR = 35002.0
    APROBADO_EN_EJECUCION = 35003.0
    EJECUTADO = 35004.0
    NO_SE_EJECUTO = 35005.0
    NO_VIABLE = 35006.0
    MODIFICADO = 35007.0

    @property
    def descripcion(self):
        descripciones = {
            35001.0: "Evaluación",
            35002.0: "Aprobado por ejecutar",
            35003.0: "Aprobado en ejecución",
            35004.0: "Ejecutado",
            35005.0: "No se ejecutó",
            35006.0: "No viable",
            35007.0: "Modificado"
        }
        return descripciones.get(self.value)