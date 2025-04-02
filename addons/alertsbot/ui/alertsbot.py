import streamlit as st
from addons.alertsbot.src.symbols_manager import SymbolsManager
from utils import load_alpaca_assets
from addons.alertsbot.src.symbols_manager import SymbolsManager
from services.alpaca_integration import AlpacaIntegration
alpaca = AlpacaIntegration()
symbols_manager = SymbolsManager()
alpaca = AlpacaIntegration()

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
        categories = list(set(asset["class"] for asset in assets))
        categories.sort()  # Ordenar alfabéticamente

        # Mostrar combobox con las categorías
        selected_category = st.selectbox("Categoría de activo", categories)

        # Filtrar activos por la categoría seleccionada
        filtered_assets = [asset for asset in assets if asset["class"] == selected_category]

        # Mostrar los activos filtrados
        st.markdown(f"### Activos en la categoría: {selected_category}")
        st.dataframe(filtered_assets[:10])  # Mostrar los primeros 10 activos como ejemplo
    else:
        st.error(assets.get("error", "No se pudieron cargar los activos desde Alpaca."))

    # Dividir la interfaz en pestañas
    tab1, tab2, tab3 = st.tabs(["Configurar Alertas", "Alertas Activas", "Configuración"])

    # Tab 1: Configurar Alertas
    with tab1:
        st.header("Configurar Nueva Alerta")

        # Selección de categoría de activos
        asset_class = st.selectbox("Categoría de Activo", ["Todos", "Acciones", "Criptomonedas"], index=0)
        asset_class_map = {
            "Todos": None,
            "Acciones": "us_equity",
            "Criptomonedas": "crypto"
        }
        selected_asset_class = asset_class_map[asset_class]

        # Obtener lista de activos desde Alpaca
        available_symbols = symbols_manager.get_symbols_list(asset_class=selected_asset_class)

        # Mostrar selectbox o mensaje de advertencia
        if available_symbols:
            selected_symbol = st.selectbox("Activo", available_symbols)
        else:
            st.warning("No hay activos disponibles para la categoría seleccionada.")
            selected_symbol = st.selectbox("Activo", available_symbols)

        with st.form("configurar_alerta"):
            col1, col2 = st.columns(2)

            with col1:
                st.text_input("Nombre de la alerta", placeholder="Ejemplo: Alerta RSI")
                st.selectbox("Indicador técnico", ["RSI", "MACD", "Media Móvil", "Bollinger Bands"])

            with col2:
                st.slider("Parámetro del indicador", min_value=1, max_value=100, value=14)
                st.selectbox("Condición", ["Mayor que", "Menor que", "Cruce por arriba", "Cruce por abajo"])
                st.number_input("Valor de referencia", value=50.0)

            submitted = st.form_submit_button("Crear Alerta")
            if submitted:
                st.success(f"Alerta creada correctamente para el activo {selected_symbol}.")

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
