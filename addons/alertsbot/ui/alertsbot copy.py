import streamlit as st
from addons.alertsbot.src.symbols_manager import SymbolsManager
from services.alpaca_integration import AlpacaIntegration

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
        
        #Diccionario realizado por Claude
        alert_types_by_category = {
    "Precio": [
        "Cruce de Precio", 
        "Alerta de Precio Fijo",
        "Ruptura de Soporte/Resistencia",
        "Máximos/Mínimos del Día",
        "Cambio Porcentual desde Apertura"
    ],
    "Volumen": [
        "Cruce de Volumen", 
        "Volumen Anómalo",
        "Picos Repentinos",
        "Acumulación/Distribución"
    ],
    "Indicadores Técnicos": [
        "Cruce de RSI", 
        "Cruce de MACD", 
        "Cruce de Medias Móviles",
        "Estrechamiento de Bollinger",
        "Patrones de Velas",
        "Divergencias"
    ],
    "Momentum": [
        "Momentum Positivo", 
        "Momentum Negativo",
        "Cambio de Tendencia Intradiaria",
        "Movimiento Direccional Fuerte"
    ],
    "Riesgo": [
        "Alerta de Riesgo Alto", 
        "Alerta de Riesgo Bajo",
        "Proximidad a Stop Loss",
        "Proximidad a Take Profit",
        "Drawdown Diario Crítico",
        "Exposición Sectorial Excesiva"
    ],
    "Mercado": [
        "Correlación Positiva", 
        "Correlación Negativa",
        "Cambio de Dirección en Índices",
        "Próximos Anuncios Económicos",
        "Noticias Relevantes"
    ]
}
        
        
        """ # Diccionario que mapea categorías a tipos de alertas
        alert_types_by_category = {
            "Precio": ["Cruce de Precio", "Alerta de Precio Fijo"],
            "Volumen": ["Cruce de Volumen", "Volumen Anómalo"],
            "Indicadores Técnicos": ["Cruce de RSI", "Cruce de MACD", "Cruce de Medias Móviles"],
            "Momentum": ["Momentum Positivo", "Momentum Negativo"],
            "Riesgo": ["Alerta de Riesgo Alto", "Alerta de Riesgo Bajo"],
            "Mercado": ["Correlación Positiva", "Correlación Negativa"]
        } """

        # Crear columnas para organizar los selectboxes
        col1, col2 = st.columns(2)

        with col1:
            # Selectbox para seleccionar la categoría
            selected_category = st.selectbox(
                "Categoría de alerta:",
                list(alert_types_by_category.keys())  # Las claves del diccionario son las categorías
            )

        with col2:
            # Obtener los tipos correspondientes a la categoría seleccionada
            types_for_category = alert_types_by_category.get(selected_category, [])
            
            # Selectbox para seleccionar el tipo de alerta
            selected_alert_type = st.selectbox(
                "Tipo de alerta:",
                types_for_category
            )

        # # Mostrar la selección actual
        # st.markdown(f"### Selección actual:")
        # st.write(f"Categoría seleccionada: {selected_category}")
        # st.write(f"Tipo de alerta seleccionado: {selected_alert_type}")

        """ # Formulario para configurar una nueva alerta
        with st.form("configurar_alerta"):
            
            col1, col2 = st.columns(2)

            with col1:
                alert_name = st.text_input("Nombre de la alerta", placeholder="Ejemplo: Alerta RSI")
                selected_symbol = st.selectbox("Activo", available_symbols)
                indicator = st.selectbox("Indicador técnico", ["RSI", "MACD", "Media Móvil", "Bollinger Bands"])


            with col2:
                parameter = st.slider("Parámetro del indicador", min_value=1, max_value=100, value=14)
                condition = st.selectbox("Condición", ["Mayor que", "Menor que", "Cruce por arriba", "Cruce por abajo"])
                reference_value = st.number_input("Valor de referencia", value=50.0)

            # Botón para enviar el formulario
            submitted = st.form_submit_button("Crear Alerta")
            if submitted:
                st.success(f"Alerta '{alert_name}' creada correctamente para el activo {selected_symbol} con el indicador {indicator}.")
    else:
        st.warning("No hay activos disponibles para la categoría seleccionada.") """
    
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
