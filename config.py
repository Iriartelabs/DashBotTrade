import os
import json

# Configuración base
class Config:
    # Intenta cargar las claves desde alpaca_config.json
    try:
        with open("alpaca_config.json", "r") as f:
            config_data = json.load(f)
            ALPACA_API_KEY = config_data.get("ALPACA_API_KEY", os.getenv("ALPACA_API_KEY", "tu_api_key"))
            ALPACA_API_SECRET = config_data.get("ALPACA_API_SECRET", os.getenv("ALPACA_API_SECRET", "tu_api_secret"))
            ALPACA_BASE_URL = config_data.get("ALPACA_BASE_URL", os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets/v2"))
    except FileNotFoundError:
        # Si el archivo no existe, usa las variables de entorno o valores por defecto
        ALPACA_API_KEY = os.getenv("ALPACA_API_KEY", "tu_api_key")
        ALPACA_API_SECRET = os.getenv("ALPACA_API_SECRET", os.getenv("ALPACA_API_SECRET", "tu_api_secret"))
        ALPACA_BASE_URL = os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets/v2")

# Configuración actual
current_config = Config()