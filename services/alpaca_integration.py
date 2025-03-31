import requests
from config import Config

class AlpacaIntegration:
    def __init__(self):
        # Cargar las credenciales de Alpaca desde el objeto Config.
        self.api_key = Config.ALPACA_API_KEY
        self.api_secret = Config.ALPACA_API_SECRET
        self.base_url = Config.ALPACA_BASE_URL

    def get_account(self):
        """Ejemplo: Obtiene información de la cuenta."""
        endpoint = f"{self.base_url}/v2/account"
        headers = {
            "APCA-API-KEY-ID": self.api_key,
            "APCA-API-SECRET-KEY": self.api_secret
        }
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.text}

    def get_bars(self, symbol, timeframe="1Day", start=None, end=None):
        """Ejemplo: Obtiene barras de precios para un símbolo dado."""
        endpoint = f"{self.base_url}/v2/stocks/{symbol}/bars"
        headers = {
            "APCA-API-KEY-ID": self.api_key,
            "APCA-API-SECRET-KEY": self.api_secret
        }
        params = {"timeframe": timeframe}
        if start:
            params["start"] = start
        if end:
            params["end"] = end
        response = requests.get(endpoint, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.text}
