import streamlit as st
import pandas as pd
import os, json, shutil
#from utils import refrescar

# Configuración de la página
st.set_page_config(
    page_title="DashBotTrade",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar la variable de sesión para el módulo seleccionado
if "module" not in st.session_state:
    st.session_state.module = "Inicio"
if "show_create_form" not in st.session_state:
    st.session_state.show_create_form = False

def set_module(mod):
    st.session_state.module = mod

#def refrescar():
    # Guarda el módulo activo en una variable de sesión
#   st.session_state.last_module = st.session_state.module
    # Cambia temporalmente a un módulo de refresco
#   st.session_state.module = "Refresh"

# ------------------
# Sidebar personalizado con botones independientes
# ------------------
st.sidebar.markdown("## Navegación")
# Botones principales de navegación
if st.sidebar.button("Inicio"):
    set_module("Inicio")
if st.sidebar.button("Carga de Datos"):
    set_module("Carga de Datos")
if st.sidebar.button("Módulo de Gráficos"):
    set_module("Módulo de Gráficos")
from services.addons_manager import scan_addons
addon_list = scan_addons()  # Lee todos los addons (cada uno con su config)

if addon_list:
    #st.sidebar.markdown("---")
    #st.sidebar.markdown("## Addons")
    for addon in addon_list:
        nav = addon.get("nav_button", {})
        if nav.get("show", False):
            button_label = nav.get("label", addon["name"])
            if st.sidebar.button(button_label):
                st.session_state.module = addon["name"]

st.sidebar.markdown("---")
st.sidebar.markdown("## Herramientas")
if st.sidebar.button("Configuración"):
    set_module("Configuración")
if st.sidebar.button("Gestor de Addons"):
    set_module("Gestor de Addons")

# ------------------
# Funciones para escanear y refrescar la lista de addons
# ------------------
addons_dir = "addons"





# ------------------
# Contenido principal según módulo seleccionado
# ------------------
if st.session_state.module == "Inicio":
    st.title("DashBotTrade")
    st.markdown("## Dashboard para análisis de Trading")
    st.header("Bienvenido a DashBotTrade")
    st.info("Esta es la pantalla principal. Los módulos se integrarán aquí conforme avance el desarrollo.")

elif st.session_state.module == "Carga de Datos":
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

elif st.session_state.module == "Módulo de Gráficos":
    st.title("DashBotTrade")
    st.markdown("## Dashboard para análisis de Trading")
    st.header("Módulo de Gráficos")
    st.info("Aquí se mostrarán los gráficos interactivos. (Módulo pendiente de implementación)")

elif st.session_state.module == "Configuración":
    st.title("DashBotTrade")
    st.markdown("## Dashboard para análisis de Trading")
    st.header("Configuración")
    st.subheader("Configuración de la API de Alpaca Markets")
    
    # Archivo de configuración de Alpaca
    config_file = "alpaca_config.json"
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            alpaca_config = json.load(f)
    else:
        alpaca_config = {
            "ALPACA_API_KEY": "",
            "ALPACA_API_SECRET": "",
            "ALPACA_BASE_URL": "https://paper-api.alpaca.markets"
        }
    
    with st.form("alpaca_config_form"):
        api_key = st.text_input("API Key", value=alpaca_config.get("ALPACA_API_KEY", ""))
        api_secret = st.text_input("API Secret", value=alpaca_config.get("ALPACA_API_SECRET", ""), type="password")
        base_url = st.text_input("Base URL", value=alpaca_config.get("ALPACA_BASE_URL", "https://paper-api.alpaca.markets"))
        submitted = st.form_submit_button("Guardar configuración")
        if submitted:
            alpaca_config = {
                "ALPACA_API_KEY": api_key,
                "ALPACA_API_SECRET": api_secret,
                "ALPACA_BASE_URL": base_url
            }
            with open(config_file, "w") as f:
                json.dump(alpaca_config, f, indent=4)
            st.success("Configuración de Alpaca actualizada.")
    st.write("La configuración actual es:")
    st.json(alpaca_config)

elif st.session_state.module == "Gestor de Addons":
    st.title("DashBotTrade")
    st.markdown("## Dashboard para análisis de Trading")
    st.header("Gestor de Addons")
    
    from services.addons_manager import create_addon, scan_addons, refresh_addons, toggle_addons, uninstall_addons, import_addon

    # Escanea la carpeta de addons usando la función importada
    addon_list = scan_addons()
    
    # Sección para Importar o Crear addons siempre visibles
    st.markdown("### Añadir Nuevo Addon")
    col_import, col_create = st.columns(2)
    with col_import:
        # Reemplazamos el mensaje de funcionalidad pendiente por un file uploader para el zip del addon.
        uploaded_zip = st.file_uploader("Selecciona el archivo .zip del addon", type=["zip"])
        if uploaded_zip is not None:
            result = import_addon(uploaded_zip)
            if result is not None:
                st.success("Addon importado correctamente.")
                addon_list = refresh_addons()
                
    with col_create:
        if st.button("Crear Nuevo Addon"):
            st.session_state.show_create_form = True

    # Formulario para crear un nuevo addon
    if st.session_state.get("show_create_form", False):
        with st.form("create_addon_form"):
            addon_id = st.text_input("ID del Addon (sin espacios)", value="")
            addon_name = st.text_input("Nombre del Addon", value="")
            addon_description = st.text_area("Descripción", value="")
            submitted = st.form_submit_button("Crear Addon")
            if submitted:
                result = create_addon(addon_id.strip(), addon_name.strip(), addon_description.strip())
                st.success(result)
                st.session_state.show_create_form = False
                addon_list = refresh_addons()  # Actualiza la lista

    st.markdown("---")
    
    # Mostrar tabla con la información de los addons
    if addon_list:
        data = []
        for addon in addon_list:
            data.append({
                "ID": addon["folder"],
                "Nombre": addon["name"],
                "Versión": addon.get("version", "N/A"),
                "Descripción": addon.get("description", ""),
                "Activo": "Sí" if addon.get("active", True) else "No"
            })
        df = pd.DataFrame(data)
        st.write("### Lista de Addons")
        st.table(df)
        
        # Permitir seleccionar addons para acciones en lote
        options = {addon["folder"]: f"{addon['name']} ({addon['folder']})" for addon in addon_list}
        selected = st.multiselect("Selecciona los addons a modificar", list(options.keys()), format_func=lambda x: options[x])
        
        st.markdown("### Acciones en lote")
        colA, colB, colC, colD = st.columns(4)
        if colA.button("Activar/Desactivar"):
            addon_list = toggle_addons(addon_list, selected, addons_dir)
        if colB.button("Editar"):
            st.info("Funcionalidad de edición pendiente.")
        if colC.button("Exportar"):
            st.info("Funcionalidad de exportación pendiente.")
        if colD.button("Desinstalar"):
            addon_list = uninstall_addons(addon_list, selected, addons_dir)
    else:
        st.info("No hay addons instalados.")

elif st.session_state.module == "Refresh":
    st.title("")
    st.markdown("")
    st.header("")
    st.info("")
    st.session_state.module = st.session_state.get("last_module", "Inicio")

elif st.session_state.module in [addon["name"] for addon in addon_list]:
    try:
        import importlib
        module_name = st.session_state.module  # por ejemplo, "hola_addon"
        ui_module_path = f"addons.{module_name}.ui.ui"
        ui_module = importlib.import_module(ui_module_path)
        ui_module.render()  # Se renderiza la interfaz definida en ui.py del addon
    except Exception as e:
        st.error(f"Error al cargar la interfaz del addon: {e}")