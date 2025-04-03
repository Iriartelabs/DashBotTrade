import streamlit as st

def render_form(available_symbols):
    """
    Renderiza el formulario para configurar una alerta de cruce de precio.
    """
    st.subheader("Configurar Alerta de Cruce de Precio")

    with st.form("price_crossover_alert_form"):
        col1, col2 = st.columns(2)

        # Parámetros esenciales
        with col1:
            alert_name = st.text_input("Nombre de la alerta", placeholder="Ejemplo: Cruce de Precio")
            selected_symbol = st.selectbox("Símbolo/Activo", available_symbols)
            first_price_line = st.text_input("Primera línea de precio", placeholder="Ejemplo: Media móvil (50)")
            second_price_line = st.text_input("Segunda línea de precio", placeholder="Ejemplo: Precio actual")
            direction = st.selectbox("Dirección del cruce", ["Ascendente", "Descendente"])
        
        with col2:
            time_interval = st.selectbox("Intervalo de tiempo", ["1min", "5min", "15min", "Diario", "Semanal"])

        st.markdown("---")  # Separador visual

        # Parámetros opcionales
        st.subheader("Opciones avanzadas")
        col3, col4 = st.columns(2)

        with col3:
            confirmation_time = st.number_input("Confirmación (segundos)", min_value=0, step=1, value=0)
            volume_filter = st.number_input("Filtro de volumen mínimo", min_value=0, step=1, value=0)

        with col4:
            auto_action = st.selectbox("Acción automática", ["Enviar notificación", "Ejecutar orden automáticamente"])
            activation_schedule = st.selectbox("Horario de activación", ["Horario regular", "Todo el día"])

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
                st.write(f"- Primera línea de precio: {first_price_line}")
                st.write(f"- Segunda línea de precio: {second_price_line}")
                st.write(f"- Dirección del cruce: {direction}")
                st.write(f"- Intervalo de tiempo: {time_interval}")
                st.write(f"- Confirmación: {confirmation_time} segundos")
                st.write(f"- Filtro de volumen: {volume_filter}")
                st.write(f"- Acción automática: {auto_action}")
                st.write(f"- Horario de activación: {activation_schedule}")