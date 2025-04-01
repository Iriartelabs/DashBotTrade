import streamlit as st
import time

def refrescar():
    time.sleep(10)
    st.experimental_rerun()  # Actualiza la UI