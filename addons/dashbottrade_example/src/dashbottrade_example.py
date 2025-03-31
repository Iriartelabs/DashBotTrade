"""
Addon: EjemploAddon
Descripción: Este es un addon de ejemplo para DashBotTrade
"""

from services.addons_manager import register_new_addon

def ejemploaddon_view():
    # Aquí va la lógica del addon
    return "Hola desde EjemploAddon (esto debe devolver una vista renderizada con Streamlit u otro método)"

# Registro del addon en el sistema
register_new_addon(
    addon_id="ejemploaddon",
    name="Ejemplo Addon",
    description="Este es un addon de ejemplo para DashBotTrade.",
    route="/ejemplo-addon",
    view_func=ejemploaddon_view,
    template="ejemploaddon.html",
    icon="cpu",
    version="1.0.0",
    author="Jose"
)
