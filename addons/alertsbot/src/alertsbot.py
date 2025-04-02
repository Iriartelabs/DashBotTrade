'''Addon: Bot de Alertas
Descripción: Sistema configurable de alertas para múltiples activos e indicadores técnicos
Versión: 1.0.0
Autor: DashBotTrade Team'
'''
from services.addons_manager import register_new_addon
import os
import sys

# Aseguramos que el directorio del addon esté en el path
current_dir = os.path.dirname(os.path.abspath(__file__))
addon_dir = os.path.dirname(os.path.dirname(current_dir))
if addon_dir not in sys.path:
    sys.path.append(addon_dir)

def alertsbot_view():
    #Función principal del addon Bot de Alertas.
    # Importamos aquí para evitar problemas de importación circular
    from addons.alertsbot.ui.alertsbot import render_alerts_ui
    return render_alerts_ui()

# Registro del addon en el sistema
register_new_addon(
    addon_id="alertsbot",
    name="Bot de Alertas",
    description="Sistema configurable de alertas para múltiples activos e indicadores técnicos",
    route="/alertsbot",
    view_func=alertsbot_view,
    template="alertsbot.html",
    icon="bell",
    version="1.0.0",
    author="DashBotTrade Team"
)
