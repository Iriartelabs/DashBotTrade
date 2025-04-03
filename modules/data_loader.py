import streamlit as st
import pandas as pd

def render_data_loader():
    """
    Renderiza la interfaz de Carga de Datos.
    """
    st.title("DashBotTrade")
    st.markdown("## Dashboard para análisis de Trading")
    st.header("Carga de Datos de Trading")
    uploaded_file = st.file_uploader("Sube tu archivo CSV de trading", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("Datos cargados correctamente")
        st.dataframe(df)
    else:
        st.info("Sube un archivo para comenzar")
