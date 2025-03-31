"""
Addon: Addon de prueba nuevo
Descripción: Pues eso
Versión: 1.0.0
Autor: Tu Nombre
"""
from addon_system import AddonRegistry, custom_render_template
from flask import redirect, url_for, flash, request

def prueba2_view():
    """
    Función principal del addon Addon de prueba nuevo.
    """
    # Aquí implementa la lógica del addon.
    return custom_render_template(
        'prueba2',
        'prueba2.html'
    )

def register_addon():
    """Registra este addon en el sistema"""
    AddonRegistry.register('prueba2', {
        'name': 'Addon de prueba nuevo',
        'description': 'Pues eso',
        'route': '/prueba2',  # Puedes ajustar la ruta pública si lo deseas
        'view_func': prueba2_view,
        'template': 'prueba2.html',
        'icon': 'chart-bar',  # Cambia el icono según tus preferencias
        'active': True,
        'version': '1.0.0',
        'author': 'Tu Nombre'
    })

if __name__ != '__main__':
    register_addon()
