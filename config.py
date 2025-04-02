import os

# Configuración base
class Config:
    ALPACA_API_KEY = os.getenv("ALPACA_API_KEY", "tu_api_key")
    ALPACA_API_SECRET = os.getenv("ALPACA_API_SECRET", "tu_api_secret")
    ALPACA_BASE_URL = os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets/v2")

# Configuración actual
current_config = Config()