import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('Acuíferos del Uruguay')
st.markdown('---')

@st.cache_data
def cargar_datos_muestras():
    df = pd.read_csv('C:/Users/tania/PycharmProjects/Python-Data-Analysis-GrupoA/data/processed/Base_de_datos_Python_GRUPO A.csv',sep=';')
    return df

try:
    df_completo = cargar_datos_muestras()
except FileNotFoundError:
    st.error("❌ No se encontró el archivo procesado. Asegúrate de ejecutar la Fase 1 primero.")
    st.stop()

st.header('📈 Gestión Operativa por Oficina Regional')
st.info("Distribución de la carga laboral acumulada por territorio administrativo:")

df_completo['Regional'] = df_completo['Regional'].astype(str).str.strip()

# Generamos la serie de frecuencias. st.bar_chart usa el índice como eje X
chart_data = df_completo['Regional'].value_counts()

# Desplegamos el gráfico interactivo directamente en el layout de la app
st.bar_chart(chart_data)

st.title("Panel de Control: Gestión de Recursos Hídricos")
fig, axis = plt.subplots(2, 2, figsize=(14, 10))

sns.countplot(
    ax = axis[0, 0],
    data = df_completo,
    x="Estado",
    order=df_completo['Estado'].value_counts().index,
    hue="Estado",
    palette="Blues_r",
    legend=False
)
axis[0, 0].set_title("Distribución por Estado del Trámite")
axis[0, 0].set_xlabel("Estado")
axis[0, 0].set_ylabel("Cantidad de Registros")
axis[0, 0].tick_params(axis='x', rotation=45) # Añadido rotación por si los textos son largos


top_usos = df_completo['Uso'].value_counts().head(5).index
df_usos = df_completo[df_completo['Uso'].isin(top_usos)]
sns.countplot(
    ax = axis[0, 1],
    data = df_usos,
    x = "Uso",
    order = top_usos,
    hue = "Uso",
    palette = "Greens_r",
    legend = False
)
axis[0, 1].set_title("Top 5 Usos Principales del Agua")
axis[0, 1].set_xlabel("Uso")
axis[0, 1].set_ylabel(None)
axis[0, 1].tick_params(axis='x', rotation=45)

top_regionales = df_completo['Regional'].value_counts().head(5).index
df_regionales = df_completo[df_completo['Regional'].isin(top_regionales)]
sns.countplot(
    ax = axis[1, 0],
    data = df_regionales,
    x = "Regional",
    order = top_regionales,
    hue = "Regional",
    palette = "Purples_r",
    legend = False
)
axis[1, 0].set_title("Top 5 Regionales con más Solicitudes")
axis[1, 0].set_xlabel("Regional")
axis[1, 0].set_ylabel("Cantidad de Registros")
axis[1, 0].tick_params(axis='x', rotation=45)

top_deptos = df_completo['Departamento'].value_counts().head(5).index
df_deptos = df_completo[df_completo['Departamento'].isin(top_deptos)]
sns.countplot(
    ax = axis[1, 1],
    data = df_deptos,
    x = "Departamento",
    order = top_deptos,
    hue = "Departamento",
    palette = "Oranges_r",
    legend = False
)
axis[1, 1].set_title("Top 5 Departamentos con más Obras")
axis[1, 1].set_xlabel("Departamento")
axis[1, 1].set_ylabel(None)
axis[1, 1].tick_params(axis='x', rotation=45)

plt.tight_layout()

st.pyplot(fig)

st.subheader("🗺️ Distribución Geográfica de las Solicitudes")
st.markdown("Ubicación e impacto territorial de las solicitudes registradas:")

df_mapa = df_completo[["Latitud", "Longitud"]].copy()
df_mapa["lat"] = pd.to_numeric(df_mapa["Latitud"].astype(str).str.replace(',', '.'), errors="coerce")
df_mapa["lon"] = pd.to_numeric(df_mapa["Longitud"].astype(str).str.replace(',', '.'), errors="coerce")

df_mapa_listo = df_mapa[["lat", "lon"]].dropna()

if df_mapa_listo.empty:
    st.info("⚠️")
else:
    st.map(df_mapa_listo, use_container_width=True)