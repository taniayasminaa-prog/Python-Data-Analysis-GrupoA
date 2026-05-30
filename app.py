import streamlit as st
import pandas as pd
import numpy as np

st.title('Gestión de Recursos Hídricos')
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

st.subheader('🗺️ Distribución Geográfica de los Expedientes')
st.markdown("Ubicación e impacto territorial de las solicitudes y perforaciones registradas en el territorio:")


# Validar si las columnas de coordenadas existen
if {"latitud", "longitud"}.issubset(df_completo.columns):
    st.subheader("Mapa geográfico de solicitudes")

    # Quitamos los valores nulos para evitar errores de renderizado
    df_mapa = df_completo.dropna(subset=['latitud', 'longitud'])

    if df_mapa.empty:
        st.info("No hay coordenadas válidas disponibles para los filtros seleccionados.")
    else:
        # Renombramos las columnas a lo que exige Streamlit ('lat' y 'lon')
        df_mapa_listo = df_mapa.rename(columns={
            "latitud": "lat",
            "longitud": "lon"
        })

        st.map(df_mapa_listo, use_container_width=True)


