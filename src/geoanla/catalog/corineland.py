from enum import Enum

class Dom_CateCober(float, Enum):
    """
    Dominio: Dom_CateCober
    Descripción: Categoría principal de la cobertura (Nivel 1).
    """
    TERRITORIOS_ARTIFICIALIZADOS = 1.0
    TERRITORIOS_AGRICOLAS = 2.0
    BOSQUES_AREAS_SEMINATURALES = 3.0
    AREAS_HUMEDAS = 4.0
    SUPERFICIES_DE_AGUA = 5.0

    @property
    def descripcion(self):
        descripciones = {
            1.0: "Territorios Artificializados",
            2.0: "Territorios Agrícolas",
            3.0: "Bosques y Áreas Seminaturales",
            4.0: "Áreas Húmedas",
            5.0: "Superficies de Agua"
        }
        return descripciones.get(self.value)

class Dom_SubcatCober(float, Enum):
    """
    Dominio: Dom_SubcatCober
    Descripción: Subcategoría o segundo nivel de la cobertura.
    """
    ZONAS_URBANIZADAS = 11.0
    ZONAS_INDUSTRIALES_COMERCIALES = 12.0
    ZONAS_EXTRACCION_MINERA = 13.0
    ZONAS_VERDES_ARTIFICIALIZADAS = 14.0
    CULTIVOS_TRANSITORIOS = 21.0
    CULTIVOS_PERMANENTES = 22.0
    PASTOS = 23.0
    AREAS_AGRICOLAS_HETEROGENEAS = 24.0
    BOSQUES = 31.0
    AREAS_HERBACEA_ARBUSTIVA = 32.0
    AREAS_ABIERTAS_POCA_VEGETACION = 33.0
    AREAS_HUMEDAS_CONTINENTALES = 41.0
    AREAS_HUMEDAS_COSTERAS = 42.0
    AGUAS_CONTINENTALES = 51.0
    AGUAS_MARITIMAS = 52.0

    @property
    def descripcion(self):
        descripciones = {
            11.0: "Zonas urbanizadas",
            12.0: "Zonas industriales o comerciales y redes de comunicación",
            13.0: "Zonas de extracción minera y escombreras",
            14.0: "Zonas verdes artificializadas, no agrícolas",
            21.0: "Cultivos transitorios",
            22.0: "Cultivos permanentes",
            23.0: "Pastos",
            24.0: "Áreas agrícolas heterogéneas",
            31.0: "Bosques",
            32.0: "Áreas con vegetación herbácea y/o arbustiva",
            33.0: "Áreas abiertas, sin o con poca vegetación",
            41.0: "Áreas húmedas continentales",
            42.0: "Áreas húmedas costeras",
            51.0: "Aguas continentales",
            52.0: "Aguas marítimas"
        }
        return descripciones.get(self.value)

class Dom_Clas_Cober(float, Enum):
    """
    Dominio: Dom_Clas_Cober
    Descripción: Clase o tercer nivel de la cobertura (Corine Land Cover).
    """
    TEJIDO_URBANO_CONTINUO = 111.0
    TEJIDO_URBANO_DISCONTINUO = 112.0
    ZONAS_INDUSTRIALES_COMERCIALES = 121.0
    RED_VIAL_FERROVIARIA = 122.0
    ZONAS_PORTUARIAS = 123.0
    AEROPUERTOS = 124.0
    OBRAS_HIDRAULICAS = 125.0
    ZONAS_EXTRACCION_MINERA = 131.0
    ZONAS_DISPOSICION_RESIDUOS = 132.0
    ZONAS_VERDES_URBANAS = 141.0
    INSTALACIONES_RECREATIVAS = 142.0
    OTROS_CULTIVOS_TRANSITORIOS = 211.0
    CEREALES = 212.0
    OLEAGINOSAS_LEGUMINOSAS = 213.0
    HORTALIZAS = 214.0
    TUBERCULOS = 215.0
    CULTIVOS_PERMANENTES_HERBACEOS = 221.0
    CULTIVOS_PERMANENTES_ARBUSTIVOS = 222.0
    CULTIVOS_PERMANENTES_ARBOREOS = 223.0
    CULTIVOS_AGROFORESTALES = 224.0
    CULTIVOS_CONFINADOS = 225.0
    PASTOS_LIMPIOS = 231.0
    PASTOS_ARBOLADOS = 232.0
    PASTOS_ENMALEZADOS = 233.0
    MOSAICO_CULTIVOS = 241.0
    MOSAICO_PASTOS_CULTIVOS = 242.0
    MOSAICO_CULTIVOS_PASTOS_NATURALES = 243.0
    MOSAICO_PASTOS_NATURALES = 244.0
    MOSAICO_CULTIVOS_NATURALES = 245.0
    BOSQUE_DENSO = 311.0
    BOSQUE_ABIERTO = 312.0
    BOSQUE_FRAGMENTADO = 313.0
    BOSQUE_GALERIA_RIPARIO = 314.0
    PLANTACION_FORESTAL = 315.0
    HERBAZAL = 321.0
    ARBUSTAL = 322.0
    VEGETACION_SECUNDARIA_TRANSICION = 323.0
    ZONAS_ARENOSAS_NATURALES = 331.0
    AFLORAMIENTOS_ROCOSOS = 332.0
    TIERRAS_DESNUDAS_DEGRADADAS = 333.0
    ZONAS_QUEMADAS = 334.0
    ZONAS_GLACIARES_NIVALES = 335.0
    ZONAS_PANTANOSAS = 411.0
    TURBERAS = 412.0
    VEGETACION_ACUATICA_CUERPOS_AGUA = 413.0
    PANTANOS_COSTEROS = 421.0
    SALITRAL = 422.0
    SEDIMENTOS_EXPUESTOS_BAJAMAR = 423.0
    RIOS_50M = 511.0
    LAGUNAS_LAGOS_CIENAGAS_NATURALES = 512.0
    CANALES = 513.0
    CUERPOS_AGUA_ARTIFICIALES = 514.0
    LAGUNAS_COSTERAS = 521.0
    MARES_OCEANOS = 522.0
    ESTANQUES_ACUICULTURA_MARINA = 523.0

    @property
    def descripcion(self):
        descripciones = {
            111.0: "Tejido urbano continuo",
            112.0: "Tejido urbano discontinuo",
            121.0: "Zonas industriales o comerciales",
            122.0: "Red vial, ferroviaria y terrenos asociados",
            123.0: "Zonas portuarias",
            124.0: "Aeropuertos",
            125.0: "Obras hidráulicas",
            131.0: "Zonas de extracción minera",
            132.0: "Zonas de disposición de residuos",
            141.0: "Zonas verdes urbanas",
            142.0: "Instalaciones recreativas",
            211.0: "Otros cultivos transitorios",
            212.0: "Cereales",
            213.0: "Oleaginosas y leguminosas",
            214.0: "Hortalizas",
            215.0: "Tubérculos",
            221.0: "Cultivos permanentes herbáceos",
            222.0: "Cultivos permanentes arbustivos",
            223.0: "Cultivos permanentes arbóreos",
            224.0: "Cultivos agroforestales",
            225.0: "Cultivos confinados",
            231.0: "Pastos limpios",
            232.0: "Pastos arbolados",
            233.0: "Pastos enmalezados",
            241.0: "Mosaico de cultivos",
            242.0: "Mosaico de pastos y cultivos",
            243.0: "Mosaico de cultivos, pastos y espacios naturales",
            244.0: "Mosaico de pastos con espacios naturales",
            245.0: "Mosaico de cultivos y espacios naturales",
            311.0: "Bosque denso",
            312.0: "Bosque abierto",
            313.0: "Bosque fragmentado",
            314.0: "Bosque de galería y/o ripario",
            315.0: "Plantación forestal",
            321.0: "Herbazal",
            322.0: "Arbustal",
            323.0: "Vegetación secundaria o en transición",
            331.0: "Zonas arenosas naturales",
            332.0: "Afloramientos rocosos",
            333.0: "Tierras desnudas y degradadas",
            334.0: "Zonas quemadas",
            335.0: "Zonas glaciares y nivales",
            411.0: "Zonas pantanosas",
            412.0: "Turberas",
            413.0: "Vegetación acuática sobre cuerpos de agua",
            421.0: "Pantanos costeros",
            422.0: "Salitral",
            423.0: "Sedimentos expuestos en bajamar",
            511.0: "Ríos (50 m)",
            512.0: "Lagunas, lagos y ciénagas naturales",
            513.0: "Canales",
            514.0: "Cuerpos de agua artificiales",
            521.0: "Lagunas costeras",
            522.0: "Mares y océanos",
            523.0: "Estanques para acuicultura marina"
        }
        return descripciones.get(self.value)

class Dom_Subclas_Cober(float, Enum):
    """
    Dominio: Dom_Subclas_Cober
    Descripción: Subclase o cuarto nivel de la cobertura (Corine Land Cover).
    """
    ZONAS_INDUSTRIALES = 1211.0
    ZONAS_COMERCIALES = 1212.0
    RED_VIAL_TERRITORIOS_ASOCIADOS = 1221.0
    RED_FERROVIARIA_TERRENOS_ASOCIADOS = 1222.0
    ZONAS_PORTUARIAS_FLUVIALES = 1231.0
    ZONAS_PORTUARIAS_MARITIMAS = 1232.0
    AEROPUERTO_INFRAESTRUCTURA_ASOCIADA = 1241.0
    AEROPUERTO_SIN_INFRAESTRUCTURA = 1242.0
    OTRAS_EXPLOTACIONES_MINERAS = 1311.0
    EXPLOTACION_HIDROCARBUROS = 1312.0
    EXPLOTACION_CARBON = 1313.0
    EXPLOTACION_ORO = 1314.0
    EXPLOTACION_MATERIALES_CONSTRUCCION = 1315.0
    EXPLOTACION_SAL = 1316.0
    OTROS_SITIOS_DISPOSICION_RESIDUOS = 1321.0
    ESCOMBRERAS = 1322.0
    VERTEDEROS = 1323.0
    RELLENO_SANITARIO = 1324.0
    OTRAS_ZONAS_VERDES_URBANAS = 1411.0
    PARQUES_CEMENTERIOS = 1412.0
    JARDINES_BOTANICOS = 1413.0
    ZOOLOGICOS = 1414.0
    PARQUES_URBANOS = 1415.0
    RONDAS_CUERPOS_AGUA_URBANOS = 1416.0
    AREAS_CULTURALES = 1421.0
    AREAS_DEPORTIVAS = 1422.0
    AREAS_TURISTICAS = 1423.0
    OTROS_CULTIVOS_PERMANENTES_HERBACEOS = 2211.0
    CANA = 2212.0
    PLATANO_Y_BANANO = 2213.0
    TABACO = 2214.0
    PAPAYA = 2215.0
    AMAPOLA = 2216.0
    OTROS_CULTIVOS_PERMANENTES_ARBUSTIVOS = 2221.0
    CAFE = 2222.0
    CACAO = 2223.0
    VINEDOS = 2224.0
    COCA = 2225.0
    OTROS_CULTIVOS_PERMANENTES_ARBOREOS = 2231.0
    PALMA_DE_ACEITE = 2232.0
    CITRICOS = 2233.0
    MANGO = 2234.0
    PASTOS_Y_ARBOLES_PLANTADOS = 2241.0
    CULTIVOS_Y_ARBOLES_PLANTADOS = 2242.0
    ARROZ = 2121.0
    MAIZ = 2122.0
    SORGO = 2123.0
    CEBADA = 2124.0
    TRIGO = 2125.0
    ALGODON = 2131.0
    AJONJOLI = 2132.0
    FRIJOL = 2133.0
    SOYA = 2134.0
    MANI = 2135.0
    CEBOLLA = 2141.0
    ZANAHORIA = 2142.0
    REMOLACHA = 2143.0
    PAPA = 2151.0
    YUCA = 2152.0
    BOSQUE_DENSO_ALTO = 3111.0
    BOSQUE_DENSO_BAJO = 3112.0
    BOSQUE_ABIERTO_ALTO = 3121.0
    BOSQUE_ABIERTO_BAJO = 3122.0
    BOSQUE_FRAGMENTADO_PASTOS_CULTIVOS = 3131.0
    BOSQUE_FRAGMENTADO_VEGETACION_SECUNDARIA = 3132.0
    PLANTACION_CONIFERAS = 3151.0
    PLANTACION_LATIFOLIADAS = 3152.0
    HERBAZAL_DENSO = 3211.0
    HERBAZAL_ABIERTO = 3212.0
    ARBUSTAL_DENSO = 3221.0
    ARBUSTAL_ABIERTO = 3222.0
    VEGETACION_SECUNDARIA_ALTA = 3231.0
    VEGETACION_SECUNDARIA_BAJA = 3232.0
    PLAYAS = 3311.0
    ARENALES = 3312.0
    CAMPOS_DE_DUNAS = 3313.0
    ZONAS_GLACIARES = 3351.0
    ZONAS_NIVALES = 3352.0
    EMBALSES = 5141.0
    LAGUNAS_OXIDACION = 5142.0
    ESTANQUES_ACUICULTURA_CONTINENTAL = 5143.0
    OTROS_FONDOS = 5221.0
    FONDOS_CORALINOS_SOMEROS = 5222.0
    PRADERAS_PASTOS_MARINOS_SOMERAS = 5223.0
    FONDOS_SOMEROS_ARENAS_CASCAJO = 5224.0

    @property
    def descripcion(self):
        descripciones = {
            1211.0: "Zonas industriales",
            1212.0: "Zonas comerciales",
            1221.0: "Red vial y territorios asociados",
            1222.0: "Red ferroviaria y terrenos asociados",
            1231.0: "Zonas portuarias fluviales",
            1232.0: "Zonas portuarias marítimas",
            1241.0: "Aeropuerto con infraestructura asociada",
            1242.0: "Aeropuerto sin infraestructura asociada",
            1311.0: "Otras explotaciones mineras",
            1312.0: "Explotación de hidrocarburos",
            1313.0: "Explotación de carbón",
            1314.0: "Explotación de oro",
            1315.0: "Explotación de materiales de construcción",
            1316.0: "Explotación de sal",
            1321.0: "Otros sitios de disposición de residuos a cielo abierto",
            1322.0: "Escombreras",
            1323.0: "Vertederos",
            1324.0: "Relleno sanitario",
            1411.0: "Otras zonas verdes urbanas",
            1412.0: "Parques cementerios",
            1413.0: "Jardines botánicos",
            1414.0: "Zoológicos",
            1415.0: "Parques urbanos",
            1416.0: "Rondas de cuerpos de agua de zonas urbanas",
            1421.0: "Áreas culturales",
            1422.0: "Áreas deportivas",
            1423.0: "Áreas turísticas",
            2211.0: "Otros cultivos permanentes herbáceos",
            2212.0: "Caña",
            2213.0: "Plátano y banano",
            2214.0: "Tabaco",
            2215.0: "Papaya",
            2216.0: "Amapola",
            2221.0: "Otros cultivos permanentes arbustivos",
            2222.0: "Café",
            2223.0: "Cacao",
            2224.0: "Viñedos",
            2225.0: "Coca",
            2231.0: "Otros cultivos permanentes arbóreos",
            2232.0: "Palma de aceite",
            2233.0: "Cítricos",
            2234.0: "Mango",
            2241.0: "Pastos y árboles plantados",
            2242.0: "Cultivos y árboles plantados",
            2121.0: "Arroz",
            2122.0: "Maíz",
            2123.0: "Sorgo",
            2124.0: "Cebada",
            2125.0: "Trigo",
            2131.0: "Algodón",
            2132.0: "Ajonjolí",
            2133.0: "Fríjol",
            2134.0: "Soya",
            2135.0: "Maní",
            2141.0: "Cebolla",
            2142.0: "Zanahoria",
            2143.0: "Remolacha",
            2151.0: "Papa",
            2152.0: "Yuca",
            3111.0: "Bosque denso alto",
            3112.0: "Bosque denso bajo",
            3121.0: "Bosque abierto alto",
            3122.0: "Bosque abierto bajo",
            3131.0: "Bosque fragmentado con pastos y cultivos",
            3132.0: "Bosque fragmentado con vegetación secundaria",
            3151.0: "Plantación de coníferas",
            3152.0: "Plantación de latifoliadas",
            3211.0: "Herbazal denso",
            3212.0: "Herbazal abierto",
            3221.0: "Arbustal denso",
            3222.0: "Arbustal abierto",
            3231.0: "Vegetación secundaria alta",
            3232.0: "Vegetación secundaria baja",
            3311.0: "Playas",
            3312.0: "Arenales",
            3313.0: "Campos de dunas",
            3351.0: "Zonas glaciares",
            3352.0: "Zonas nivales",
            5141.0: "Embalses",
            5142.0: "Lagunas de oxidación",
            5143.0: "Estanques para acuicultura continental",
            5221.0: "Otros fondos",
            5222.0: "Fondos coralinos someros",
            5223.0: "Praderas de pastos marinos someras",
            5224.0: "Fondos someros de arenas y cascajo"
        }
        return descripciones.get(self.value)

class Dom_Nivel5_Cober(float, Enum):
    """
    Dominio: Dom_Nivel5_Cober
    Descripción: Cobertura del quinto nivel (Corine Land Cover).
    """
    BOSQUE_DENSO_ALTO_TIERRA_FIRME = 31111.0
    BOSQUE_DENSO_ALTO_INUNDABLE = 31112.0
    BOSQUE_DENSO_BAJO_TIERRA_FIRME = 31121.0
    BOSQUE_DENSO_BAJO_INUNDABLE = 31122.0
    BOSQUE_ABIERTO_ALTO_TIERRA_FIRME = 31211.0
    BOSQUE_ABIERTO_ALTO_INUNDABLE = 31212.0
    BOSQUE_ABIERTO_BAJO_TIERRA_FIRME = 31221.0
    BOSQUE_ABIERTO_BAJO_INUNDABLE = 31222.0
    HERBAZAL_DENSO_TIERRA_FIRME = 32111.0
    HERBAZAL_DENSO_INUNDABLE = 32112.0
    HERBAZAL_ABIERTO_ARENOSO = 32121.0
    HERBAZAL_ABIERTO_ROCOSO = 32122.0
    ARBUSTAL_ABIERTO_ESCLEROFILO = 32221.0
    ARBUSTAL_ABIERTO_MESOFILO = 32222.0

    @property
    def descripcion(self):
        descripciones = {
            31111.0: "Bosque denso alto de tierra firme",
            31112.0: "Bosque denso alto inundable",
            31121.0: "Bosque denso bajo de tierra firme",
            31122.0: "Bosque denso bajo inundable",
            31211.0: "Bosque abierto alto de tierra firme",
            31212.0: "Bosque abierto alto inundable",
            31221.0: "Bosque abierto bajo de tierra firme",
            31222.0: "Bosque abierto bajo inundable",
            32111.0: "Herbazal denso de tierra firme",
            32112.0: "Herbazal denso inundable",
            32121.0: "Herbazal abierto arenoso",
            32122.0: "Herbazal abierto rocoso",
            32221.0: "Arbustal abierto esclerófilo",
            32222.0: "Arbustal abierto mesófilo"
        }
        return descripciones.get(self.value)

class Dom_Nivel6_Cober(float, Enum):
    """
    Dominio: Dom_Nivel6_Cober
    Descripción: Cobertura del sexto nivel (Detalle fisonómico y botánico).
    """
    BOSQUE_DENSO_ALTO_INUNDABLE_HETEROGENEO = 311121.0
    MANGLAR_DENSO_ALTO = 311122.0
    PALMARES = 311123.0
    HERBAZAL_DENSO_TIERRA_FIRME_NO_ARBOLADO = 321111.0
    HERBAZAL_DENSO_TIERRA_FIRME_ARBOLADO = 321112.0
    HERBAZAL_DENSO_TIERRA_FIRME_CON_ARBUSTOS = 321113.0
    HERBAZAL_DENSO_INUNDABLE_NO_ARBOLADO = 321121.0
    HERBAZAL_DENSO_INUNDABLE_ARBOLADO = 321122.0
    ARRACACHAL = 321123.0
    HELECHAL = 321124.0

    @property
    def descripcion(self):
        descripciones = {
            311121.0: "Bosque denso alto inundable heterogéneo",
            311122.0: "Manglar denso alto",
            311123.0: "Palmares",
            321111.0: "Herbazal denso de tierra firme no arbolado",
            321112.0: "Herbazal denso de tierra firme arbolado",
            321113.0: "Herbazal denso de tierra firme con arbustos",
            321121.0: "Herbazal denso inundable no arbolado",
            321122.0: "Herbazal denso inundable arbolado",
            321123.0: "Arracachal",
            321124.0: "Helechal"
        }
        return descripciones.get(self.value)