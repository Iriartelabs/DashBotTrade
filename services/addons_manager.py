import os
import json
import importlib.util

REGISTERED_ADDONS = {}

def create_addon(addon_id, name, description, version="1.0.0", author="Tu Nombre"):
    """
    Crea la estructura básica de un nuevo addon.

    La estructura resultante será:
    addons/
        addon_id/
            src/
                addon_id.py
            ui/
                addon_id.html
            config.json

    Parámetros:
        addon_id (str): Identificador único del addon (en minúsculas, con guiones bajos si es necesario)
        name (str): Nombre para mostrar del addon.
        description (str): Descripción del addon.
        version (str): Versión inicial (por defecto "1.0.0").
        author (str): Autor del addon.
    """
    base_dir = os.path.join("addons", addon_id)
    src_dir = os.path.join(base_dir, "src")
    ui_dir = os.path.join(base_dir, "ui")

    # Crear la estructura de carpetas
    os.makedirs(src_dir, exist_ok=True)
    os.makedirs(ui_dir, exist_ok=True)

    # Crear el archivo Python en src: addon_id.py
    py_file_path = os.path.join(src_dir, f"{addon_id}.py")
    if not os.path.exists(py_file_path):
        py_content = f'''"""
Addon: {name}
Descripción: {description}
Versión: {version}
Autor: {author}
"""
from addon_system import AddonRegistry, custom_render_template
from flask import redirect, url_for, flash, request

def {addon_id}_view():
    """
    Función principal del addon {name}.
    """
    # Aquí implementa la lógica del addon.
    return custom_render_template(
        '{addon_id}',
        '{addon_id}.html'
    )

def register_addon():
    """Registra este addon en el sistema"""
    AddonRegistry.register('{addon_id}', {{
        'name': '{name}',
        'description': '{description}',
        'route': '/{addon_id}',  # Puedes ajustar la ruta pública si lo deseas
        'view_func': {addon_id}_view,
        'template': '{addon_id}.html',
        'icon': 'chart-bar',  # Cambia el icono según tus preferencias
        'active': True,
        'version': '{version}',
        'author': '{author}'
    }})

if __name__ != '__main__':
    register_addon()
'''
        with open(py_file_path, "w", encoding="utf-8") as f:
            f.write(py_content)

    # Crear la plantilla HTML en ui: addon_id.html
    html_file_path = os.path.join(ui_dir, f"{addon_id}.html")
    if not os.path.exists(html_file_path):
        html_content = f'''{{% extends 'base.html' %}}

{{% block title %}}{name} - DashBotTrade{{% endblock %}}

{{% block header %}}{name}{{% endblock %}}

{{% block content %}}
<div class="row">
    <div class="col-md-12 mb-4">
        <div class="card shadow">
            <div class="card-header py-3">
                <h6 class="m-0 font-weight-bold text-primary">{name}</h6>
            </div>
            <div class="card-body">
                <p>{description}</p>
                <!-- Agrega aquí el contenido personalizado de tu addon -->
            </div>
        </div>
    </div>
</div>
{{% endblock %}}
'''
        with open(html_file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

    # Crear un archivo de configuración (config.json) con los metadatos del addon
    config_path = os.path.join(base_dir, "config.json")
    config_data = {
        "name": name,
        "active": True,
        "version": version,
        "description": description,
        "author": author
    }
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=4)

    return f"Addon '{name}' creado en: {base_dir}"

def register_new_addon(addon_id, name, description, route, view_func, template, icon="chart-bar", version="1.0.0", author="Desconocido", active=True):
    """
    Registra un addon en el sistema DashBotTrade.

    Este registro se guarda en un diccionario en memoria y lo puede consultar la app principal.
    """
    REGISTERED_ADDONS[addon_id] = {
        "name": name,
        "description": description,
        "route": route,
        "view_func": view_func,
        "template": template,
        "icon": icon,
        "active": active,
        "version": version,
        "author": author
    }

def get_all_addons():
    """
    Devuelve el diccionario completo de addons registrados.
    """
    return REGISTERED_ADDONS

def load_addons_from_directory(addons_dir="addons"):
    """
    Escanea todos los addons en la carpeta 'addons' y ejecuta su archivo .py principal.
    Espera que cada addon tenga la siguiente estructura:

    addons/
        nombre_addon/
            src/
                nombre_addon.py
            ui/
                nombre_addon.html
            config.json
    """
    if not os.path.exists(addons_dir):
        print(f"[INFO] No existe la carpeta '{addons_dir}'.")
        return

    for folder in os.listdir(addons_dir):
        addon_path = os.path.join(addons_dir, folder)
        src_path = os.path.join(addon_path, "src", f"{folder}.py")
        if os.path.isfile(src_path):
            try:
                spec = importlib.util.spec_from_file_location(folder, src_path)
                addon_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(addon_module)
                print(f"[OK] Addon cargado: {folder}")
            except Exception as e:
                print(f"[ERROR] Falló la carga del addon '{folder}': {e}")

if __name__ == "__main__":
    # Ejemplo de uso interactivo
    addon_id = input("Ingrese el ID del addon (ej: bottrader): ").strip()
    name = input("Ingrese el nombre del addon: ").strip()
    description = input("Ingrese la descripción: ").strip()
    result = create_addon(addon_id, name, description)
    print(result)
