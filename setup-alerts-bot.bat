@echo off
echo Generando estructura de carpetas para el addon Bot de Alertas...

REM Crear estructura de carpetas
mkdir addons\alertsbot
mkdir addons\alertsbot\src
mkdir addons\alertsbot\ui
mkdir addons\alertsbot\data
mkdir services

REM Crear archivos principales
echo Creando archivo config.json...
echo {> addons\alertsbot\config.json
echo     "name": "Bot de Alertas",>> addons\alertsbot\config.json
echo     "active": true,>> addons\alertsbot\config.json
echo     "version": "1.0.0",>> addons\alertsbot\config.json
echo     "description": "Sistema configurable de alertas para múltiples activos e indicadores técnicos",>> addons\alertsbot\config.json
echo     "author": "DashBotTrade Team",>> addons\alertsbot\config.json
echo     "folder": "alertsbot",>> addons\alertsbot\config.json
echo     "nav_button": {>> addons\alertsbot\config.json
echo         "show": true,>> addons\alertsbot\config.json
echo         "label": "🔔 Bot de Alertas">> addons\alertsbot\config.json
echo     }>> addons\alertsbot\config.json
echo }>> addons\alertsbot\config.json

echo Creando archivo alertsbot.py principal...
echo """>> addons\alertsbot\src\alertsbot.py
echo Addon: Bot de Alertas>> addons\alertsbot\src\alertsbot.py
echo Descripción: Sistema configurable de alertas para múltiples activos e indicadores técnicos>> addons\alertsbot\src\alertsbot.py
echo Versión: 1.0.0>> addons\alertsbot\src\alertsbot.py
echo Autor: DashBotTrade Team>> addons\alertsbot\src\alertsbot.py
echo """>> addons\alertsbot\src\alertsbot.py
echo from services.addons_manager import register_new_addon>> addons\alertsbot\src\alertsbot.py
echo import os>> addons\alertsbot\src\alertsbot.py
echo import sys>> addons\alertsbot\src\alertsbot.py
echo.>> addons\alertsbot\src\alertsbot.py
echo # Aseguramos que el directorio del addon esté en el path>> addons\alertsbot\src\alertsbot.py
echo current_dir = os.path.dirname(os.path.abspath(__file__))>> addons\alertsbot\src\alertsbot.py
echo addon_dir = os.path.dirname(os.path.dirname(current_dir))>> addons\alertsbot\src\alertsbot.py
echo if addon_dir not in sys.path:>> addons\alertsbot\src\alertsbot.py
echo     sys.path.append(addon_dir)>> addons\alertsbot\src\alertsbot.py
echo.>> addons\alertsbot\src\alertsbot.py
echo def alertsbot_view():>> addons\alertsbot\src\alertsbot.py
echo     """>> addons\alertsbot\src\alertsbot.py
echo     Función principal del addon Bot de Alertas.>> addons\alertsbot\src\alertsbot.py
echo     """>> addons\alertsbot\src\alertsbot.py
echo     # Importamos aquí para evitar problemas de importación circular>> addons\alertsbot\src\alertsbot.py
echo     from addons.alertsbot.ui.alertsbot import render_alerts_ui>> addons\alertsbot\src\alertsbot.py
echo     return render_alerts_ui()>> addons\alertsbot\src\alertsbot.py
echo.>> addons\alertsbot\src\alertsbot.py
echo # Registro del addon en el sistema>> addons\alertsbot\src\alertsbot.py
echo register_new_addon(>> addons\alertsbot\src\alertsbot.py
echo     addon_id="alertsbot",>> addons\alertsbot\src\alertsbot.py
echo     name="Bot de Alertas",>> addons\alertsbot\src\alertsbot.py
echo     description="Sistema configurable de alertas para múltiples activos e indicadores técnicos",>> addons\alertsbot\src\alertsbot.py
echo     route="/alertsbot",>> addons\alertsbot\src\alertsbot.py
echo     view_func=alertsbot_view,>> addons\alertsbot\src\alertsbot.py
echo     template="alertsbot.html",>> addons\alertsbot\src\alertsbot.py
echo     icon="bell",>> addons\alertsbot\src\alertsbot.py
echo     version="1.0.0",>> addons\alertsbot\src\alertsbot.py
echo     author="DashBotTrade Team">> addons\alertsbot\src\alertsbot.py
echo )>> addons\alertsbot\src\alertsbot.py

echo Creando otros archivos iniciales...
echo # Este archivo será reemplazado por el código completo> addons\alertsbot\src\alert_manager.py
echo # Este archivo será reemplazado por el código completo> addons\alertsbot\src\indicators.py
echo # Este archivo será reemplazado por el código completo> addons\alertsbot\src\symbols_manager.py
echo # Este archivo será reemplazado por el código completo> addons\alertsbot\ui\alertsbot.py
echo # Este archivo será reemplazado por el código completo> services\alpaca_integration_extended.py

echo Estructura básica creada. Ahora debes reemplazar los archivos con el código completo.
echo.
echo Crea los siguientes archivos manualmente:
echo 1. addons\alertsbot\src\alert_manager.py - Gestor de alertas
echo 2. addons\alertsbot\src\indicators.py - Indicadores técnicos
echo 3. addons\alertsbot\src\symbols_manager.py - Gestor de símbolos
echo 4. addons\alertsbot\ui\alertsbot.py - Interfaz de usuario
echo 5. services\alpaca_integration_extended.py - Extensión de Alpaca
echo.
echo Estructura de directorios creada correctamente!
