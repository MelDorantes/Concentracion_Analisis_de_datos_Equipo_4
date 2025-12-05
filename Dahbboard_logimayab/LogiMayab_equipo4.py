# pip install streamlit pandas matplotlib pydeck
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import altair as alt

import unicodedata

def normalizar_texto(s: str) -> str:
    """Convierte a mayúsculas, quita acentos y espacios extra."""
    if pd.isna(s):
        return ""
    s = str(s).strip()
    # Quitar acentos
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    # Mayúsculas
    return s.upper()


if "dfs_cargados" not in st.session_state:
    st.session_state["dfs_cargados"] = []

if "nombres_archivos" not in st.session_state:
    st.session_state["nombres_archivos"] = []

if "df_archivo_1" not in st.session_state:
    st.session_state["df_archivo_1"] = None
    st.session_state["nombre_archivo_1"] = ""

if "df_archivo_2" not in st.session_state:
    st.session_state["df_archivo_2"] = None
    st.session_state["nombre_archivo_2"] = ""

if "df_plantilla" not in st.session_state:
    st.session_state["df_plantilla"] = None


# Configuración general
st.set_page_config(page_title="Demo App", layout="wide")
# python3 -m streamlit run borrador_d.py


# Estilos CSS personalizados
st.markdown(
    """
    <style>
        :root {
            --naranja: #EC6C24;
            --gris-oscuro: #848C8C;
            --gris-claro: #E8E7E7;
            --arena: #E4B396;
            --gris-medio: #B1B4B6;
            --durazno: #FCD4BE;
            --gris-uploader: #D3D4D5; 
        }
        body, .stApp { background-color: var(--gris-claro) !important; }
        [data-testid="stSidebar"] { background-color: var(--durazno) !important; color: #333 !important; }
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3 { color: #333 !important; }
        h1, h2, h3, h4, h5, h6, p, label, span { color: #333 !important; }
        .stButton>button {
            background-color: var(--naranja) !important;
            color: white !important;
            border-radius: 8px;
            border: none;
            padding: 0.6rem 1.2rem;
        }
        .stButton>button:hover { background-color: #d85f20 !important; }
        .stRadio div, .stSelectbox div { color: #333 !important; }
        .stTextInput>div>div>input, 
        .stSelectbox div[role="button"] {
            border-radius: 6px !important;
            border: 1px solid var(--gris-medio) !important;
        }
        [data-testid="stDataFrame"] {
            background-color: white !important;
            border-radius: 10px !important;
            color: #333 !important;
        }
        [data-testid="stDataFrame"] table {
            background-color: white !important;
            color: #333 !important;
            border-radius: 10px !important;
        }
        [data-testid="stDataFrame"] thead tr th {
            background-color: var(--gris-uploader) !important;
            color: #333 !important;
        }
        [data-testid="stDataFrame"] tbody tr td { background-color: white !important; color: #333 !important; }
        [data-testid="stDataFrame"] tbody tr:nth-child(even) td { background-color: #F5F5F5 !important; }
        hr { border: 1px solid var(--arena) !important; }
        [data-testid="stFileUploader"] section {
            background-color: var(--gris-uploader) !important;
            border-radius: 12px !important;
            padding: 12px !important;
        }
        [data-testid="stFileUploader"] div { background-color: var(--gris-uploader) !important; }
        [data-testid="stFileUploader"] * { color: #333 !important; }
        [data-testid="stFileUploader"] button {
            background-color: var(--naranja) !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
        }
        [data-testid="stFileUploader"] button:hover { background-color: #d85f20 !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# header con logos
LOGO_URL = "https://bepensa.com/wp-content/uploads/2021/08/IMG_8536-1-1.png"
LOGO2_URL = "https://javier.rodriguez.org.mx/itesm/2014/tecnologico-de-monterrey-blue-med.png"
header = st.container()
with header:
    col_logo_left, col_space, col_logo_right = st.columns([1, 5, 1])
    with col_logo_left:
        st.image(LOGO_URL, width=140)
    with col_space:
        st.write("")
    with col_logo_right:
        st.image(LOGO2_URL, width=140)

st.markdown("---")

# navbar
st.sidebar.title("Menú de Navegación")
page = st.sidebar.radio("Selecciona una opción:", ["Inicio", 
                                                   "Análisis de Datos", 
                                                   "Visualización Interactiva",
                                                   "Visualización Bitácoras"])

# página: inicio
if page == "Inicio":
    st.title("Bienvenido a la Aplicación de BEPENSA/LogiMayab")
    st.markdown(
        "Esta aplicación fue desarrollada para apoyar al equipo de BEPENSA en la exploración, análisis y "
        "visualización de datos de manera sencilla, rápida e intuitiva. Su objetivo principal es facilitar la "
        "generación de insights estratégicos a partir de archivos cargados por el usuario, permitiendo transformar "
        "la información en decisiones informadas."
    )
    st.markdown("---")
    st.subheader("Objetivos principales:")
    st.markdown("""
        <div style='color: #000;'> 
                
        - Centraliza la visualización y análisis preliminar de datos. 
                 
        - Reduce el tiempo necesario para comprender la información disponible. 
                 
        - Facilita la identificación de outliers, anomalías y oportunidades de mejora.
                  
        - Proporciona gráficos dinámicos que apoyan la comunicación de resultados.
        </div>
    """, unsafe_allow_html=True)

elif page == "Análisis de Datos":
    st.title("Carga tus datos para comenzar el Análisis")
    st.markdown(
        "Por favor, carga **dos archivos** en formato CSV o Excel que contengan los datos que deseas analizar. "
        "Cada archivo se carga por separado en su propio botón."
    )
    st.markdown("Nota: Se recommienda que los archivos de fallas y viajes esten en csv.")

    st.subheader("Archivo Viajes")
    archivo_1 = st.file_uploader(
        "Carga el Archivo 1 (CSV o Excel)",
        type=["csv", "xlsx"],
        key="archivo_1"
    )

    # Si se carga un archivo nuevo en este run, lo guardamos en memoria
    if archivo_1 is not None:
        try:
            if archivo_1.name.endswith(".csv"):
                df1 = pd.read_csv(archivo_1)
            else:
                df1 = pd.read_excel(archivo_1, header=1)

            st.session_state["df_archivo_1"] = df1
            st.session_state["nombre_archivo_1"] = archivo_1.name
            st.success(f"Archivo 1 cargado correctamente: {archivo_1.name}")
        except Exception as e:
            st.error(f"Ocurrió un error al procesar el Archivo 1 ({archivo_1.name}): {e}")

    # Mensaje de estado (aunque hayas cambiado de pestaña)
    if st.session_state["df_archivo_1"] is not None:
        st.info(f"Archivo 1 sigue cargado en memoria: **{st.session_state['nombre_archivo_1']}**")
    else:
        st.warning("Archivo 1 aún no ha sido cargado.")

    st.write("---")

    st.subheader("Archivo Fallas")
    archivo_2 = st.file_uploader(
        "Carga el Archivo 2 (CSV o Excel)",
        type=["csv", "xlsx"],
        key="archivo_2"
    )

    if archivo_2 is not None:
        try:
            if archivo_2.name.endswith(".csv"):
                df2 = pd.read_csv(archivo_2)
            else:
                df2 = pd.read_excel(archivo_2, header=1)

            st.session_state["df_archivo_2"] = df2
            st.session_state["nombre_archivo_2"] = archivo_2.name
            st.success(f"Archivo 2 cargado correctamente: {archivo_2.name}")
        except Exception as e:
            st.error(f"Ocurrió un error al procesar el Archivo 2 ({archivo_2.name}): {e}")

    if st.session_state["df_archivo_2"] is not None:
        st.info(f"Archivo 2 sigue cargado en memoria: **{st.session_state['nombre_archivo_2']}**")
    else:
        st.warning("Archivo 2 aún no ha sido cargado.")

    st.write("---")

    st.markdown("### Descargar plantilla de bitácora")
    st.write("Puedes descargar una plantilla de Excel para facilitar la carga de datos en el formato esperado.")

    with open("Plantilla_Bepensa.xlsx", "rb") as file:
        st.download_button(
            label="Descargar plantilla Excel aquí ⬇",
            data=file.read(),
            file_name="Plantilla_Bepensa.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="descargar_plantilla"
        )

    st.write("---")
    st.markdown("### Cargar plantilla con datos llenados")
    st.write("Una vez que completes la plantilla, súbela aquí para procesarla.")

    archivo_plantilla = st.file_uploader(
        "Sube aquí el archivo Excel basado en la plantilla",
        type=["xlsx"],
        key="archivo_plantilla"
    )

    if archivo_plantilla is not None:
        try:
            df_plantilla = pd.read_excel(archivo_plantilla)
            st.session_state["df_plantilla"] = df_plantilla
            st.success(f"Plantilla cargada correctamente: {archivo_plantilla.name}")
        except Exception as e:
            st.error(f"Error al procesar el archivo de plantilla: {e}")

    if st.session_state.get("df_plantilla") is not None:
        st.info("Plantilla con datos sigue cargada en memoria.")
    else:
        st.warning("Aún no se ha cargado una plantilla con datos.")

    st.write(
        "Nota: La presente herramienta está enfocada en el análisis integral de la información "
        "relacionada con viajes, fallas y bitácoras, facilitando la visualización, exploración y comprensión "
        "de los datos para apoyar la toma de decisiones. Para esto, es funadamentar que los archivos cargados **UNICAMENTE CONTENGAN LA HOJA DONDE ESTAN LOS DATOS**, no hojas adicionales."
    )

# Diccionario de mapeo: Clasificación de servicio -> Tipo de costo
categoria_map = {
    # Preventivo Menor (PM1)
    "PREVENTIVO": "Preventivo Menor",
    "A 25,000 KM": "Preventivo Menor",
    "A 30,000 KM": "Preventivo Menor",
    "A 39 000 KMS": "Preventivo Menor",
    "INSPECCIÓN DE VIAJE 0 KMS": "Preventivo Menor",
    "GENERAL": "Preventivo Menor",
    "LAVADERO": "Preventivo Menor",

    # Preventivo Intermedio (PM2)
    "B 75,000 KM": "Preventivo intermedio",
    "B 90,000 KM": "Preventivo intermedio",
    "B 120,000 KM": "Preventivo intermedio",
    "CONSERVACIÓN": "Preventivo intermedio",
    "PRE ENTREGA DE UNIDAD": "Preventivo intermedio",

    # Preventivo Mayor (PM3)
    "C 198,000 KMS": "Preventivo Mayor",
    "C 225,000 KM": "Preventivo Mayor",
    "C 240,000 KM": "Preventivo Mayor",

    # Correctivo Menor (CM1)
    "CARROCERIA / CABINA": "Correctivo menor",
    "SISTEMA ELECTRICO": "Correctivo menor",
    "SISTEMA DE LLANTAS": "Correctivo menor",
    "LLANTAS": "Correctivo menor",
    "MODIFICACIONES": "Correctivo menor",

    # Correctivo Moderado (CM2)
    "SISTEMA DE SUSPENSION": "Correctivo intermedio",
    "SISTEMA HIDRAULICO": "Correctivo intermedio",
    "EQUIPO ALIADO DE SISTEMA HIDRAULICO": "Correctivo intermedio",
    "EQUIPO ALIADO ESTRUCTURAL": "Correctivo intermedio",
    "SISTEMA DE ARRASTRE": "Correctivo intermedio",
    "SISTEMA DE FRENOS": "Correctivo intermedio",
    "TREN MOTRIZ": "Correctivo intermedio",
    "CORRECTIVO": "Correctivo intermedio",

    # Correctivo Mayor (CM3)
    "MOTOR": "Correctivo mayor",
    "TRANSMISION": "Correctivo mayor",
    "SINIESTRO": "Correctivo mayor",
    "SINIESTRO 0 KMS": "Correctivo mayor",
    "RESCATE": "Correctivo mayor",
}

categoria_map_norm = {
    normalizar_texto(k): v
    for k, v in categoria_map.items()
}

# página: visualización interactiva fallas / viajeselif page == "Visualización Interactiva":
if page == "Visualización Interactiva":
    st.title("Visualización Interactiva: Porcentaje de fallas vs viajes por Tractocamión")

    paleta = ["#FFA15A", "#F3AE19", "#FFC561", "#F36D19", "#FF7F50", "#D62728"]  # Colores personalizados

    # Recuperar lo que se cargó en "Análisis de Datos"
    df1 = st.session_state.get("df_archivo_1")
    df2 = st.session_state.get("df_archivo_2")

    if df1 is None and df2 is None:
        st.warning("Primero carga los archivos de datos en la sección 'Análisis de Datos'.")
    else:
        # Construimos una lista solo con los que existan
        dfs = []
        if df1 is not None:
            dfs.append(df1)
        if df2 is not None:
            dfs.append(df2)

        viajes_df = None
        fallas_df = None

        # Detectar automáticamente cuál es "viajes" y cuál es "fallas"
        for df in dfs:
            cols_lower = [c.lower() for c in df.columns]

            # Viajes: columna Tractocamión (con o sin acento)
            if any(c in cols_lower for c in ["tractocamión", "tractocamion"]):
                viajes_df = df

            # Fallas: columna unidad
            if "unidad" in cols_lower:
                fallas_df = df

        if viajes_df is None or fallas_df is None:
            st.error(
                "No se pudieron identificar correctamente las bases de 'viajes' y 'fallas'. "
                "Verifica que un archivo tenga la columna 'Tractocamión' y el otro la columna 'unidad'."
            )

            # (Opcional) Mostrar columnas para depurar
            st.write("Columnas archivo 1:", list(df1.columns) if df1 is not None else "No cargado")
            st.write("Columnas archivo 2:", list(df2.columns) if df2 is not None else "No cargado")

        else:
            # Nombre exacto de las columnas clave
            col_tracto = next(
                c for c in viajes_df.columns
                if c.lower() in ["tractocamión", "tractocamion"]
            )
            col_unidad = next(
                c for c in fallas_df.columns
                if c.lower() == "unidad"
            )

            viajes = viajes_df.copy()
            fallas = fallas_df.copy()

            # Normalizar IDs
            viajes["id_tracto"] = viajes[col_tracto].astype(str).str.strip().str.upper()
            fallas["id_unidad"] = fallas[col_unidad].astype(str).str.strip().str.upper()

            # Filtrar solo los que empiezan con 'T'
            viajes_T = viajes[viajes["id_tracto"].str.startswith("T", na=False)]
            fallas_T = fallas[fallas["id_unidad"].str.startswith("T", na=False)]

            # Clasificar cada mantenimiento según la 'Clasificación de servicio'
            if "Clasificación de servicio" in fallas_T.columns:
    # Columna original normalizada
                fallas_T["clasif_norm"] = fallas_T["Clasificación de servicio"].apply(normalizar_texto)

    # Mapear usando el diccionario normalizado
                fallas_T["Tipo de costo"] = fallas_T["clasif_norm"].map(categoria_map_norm)
                fallas_T["Tipo de costo"] = fallas_T["Tipo de costo"].fillna("Sin clasificar")
            else:
                fallas_T["Tipo de costo"] = "Sin clasificar"



            # Si no hay viajes T, avisar y salir
            if viajes_T.empty:
                st.warning("No se encontraron viajes con Tractocamión que comience con 'T'.")
            else:
                viajes_counts = (
                    viajes_T.groupby("id_tracto")
                    .size()
                    .rename("viajes_totales")
                )

                fallas_counts = (
                    fallas_T.groupby("id_unidad")
                    .size()
                    .rename("fallas_totales")
                )

                resumen = (
                    viajes_counts.to_frame()
                    .merge(
                        fallas_counts.to_frame(),
                        left_index=True,
                        right_index=True,
                        how="left"
                    )
                    .fillna(0)
                )

                resumen["fallas_totales"] = resumen["fallas_totales"].astype(int)
                resumen["porcentaje_fallas"] = (
                    resumen["fallas_totales"] / resumen["viajes_totales"] * 100
                ).round(2)

                # Pasar el índice (id_tracto) a columna y renombrarla a 'Unidad'
                resumen = resumen.reset_index()
                id_col = resumen.columns[0]           # normalmente 'id_tracto'
                resumen = resumen.rename(columns={id_col: "Unidad"})

                st.subheader("Resumen global por Unidad / Tractocamión (solo los que comienzan con 'T')")
                st.dataframe(resumen)

                # Selector de unidad
                unidades = resumen["Unidad"].tolist()
                unidad_sel = st.selectbox(
                    "Selecciona una Unidad / Tractocamión:",
                    unidades
                )

                datos_unidad = resumen[resumen["Unidad"] == unidad_sel].iloc[0]

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Viajes totales", int(datos_unidad["viajes_totales"]))
                with col2:
                    st.metric("Fallas totales", int(datos_unidad["fallas_totales"]))
                with col3:
                    st.metric("% fallas / viajes", f"{datos_unidad['porcentaje_fallas']} %")

                st.markdown("### Gráfico de viajes vs fallas de la unidad seleccionada")

                fig_sel = px.bar(
                    x=["Viajes", "Fallas"],
                    y=[datos_unidad["viajes_totales"], datos_unidad["fallas_totales"]],
                    color_discrete_sequence=paleta,
                    labels={"x": "Tipo de evento", "y": "Número de eventos"},
                    text=[datos_unidad["viajes_totales"], datos_unidad["fallas_totales"]],
                )
                fig_sel.update_traces(textposition="outside")
                st.plotly_chart(fig_sel, use_container_width=True)


                st.markdown("### Ranking de tractocamiones por número de mantenimientos")

                dfg = fallas_T.copy()

                mantenimientos_total = (
                    dfg.groupby("id_unidad")
                    .size()
                    .reset_index(name="Mantenimientos")
                )

                # Renombrar id_unidad a Unidad para ser consistentes
                mantenimientos_total = mantenimientos_total.rename(columns={"id_unidad": "Unidad"})

                if not mantenimientos_total.empty:
                    # Máximo posible de unidades
                    max_n = int(len(mantenimientos_total))

                    # Slider para que el usuario elija cuántos tractos ver
                    N = st.slider(
                        "Selecciona cuántos tractos mostrar en el ranking",
                        min_value=1,
                        max_value=max_n,
                        value=min(10, max_n)
                    )

                    # Top N por número de mantenimientos
                    top_tractos_mantenimientos = (
                        mantenimientos_total
                        .sort_values(by="Mantenimientos", ascending=False)
                        .head(N)
                    )

                    # Gráfico de barras simple
                    fig_top_mant = px.bar(
                        top_tractos_mantenimientos,
                        x="Unidad",
                        y="Mantenimientos",
                        color_discrete_sequence=paleta,
                        text="Mantenimientos",
                        labels={"Unidad": "Tracto", "Mantenimientos": "Mantenimientos"},
                        title=f"Top {N} tractos por número de mantenimientos",
                    )
                    fig_top_mant.update_traces(textposition="outside")
                    st.plotly_chart(fig_top_mant, use_container_width=True)

                    st.markdown("### Composición de los mantenimientos por tipo de costo (Top seleccionados)")

                    # Unidades que están en el Top N
                    unidades_top = top_tractos_mantenimientos["Unidad"].unique().tolist()

                    # Filtramos fallas solo de esas unidades
                    fallas_top = fallas_T[fallas_T["id_unidad"].isin(unidades_top)].copy()

                    # Agrupamos por Unidad y Tipo de costo
                    eventos_tipo = (
                        fallas_top
                        .groupby(["id_unidad", "Tipo de costo"])
                        .size()
                        .reset_index(name="Cantidad de Eventos")
                    )

                    # Renombrar id_unidad -> Unidad para que coincida con el eje X
                    eventos_tipo = eventos_tipo.rename(columns={"id_unidad": "Unidad"})

                    # Ordenar las unidades según el ranking de mantenimientos (mismo orden que el Top N)
                    orden_unidades = top_tractos_mantenimientos["Unidad"].tolist()
                    eventos_tipo["Unidad"] = pd.Categorical(
                        eventos_tipo["Unidad"],
                        categories=orden_unidades,
                        ordered=True
                    )
                    eventos_tipo = eventos_tipo.sort_values(["Unidad", "Tipo de costo"])

                    

                    # Gráfico de barras apiladas
                    fig_stack = px.bar(
                        eventos_tipo,
                        x="Unidad",
                        y="Cantidad de Eventos",
                        color="Tipo de costo",
                        color_discrete_sequence=paleta,
                        labels={
                            "Unidad": "Unidad / Tracto",
                            "Cantidad de Eventos": "Cantidad de eventos",
                            "Tipo de costo": "Tipo de costo"
                        },
                        title=f"Distribución del tipo de costo en el Top {N} tractos por mantenimientos",
                    )
                    fig_stack.update_layout(barmode="stack")
                    st.plotly_chart(fig_stack, use_container_width=True)

                else:
                    st.info("No hay datos de mantenimientos para construir el ranking.")
                
                st.markdown("---")
    st.markdown("""
**Nota: Se dividieron los mantenimientos en la siguiente manera:**


**Preventivo Menor (PM1)**  
- PREVENTIVO  
- A 25,000 KM  
- A 30,000 KM  
- A 39,000 KMS  
- INSPECCIÓN DE VIAJE 0 KMS  
- GENERAL  
- LAVADERO  

**Preventivo Intermedio (PM2)**  
- B 75,000 KM  
- B 90,000 KM  
- B 120,000 KM  
- CONSERVACIÓN  
- PRE ENTREGA DE UNIDAD  

**Preventivo Mayor (PM3)**  
- C 198,000 KMS  
- C 225,000 KM  
- C 240,000 KM  


**Correctivo Menor (CM1)**  
- CARROCERÍA / CABINA  
- SISTEMA ELÉCTRICO  
- SISTEMA DE LLANTAS  
- LLANTAS  
- MODIFICACIONES  


**Correctivo Moderado (CM2)**  
- SISTEMA DE SUSPENSIÓN  
- SISTEMA HIDRÁULICO  
- EQUIPO ALIADO DE SISTEMA HIDRÁULICO  
- EQUIPO ALIADO ESTRUCTURAL  
- SISTEMA DE ARRASTRE  
- SISTEMA DE FRENOS  
- TREN MOTRIZ  
- CORRECTIVO  


**Correctivo Mayor (CM3)**  
- MOTOR  
- TRANSMISIÓN  
- SINIESTRO  
- SINIESTRO 0 KMS  
- RESCATE  
""")


elif page == "Visualización Bitácoras":
    st.title("Visualización de Bitácoras – Análisis por Cliente")

    if "df_plantilla" not in st.session_state or st.session_state["df_plantilla"] is None:
        st.info("Primero carga la plantilla de bitácora con datos en la sección 'Análisis de Datos'.")
        st.stop()

    dfb = st.session_state["df_plantilla"].copy()
    dfb.columns = dfb.columns.str.strip()   # limpia espacios en nombres de columnas

    # Verificar que todas las columnas esperadas estén presentes
    columnas_esperadas = [
        "Mes", "Cliente", "Kilometraje Bitacora", "Costo",
        "Litros de consumidos", "Litros de consumo termo",
        "Rendimiento tracto", "Horas Termo", "Rendimiento Termo",
        "Costoxkm", "Ingreso", "% combustible",
        "Unidades contratadas", "Unidades colocadas", "%NS",
        "Kilometros T Cliente", "Unidades contratadas por cliente",
        "Excedente de Unidades", "Total excedente x cliente",
        "km excedente", "Costo Excedente"
    ]

    faltantes = [c for c in columnas_esperadas if c not in dfb.columns]
    if faltantes:
        st.warning("Las siguientes columnas NO están en tu archivo cargado:")
        st.write(faltantes)
        st.stop()

    # Selector de cliente
    clientes = dfb["Cliente"].dropna().unique()

    if len(clientes) == 0:
        st.error("No se encontraron clientes en la columna 'Cliente'.")
        st.stop()

    cliente_sel = st.selectbox("Selecciona un Cliente:", sorted(clientes))
    df_cliente = dfb[dfb["Cliente"] == cliente_sel]

    st.markdown(f"## Información del cliente **{cliente_sel}**")

    def safe_sum(col):
        return df_cliente[col].fillna(0).sum() if col in df_cliente.columns else 0

    def safe_mean(col):
        return df_cliente[col].dropna().mean() if col in df_cliente.columns else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Kilometraje total", f"{safe_sum('Kilometraje Bitacora'):,.0f}")
    with col2:
        st.metric("Costo total", f"${safe_sum('Costo'):,.2f}")
    with col3:
        st.metric("Ingreso total", f"${safe_sum('Ingreso'):,.2f}")

    col4, col5, col6 = st.columns(3)
    with col4:
        st.metric("Costo excedente", f"${safe_sum('Costo Excedente'):,.2f}")
    with col5:
        st.metric("Km excedente total", f"{safe_sum('km excedente'):,.0f}")
    with col6:
        st.metric("Nivel de servicio X / 100", f"{safe_mean('%NS'):.2f}")

    st.markdown("---")
    st.subheader("Gráficos de análisis")

        # Convertir columnas clave a numéricas por seguridad
    for col in [
        "Kilometraje Bitacora",
        "Costo",
        "Litros de consumidos",
        "Rendimiento tracto",
        "km excedente",
    ]:
        df_cliente[col] = pd.to_numeric(df_cliente[col], errors="coerce")


    st.markdown("## Unidades Contratadas y Colocadas por Mes")

# Convertir columnas a numéricas por seguridad
    df_cliente["Unidades contratadas"] = pd.to_numeric(df_cliente["Unidades contratadas"], errors="coerce")
    df_cliente["Unidades colocadas"]   = pd.to_numeric(df_cliente["Unidades colocadas"], errors="coerce")

# Orden de meses
    orden_meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio",
               "Agosto","Septiembre","Octubre","Noviembre","Diciembre"]

    df_cliente["Mes"] = pd.Categorical(df_cliente["Mes"], categories=orden_meses, ordered=True)


    st.subheader("Unidades Contratadas")

    chart_contratadas = (
        alt.Chart(df_cliente)
        .mark_bar(color="#FF8C42")  # naranja corporativo
        .encode(
            x=alt.X("Mes:N", title="Mes"),
            y=alt.Y("Unidades contratadas:Q", title="Cantidad"),
            tooltip=["Mes", "Unidades contratadas"]
    )
        .properties(
            height=350,
            
    )
)

    st.altair_chart(chart_contratadas, use_container_width=True)

    st.subheader("Unidades Colocadas")

    chart_colocadas = (
        alt.Chart(df_cliente)
        .mark_bar(color="#FFA95A")  # naranja más claro
        .encode(
            x=alt.X("Mes:N", title="Mes"),
            y=alt.Y("Unidades colocadas:Q", title="Cantidad"),
            tooltip=["Mes", "Unidades colocadas"]
    )
        .properties(
            height=350,
            
    )
)

    st.altair_chart(chart_colocadas, use_container_width=True)

   
    st.subheader("Registros completos del cliente seleccionado")
    st.dataframe(df_cliente)

    