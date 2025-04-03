import streamlit as st

def render_form(available_symbols):
    """
    Renderiza el formulario para configurar una alerta de precio fijo.
    """
    st.subheader("Configurar Alerta de Precio Fijo")

    with st.form("fixed_price_alert_form"):
        col1, col2 = st.columns(2)

        # Parámetros esenciales
        with col1:
            alert_name = st.text_input("Nombre de la alerta", placeholder="Ejemplo: Alerta de Precio Fijo")
            selected_symbol = st.selectbox("Símbolo/Activo", available_symbols)
            price_level = st.number_input("Nivel de precio", min_value=0.0, step=0.01, format="%.2f")
            direction = st.selectbox("Dirección", ["Por encima de", "Por debajo de"])
        
        with col2:
            duration = st.selectbox("Duración", ["Un día", "Hasta cancelación"])

        st.markdown("---")  # Separador visual

        # Parámetros opcionales
        st.subheader("Opciones avanzadas")
        col3, col4 = st.columns(2)

        with col3:
            tolerance = st.number_input("Tolerancia (%)", min_value=0.0, max_value=5.0, step=0.01, format="%.2f", value=0.05)
            activation_condition = st.selectbox("Condición de activación", ["Tocar el nivel", "Cerrar más allá del nivel"])

        with col4:
            auto_action = st.selectbox("Acción automática", ["Enviar notificación", "Ejecutar orden automáticamente"])
            frequency = st.selectbox("Frecuencia", ["Una sola vez", "Recurrente"])

        # Botón para crear la alerta
        submitted = st.form_submit_button("Crear Alerta")
        if submitted:
            # Validar entrada
            if not alert_name.strip():
                st.error("El nombre de la alerta no puede estar vacío.")
            else:
                # Mostrar mensaje de éxito
                st.success(f"Alerta '{alert_name}' creada correctamente para el activo {selected_symbol}.")
                st.write("**Detalles de la alerta:**")
                st.write(f"- Nivel de precio: {price_level}")
                st.write(f"- Dirección: {direction}")
                st.write(f"- Duración: {duration}")
                st.write(f"- Tolerancia: ±{tolerance}%")
                st.write(f"- Condición de activación: {activation_condition}")
                st.write(f"- Acción automática: {auto_action}")
                st.write(f"- Frecuencia: {frequency}")