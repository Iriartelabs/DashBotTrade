# addons/alertsbot/ui/alertsbot.py
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import json
import sys

# Importamos los componentes del addon
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
addon_dir = os.path.dirname(parent_dir)
if addon_dir not in sys.path:
    sys.path.append(addon_dir)

from addons.alertsbot.src.alert_manager import AlertManager
from addons.alertsbot.src.symbols_manager import SymbolsManager
from addons.alertsbot.src.indicators import get_available_indicators

# Inicialización de objeto AlertManager
def get_alert_manager():
    if 'alert_manager' not in st.session_state:
        st.session_state.alert_manager = AlertManager()
    return st.session_state.alert_manager

# Inicialización de objeto SymbolsManager
def get_symbols_manager():
    if 'symbols_manager' not in st.session_state:
        st.session_state.symbols_manager = SymbolsManager()
    return st.session_state.symbols_manager

def render_alerts_ui():
    """Renderiza la interfaz principal del bot de alertas"""
    
    st.title("Bot de Alertas - DashBotTrade")
    
    # Inicialización de objetos
    alert_manager = get_alert_manager()
    symbols_manager = get_symbols_manager()
    
    # Pestañas principales
    tab1, tab2, tab3 = st.tabs(["Configurar Alertas", "Alertas Activas", "Configuración"])
    
    # Tab 1: Configurar Alertas
    with tab1:
        st.header("Configuración de Nuevas Alertas")
        
        # Formulario para crear nuevas alertas
        with st.form("nueva_alerta"):
            col1, col2 = st.columns(2)
            
            with col1:
                # Lista de símbolos disponibles
                available_symbols = symbols_manager.get_symbols_list()
                selected_symbol = st.selectbox(
                    "Seleccionar Activo", 
                    options=available_symbols,
                    index=0 if available_symbols else None
                )
                
                # Timeframe
                timeframe = st.selectbox(
                    "Timeframe", 
                    options=["1min", "5min", "15min", "30min", "1hour", "1day"],
                    index=5
                )
                
            with col2:
                # Indicadores disponibles
                indicators = get_available_indicators()
                selected_indicator = st.selectbox("Indicador", options=list(indicators.keys()))
                
                # Condición para la alerta
                condition = st.selectbox(
                    "Condición", 
                    options=["mayor que", "menor que", "cruza por arriba", "cruza por abajo"],
                    index=0
                )
            
            # Parámetros del indicador (dinámicos según el indicador seleccionado)
            st.subheader("Parámetros del Indicador")
            indicator_params = {}
            
            if selected_indicator in indicators:
                for param_name, param_info in indicators[selected_indicator].get("parameters", {}).items():
                    param_type = param_info.get("type", "number")
                    param_default = param_info.get("default", 14)
                    param_min = param_info.get("min", 1)
                    param_max = param_info.get("max", 200)
                    
                    if param_type == "number":
                        indicator_params[param_name] = st.number_input(
                            f"{param_name}", 
                            min_value=param_min,
                            max_value=param_max,
                            value=param_default,
                            step=1
                        )
                    elif param_type == "float":
                        indicator_params[param_name] = st.number_input(
                            f"{param_name}", 
                            min_value=float(param_min),
                            max_value=float(param_max),
                            value=float(param_default),
                            step=0.1
                        )
            
            # Valor umbral para la condición
            threshold_value = st.number_input(
                "Valor Umbral", 
                min_value=0.0,
                value=50.0,
                step=0.1
            )
            
            # Canales de notificación
            st.subheader("Canales de Notificación")
            notify_app = st.checkbox("Notificar en la aplicación", value=True)
            notify_email = st.checkbox("Notificar por email")
            notify_webhook = st.checkbox("Notificar por webhook")
            
            if notify_email:
                email = st.text_input("Email para notificaciones")
            
            if notify_webhook:
                webhook_url = st.text_input("URL del webhook")
            
            # Botón para crear la alerta
            submitted = st.form_submit_button("Crear Alerta")
            
            if submitted:
                # Validaciones
                valid_form = True
                if not selected_symbol:
                    st.error("Debes seleccionar un activo.")
                    valid_form = False
                    
                if notify_email and not email:
                    st.error("Debes proporcionar un email para las notificaciones por email.")
                    valid_form = False
                    
                if notify_webhook and not webhook_url:
                    st.error("Debes proporcionar una URL para el webhook.")
                    valid_form = False
                
                if valid_form:
                    # Crear la alerta
                    notification_channels = {
                        "app": notify_app,
                        "email": email if notify_email else None,
                        "webhook": webhook_url if notify_webhook else None
                    }
                    
                    alert_id = alert_manager.create_alert(
                        symbol=selected_symbol,
                        indicator=selected_indicator,
                        indicator_params=indicator_params,
                        condition=condition,
                        threshold=threshold_value,
                        timeframe=timeframe,
                        notification_channels=notification_channels
                    )
                    
                    st.success(f"¡Alerta creada con éxito! ID: {alert_id}")
    
    # Tab 2: Alertas Activas
    with tab2:
        st.header("Alertas Configuradas")
        
        # Obtener todas las alertas
        alerts = alert_manager.get_all_alerts()
        
        if not alerts:
            st.info("No hay alertas configuradas. Crea tu primera alerta en la pestaña 'Configurar Alertas'.")
        else:
            # Mostrar alertas en una tabla
            alerts_data = []
            for alert_id, alert in alerts.items():
                # Formateamos los datos para mostrar en la tabla
                alert_row = {
                    "ID": alert_id,
                    "Activo": alert["symbol"],
                    "Indicador": alert["indicator"],
                    "Condición": alert["condition"],
                    "Umbral": alert["threshold"],
                    "Timeframe": alert["timeframe"],
                    "Estado": "Activo" if alert["active"] else "Inactivo",
                    "Última Verificación": alert.get("last_check", "Nunca")
                }
                alerts_data.append(alert_row)
            
            # Crear DataFrame y mostrar tabla
            df_alerts = pd.DataFrame(alerts_data)
            st.dataframe(df_alerts, use_container_width=True)
            
            # Acciones en lote para alertas
            st.subheader("Acciones")
            
            # Multi-selector para alertas
            selected_alerts = st.multiselect(
                "Selecciona alertas para realizar acciones", 
                options=list(alerts.keys()),
                format_func=lambda x: f"{x} - {alerts[x]['symbol']} ({alerts[x]['indicator']})"
            )
            
            # Botones de acción
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("Activar Seleccionadas"):
                    if not selected_alerts:
                        st.warning("No hay alertas seleccionadas.")
                    else:
                        for alert_id in selected_alerts:
                            alert_manager.activate_alert(alert_id)
                        st.success("Alertas activadas correctamente.")
            
            with col2:
                if st.button("Desactivar Seleccionadas"):
                    if not selected_alerts:
                        st.warning("No hay alertas seleccionadas.")
                    else:
                        for alert_id in selected_alerts:
                            alert_manager.deactivate_alert(alert_id)
                        st.success("Alertas desactivadas correctamente.")
            
            with col3:
                if st.button("Eliminar Seleccionadas"):
                    if not selected_alerts:
                        st.warning("No hay alertas seleccionadas.")
                    else:
                        for alert_id in selected_alerts:
                            alert_manager.delete_alert(alert_id)
                        st.success("Alertas eliminadas correctamente.")
    
    # Tab 3: Configuración
    with tab3:
        st.header("Configuración del Bot de Alertas")
        
        # Gestión de activos
        st.subheader("Gestión de Activos")
        
        # Mostrar activos actuales
        symbols = symbols_manager.get_symbols_list()
        
        if symbols:
            st.write("Activos configurados:")
            symbols_data = []
            for symbol in symbols:
                symbol_data = symbols_manager.get_symbol_data(symbol)
                symbols_data.append({
                    "Símbolo": symbol,
                    "Nombre": symbol_data.get("name", "N/A"),
                    "Tipo": symbol_data.get("type", "N/A"),
                    "Disponible": "Sí" if symbol_data.get("available", True) else "No"
                })
            
            df_symbols = pd.DataFrame(symbols_data)
            st.dataframe(df_symbols, use_container_width=True)
        
        # Formulario para añadir nuevos activos
        st.subheader("Añadir Nuevo Activo")
        
        with st.form("nuevo_activo"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_symbol = st.text_input("Símbolo (ej: AAPL, BTC/USD)")
                new_symbol_name = st.text_input("Nombre del Activo")
            
            with col2:
                new_symbol_type = st.selectbox(
                    "Tipo de Activo", 
                    options=["stock", "crypto", "forex", "index", "other"],
                    index=0
                )
            
            submitted = st.form_submit_button("Añadir Activo")
            
            if submitted:
                if not new_symbol:
                    st.error("El símbolo no puede estar vacío.")
                elif symbols_manager.symbol_exists(new_symbol):
                    st.error(f"El símbolo {new_symbol} ya existe.")
                else:
                    symbols_manager.add_symbol(
                        symbol=new_symbol, 
                        name=new_symbol_name, 
                        symbol_type=new_symbol_type
                    )
                    st.success(f"Activo {new_symbol} añadido correctamente.")
        
        # Configuración general
        st.subheader("Configuración General")
        
        # Intervalo de verificación de alertas
        check_interval = st.slider(
            "Intervalo de verificación (segundos)", 
            min_value=10,
            max_value=300,
            value=60,
            step=5
        )
        
        # Guardar configuración
        if st.button("Guardar Configuración"):
            alert_manager.update_settings({"check_interval": check_interval})
            st.success("Configuración guardada correctamente.")
        
        # Acción para sincronizar activos con Alpaca
        if st.button("Sincronizar Activos desde Alpaca"):
            with st.spinner("Sincronizando activos desde Alpaca..."):
                try:
                    # Esta función se implementará en symbols_manager.py
                    num_symbols = symbols_manager.sync_symbols_from_alpaca()
                    st.success(f"Sincronización completada. {num_symbols} activos importados/actualizados.")
                except Exception as e:
                    st.error(f"Error durante la sincronización: {str(e)}")
