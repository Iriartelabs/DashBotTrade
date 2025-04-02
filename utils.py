import streamlit as st
import time
import json

def refrescar():
    time.sleep(10)
    st.experimental_rerun()  # Actualiza la UI

def load_alpaca_assets(file_path):
    """
    Carga y analiza los datos de activos desde un archivo JSON.

    Args:
        file_path (str): Ruta al archivo que contiene los datos de Alpaca.

    Returns:
        list: Lista de activos cargados.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            print(f"Se cargaron {len(data)} activos desde Alpaca.")
            return data
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        return []