# Bot de Alertas para DashBotTrade

## Descripción
El Bot de Alertas es un addon para DashBotTrade que permite configurar y gestionar alertas basadas en indicadores técnicos para múltiples activos financieros. El bot monitorea continuamente los mercados en busca de condiciones específicas definidas por el usuario y notifica cuando estas condiciones se cumplen.

## Características principales

### Configuración de alertas
- **Selección de activos**: Stocks, criptomonedas, forex, etc.
- **Múltiples indicadores técnicos**: RSI, MACD, Medias Móviles, Bollinger Bands, etc.
- **Condiciones personalizables**: Mayor que, menor que, cruce por arriba, cruce por abajo
- **Parámetros ajustables**: Cada indicador permite ajustar sus parámetros (períodos, desviaciones, etc.)
- **Timeframes flexibles**: Desde 1 minuto hasta 1 día

### Notificaciones
- **En la aplicación**: Notificaciones visibles en la interfaz
- **Email**: Alertas por correo electrónico
- **Webhook**: Integración con servicios externos mediante webhooks

### Gestión de activos
- **Importación automática** desde Alpaca Markets
- **Gestión manual** de activos a monitorear
- **Soporte para múltiples tipos** de activos

## Instalación

### Requisitos previos
- DashBotTrade instalado y configurado
- Credenciales de API de Alpaca Markets

### Procedimiento de instalación
1. Asegúrate de que la carpeta `addons` existe en la raíz de DashBotTrade
2. Copia la carpeta `alertsbot` dentro de la carpeta `addons`
3. Reinicia la aplicación DashBotTrade

## Uso

### Configurar una nueva alerta
1. Navega a la pestaña "Bot de Alertas" en el menú principal
2. Selecciona "Configurar Alertas"
3. Elige el activo, indicador, condición y parámetros
4. Configura los canales de notificación
5. Haz clic en "Crear Alerta"

### Gestionar alertas existentes
1. Navega a la pestaña "Alertas Activas"
2. Visualiza todas tus alertas configuradas
3. Selecciona una o varias alertas para activar, desactivar o eliminar

### Configuración general
1. Navega a la pestaña "Configuración"
2. Ajusta el intervalo de verificación de alertas
3. Gestiona los activos disponibles
4. Configura los métodos de notificación

## Arquitectura del addon

### Estructura de archivos
```
alertsbot/
  ├── config.json
  ├── src/
  │   ├── alertsbot.py
  │   ├── alert_manager.py
  │   ├── indicators.py
  │   └── symbols_manager.py
  ├── ui/
  │   └── alertsbot.py
  └── data/
      ├── alerts.json
      ├── symbols.json
      └── settings.json
```

### Componentes principales
- **alert_manager.py**: Gestor de alertas (crear, modificar, eliminar, verificar)
- **indicators.py**: Implementación de indicadores técnicos
- **symbols_manager.py**: Gestión de activos y obtención de datos de mercado
- **alertsbot.py (ui)**: Interfaz de usuario con Streamlit

## Contribución
Si deseas contribuir a este addon, puedes:
1. Implementar nuevos indicadores técnicos
2. Mejorar los métodos de notificación
3. Optimizar el rendimiento en la verificación de alertas
4. Añadir visualizaciones para los indicadores

## Roadmap
- **Versión 1.1**: Añadir visualización de gráficos para cada indicador
- **Versión 1.2**: Implementar backtesting de alertas
- **Versión 1.3**: Integración con el Bot de Trading para ejecución automática
- **Versión 2.0**: Alertas basadas en patrones de velas y formaciones de precio

## Licencia
Este addon es parte del proyecto DashBotTrade y está sujeto a sus términos de licencia.

## Soporte
Para obtener ayuda con este addon, contacta al equipo de desarrollo o consulta la documentación oficial de DashBotTrade.
