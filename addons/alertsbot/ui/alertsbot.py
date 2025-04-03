import streamlit as st
from addons.alertsbot.src.symbols_manager import SymbolsManager
from services.alpaca_integration import AlpacaIntegration
import importlib
import json

# Cargar las categorías y tipos de alertas desde el archivo JSON
with open("c:/xampp/htdocs/DashBotTrade/addons/alertsbot/src/alert_types.json", "r", encoding="utf-8") as f:
    alert_types_by_category = json.load(f)

# Instancias necesarias
alpaca = AlpacaIntegration()
symbols_manager = SymbolsManager()

def render():
    """
    Renderiza la interfaz mejorada del addon Bot de Alertas.
    """
    st.title("🔔 Bot de Alertas")
    st.markdown("## Gestión de Alertas para DashBotTrade")

    # Obtener activos desde la API de Alpaca
    assets = alpaca.get_assets()

    # Verificar si la respuesta es válida
    if isinstance(assets, list):  # Verifica que la respuesta sea una lista
        # Extraer categorías únicas (class) de los activos
        categories = ["Todos"] + list(set(asset["class"] for asset in assets))
        categories.sort()  # Ordenar alfabéticamente

        # Mostrar combobox con las categorías
        selected_category = st.selectbox("Categoría de activo", categories)

        # Filtrar activos por la categoría seleccionada
        filtered_assets = assets if selected_category == "Todos" else [
            asset for asset in assets if asset["class"] == selected_category
        ]

        # Mostrar los activos filtrados
        st.markdown(f"### Activos en la categoría: {selected_category}")
        st.dataframe(filtered_assets[:10])  # Mostrar los primeros 10 activos como ejemplo

        # Obtener lista de símbolos disponibles
        available_symbols = [
            asset["symbol"] for asset in filtered_assets if asset.get("status") == "active"
        ]

    else:
        st.error(assets.get("error", "No se pudieron cargar los activos desde Alpaca."))

    # Dividir la interfaz en pestañas
    tab1, tab2, tab3 = st.tabs(["Crear Alerta","Alertas Activas", "Configuración"])

    # Tab 1: Crear Alerta
    with tab1:
        st.header("Crear Alerta")
    if available_symbols:
        
        # Selectbox para seleccionar la categoría y el tipo de alerta
        selected_category = st.selectbox("Categoría de alerta:", list(alert_types_by_category.keys()))
        selected_alert_type = st.selectbox("Tipo de alerta:", alert_types_by_category[selected_category])

        # Cargar dinámicamente el archivo correspondiente al tipo de alerta
        alert_module_name = selected_alert_type.lower().replace(" ", "_") + "_alert"
        try:
            # Intentar importar el módulo dinámicamente
            alert_module = importlib.import_module(f"addons.alertsbot.alerts.{alert_module_name}")
            
            # Verificar si el módulo tiene la función render_form
            if hasattr(alert_module, "render_form"):
                alert_module.render_form(available_symbols)  # Llamar a la función principal del módulo
            else:
                st.error(f"El módulo '{alert_module_name}' no tiene una función 'render_form'.")
        except ModuleNotFoundError:
            st.error(f"No se encontró el módulo para el tipo de alerta: {selected_alert_type}")
        except Exception as e:
            st.error(f"Error inesperado al cargar el módulo '{alert_module_name}': {e}")
    
    # Tab 2: Alertas Activas
    with tab2:
        st.header("Alertas Activas")
        st.info("Lista de alertas configuradas.")
        st.dataframe({
            "Nombre": ["Alerta RSI", "Alerta MACD"],
            "Activo": ["BTC/USD", "ETH/USD"],
            "Indicador": ["RSI", "MACD"],
            "Condición": ["Mayor que 70", "Menor que 30"]
        })

    # Tab 3: Configuración
    with tab3:
        st.header("Configuración General")
        st.slider("Intervalo de verificación (segundos)", min_value=10, max_value=300, value=60, step=10)
        st.checkbox("Habilitar notificaciones por email")
        st.checkbox("Habilitar notificaciones por webhook")
        st.button("Guardar Configuración")

        # Probar conexión con Alpaca
        st.subheader("Probar conexión con Alpaca")
        if st.button("Probar conexión"):
            result = alpaca.test_connection()
            if result["status"] == "success":
                st.success(result["message"])
                st.json(result["example_assets"])
            else:
                st.error(result["message"])
