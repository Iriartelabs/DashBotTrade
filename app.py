import streamlit as st
import pandas as pd
import os, json, shutil
from utils import refrescar  # Importamos la función reutilizable
from config import current_config

# Configuración de la página
st.set_page_config(
    page_title="DashBotTrade",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar variables de sesión
def initialize_session_state():
    if "module" not in st.session_state:
        st.session_state.module = "Inicio"
    if "show_create_form" not in st.session_state:
        st.session_state.show_create_form = False

initialize_session_state()

# Definir la ruta de la carpeta donde se almacenan los addons
addons_dir = "addons"

# Función para cambiar el módulo activo
def set_module(mod):
    st.session_state.module = mod

# Función para renderizar el contenido principal según el módulo seleccionado
from modules.data_loader import render_data_loader
from modules.charts_module import render_charts_module

def render_module(module_name):
    if module_name == "Inicio":
        st.title("DashBotTrade")
        st.markdown("## Dashboard para análisis de Trading")
        st.header("Bienvenido a DashBotTrade")
        st.info("Esta es la pantalla principal.")
    elif module_name == "Carga de Datos":
        render_data_loader()
    elif module_name == "Módulo de Gráficos":
        render_charts_module()
    elif module_name == "Configuración":
        render_configuration()
    elif module_name == "Gestor de Addons":
        render_addons_manager()
    elif module_name == "Refresh":
        st.session_state.module = st.session_state.get("last_module", "Inicio")
    else:
        render_addon_ui(module_name)

from addons.alertsbot.src.symbols_manager import SymbolsManager  # Importamos SymbolsManager para probar la conexión

# Función para renderizar la configuración de Alpaca
def render_configuration():
    st.title("DashBotTrade")
    st.header("Configuración")
    st.subheader("Configuración de la API de Alpaca Markets")

    from services.alpaca_integration import AlpacaIntegration

    alpaca = AlpacaIntegration()
    connection_status = alpaca.test_connection()
    if connection_status["status"] == "success":
        st.success(f"Conexión exitosa: {connection_status['message']}")
    else:
        st.error(f"Error de conexión: {connection_status['message']}")

    # Formulario para configurar las claves de la API
    with st.form("alpaca_config_form"):
        api_key = st.text_input("API Key", value=current_config.ALPACA_API_KEY)
        api_secret = st.text_input("API Secret", value=current_config.ALPACA_API_SECRET, type="password")
        base_url = st.text_input("Base URL", value=current_config.ALPACA_BASE_URL)
        submitted = st.form_submit_button("Guardar configuración")
        if submitted:
            # Guardar las claves en el archivo de configuración o variables de entorno
            with open("alpaca_config.json", "w") as f:
                json.dump({
                    "ALPACA_API_KEY": api_key,
                    "ALPACA_API_SECRET": api_secret,
                    "ALPACA_BASE_URL": base_url
                }, f, indent=4)
            st.success("Configuración actualizada. Por favor, prueba la conexión nuevamente.")

    # Botón para probar la conexión manualmente
    if st.button("Probar conexión con Alpaca"):
        connection_status = alpaca.test_connection()
        if connection_status["status"] == "success":
            st.success(f"Conexión exitosa: {connection_status['message']}")
            st.json(connection_status["example_assets"])
        else:
            st.error(f"Error de conexión: {connection_status['message']}")

# Función para renderizar el gestor de addons
def render_addons_manager():
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

# Función para renderizar la interfaz de un addon
def render_addon_ui(module_name):
    try:
        import importlib
        # Usar el nombre de la carpeta (module_name) para importar el módulo
        ui_module_path = f"addons.{module_name}.ui.alertsbot"
        ui_module = importlib.import_module(ui_module_path)
        if not hasattr(ui_module, "render"):
            st.error(f"El módulo '{module_name}' no tiene una función 'render'.")
            return
        ui_module.render()
    except ModuleNotFoundError:
        st.error(f"No se pudo encontrar el módulo para el addon '{module_name}'. Asegúrate de que esté instalado correctamente.")
    except ImportError as e:
        st.error(f"Error al importar el módulo del addon '{module_name}': {e}")
    except Exception as e:
        st.error(f"Error inesperado al cargar la interfaz del addon '{module_name}': {e}")
        # Opcional: Registrar el error en un archivo de log
        with open("error.log", "a") as log_file:
            log_file.write(f"Error en addon '{module_name}': {e}\n")

# Sidebar personalizado con botones independientes
st.sidebar.markdown("## Navegación")
if st.sidebar.button("Inicio"):
    set_module("Inicio")
if st.sidebar.button("Carga de Datos"):
    set_module("Carga de Datos")
if st.sidebar.button("Módulo de Gráficos"):
    set_module("Módulo de Gráficos")

from services.addons_manager import scan_addons

# Escanear addons y registrar el addon de Claude
addon_list = scan_addons()  # Lee todos los addons (cada uno con su config)

if addon_list:
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

# Renderizar el módulo seleccionado
render_module(st.session_state.module)