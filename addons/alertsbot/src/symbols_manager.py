import requests
import os

class SymbolsManager:
    def __init__(self):
        self.api_key = os.getenv("ALPACA_API_KEY", "")
        self.api_secret = os.getenv("ALPACA_API_SECRET", "")
        self.base_url = os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets/v2")
        self.headers = {
            "APCA-API-KEY-ID": self.api_key,
            "APCA-API-SECRET-KEY": self.api_secret
        }

    def get_symbols_list(self, asset_class=None):
        """
        Obtiene la lista de activos desde Alpaca y los filtra por clase de activo.

        Args:
            asset_class (str): Clase de activo para filtrar (ejemplo: "us_equity", "crypto").

        Returns:
            list: Lista de símbolos disponibles o un mensaje de error.
        """
        url = f"{self.base_url}/assets"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            assets = response.json()

            # Validar que la respuesta sea una lista
            if not isinstance(assets, list):
                print("La respuesta de la API no es válida.")
                return []

            # Filtrar por clase de activo si se especifica
            if asset_class:
                assets = [asset for asset in assets if asset.get("class") == asset_class]

            # Retornar solo los símbolos disponibles
            return [asset["symbol"] for asset in assets if asset.get("status") == "active"]

        except requests.exceptions.HTTPError as e:
            print(f"Error HTTP al obtener activos desde Alpaca: {e}")
            return []
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión al obtener activos desde Alpaca: {e}")
            return []
        except Exception as e:
            print(f"Error inesperado al obtener activos desde Alpaca: {e}")
            return []
