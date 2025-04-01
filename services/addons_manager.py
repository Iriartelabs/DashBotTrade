import os
import json
import importlib.util
import streamlit as st  # Si necesitas usar st.warning; alternativamente, puedes manejar otro sistema de log
import shutil
import zipfile
import io

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
                (opcional: archivos estáticos o recursos)
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

def scan_addons(addons_dir="addons"):
    temp_list = []
    if os.path.exists(addons_dir):
        for folder in os.listdir(addons_dir):
            addon_path = os.path.join(addons_dir, folder)
            if os.path.isdir(addon_path):
                config_path = os.path.join(addons_dir, folder, "config.json")
                if os.path.exists(config_path):
                    try:
                        with open(config_path, "r", encoding="utf-8") as f:
                            config_data = json.load(f)
                    except Exception as e:
                        config_data = {"name": folder, "active": True, "version": "1.0.0", "description": "Sin descripción"}
                else:
                    config_data = {"name": folder, "active": True, "version": "1.0.0", "description": "Sin descripción"}
                config_data["folder"] = folder
                temp_list.append(config_data)
    else:
        st.warning("No existe la carpeta de addons.")
    return temp_list

def refresh_addons(addons_dir="addons"):
    return scan_addons(addons_dir)

def toggle_addons(addon_list, selected, addons_dir="addons"):
    for addon in addon_list:
        if addon["folder"] in selected:
            addon["active"] = not addon.get("active", True)
            config_path = os.path.join(addons_dir, addon["folder"], "config.json")
            try:
                with open(config_path, "w") as f:
                    json.dump(addon, f, indent=4)
            except Exception as e:
                st.error(f"Error al guardar {addon['name']}: {e}")
    st.success("Estado actualizado en los addons seleccionados.")
    return refresh_addons(addons_dir)

def uninstall_addons(addon_list, selected, addons_dir="addons"):
    for addon in addon_list:
        if addon["folder"] in selected:
            try:
                shutil.rmtree(os.path.join(addons_dir, addon["folder"]))
                st.success(f"{addon['name']} desinstalado.")
            except Exception as e:
                st.error(f"Error al desinstalar {addon['name']}: {e}")
    
    return refresh_addons(addons_dir)

def import_addon(uploaded_zip, temp_dir="temp"):
    """
    Importa un addon a partir de un archivo zip subido.
    1. Descomprime el zip en una carpeta temporal.
    2. Busca y lee el config.json del addon.
    3. Registra el addon usando los datos de configuración.
    
    Args:
        uploaded_zip: Archivo subido (Zip) desde st.file_uploader.
        temp_dir (str): Carpeta temporal para extraer el addon.
        
    Returns:
        dict: Datos de configuración del addon o None si falla.
    """
    # Crear carpeta temporal si no existe
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        # Leer el contenido del zip
        with zipfile.ZipFile(io.BytesIO(uploaded_zip.read()), "r") as z:
            # Extraer todo en la carpeta temporal
            z.extractall(temp_dir)
    except Exception as e:
        st.error(f"Error al descomprimir el addon: {e}")
        return None

    # Buscar el archivo config.json en la carpeta extraída
    config_path = None
    for root, dirs, files in os.walk(temp_dir):
        if "config.json" in files:
            config_path = os.path.join(root, "config.json")
            break

    if not config_path:
        st.error("No se encontró el archivo config.json en el addon.")
        return None

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config_data = json.load(f)
    except Exception as e:
        st.error(f"Error al leer config.json: {e}")
        return None

    # Usamos la clave "name" para determinar el nombre de la carpeta
    addon_folder = config_data.get("name")
    if not addon_folder:
        addon_folder = os.path.splitext(uploaded_zip.name)[0]
    else:
        addon_folder = addon_folder.replace(" ", "_").lower()

    destination = os.path.join("addons", addon_folder)
    source = os.path.join(temp_dir, addon_folder)

    try:
        # Si la carpeta extraída existe, muévela
        if os.path.isdir(source):
            if os.path.exists(destination):
                shutil.rmtree(destination)
            shutil.move(source, destination)
        else:
            # Si no existe, se asume que los archivos se extrajeron directamente en temp
            # Creamos el destino y movemos todos los archivos desde temp al destino
            os.makedirs(destination, exist_ok=True)
            for item in os.listdir(temp_dir):
                s = os.path.join(temp_dir, item)
                d = os.path.join(destination, item)
                shutil.move(s, d)
    except Exception as e:
        st.error(f"Error al mover el addon a la carpeta definitiva: {e}")
        return None

    st.success(f"Addon '{config_data.get('name', '')}' importado correctamente.")

    # Trigger: actualizar la lista de addons luego de la importación
    updated_addons = refresh_addons()
    
    # Opcional: podrías devolver ambos, config_data y updated_addons, o simplemente config_data.
    return config_data

if __name__ == "__main__":
    # Ejemplo de uso interactivo
    addon_id = input("Ingrese el ID del addon (ej: bottrader): ").strip()
    name = input("Ingrese el nombre del addon: ").strip()
    description = input("Ingrese la descripción: ").strip()
    result = create_addon(addon_id, name, description)
    print(result)
