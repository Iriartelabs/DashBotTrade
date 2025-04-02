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
            list: Lista de símbolos disponibles.
        """
        url = f"{self.base_url}/assets"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            assets = response.json()

            # Filtrar por clase de activo si se especifica
            if asset_class:
                assets = [asset for asset in assets if asset["class"] == asset_class]

            # Retornar solo los símbolos disponibles
            return [asset["symbol"] for asset in assets if asset["status"] == "active"]
        except Exception as e:
            print(f"Error al obtener activos desde Alpaca: {e}")
            return []

    def test_connection(self):
        """
        Prueba la conexión con la API de Alpaca y devuelve un ejemplo de activos.
        
        Returns:
            dict: Respuesta de la API o mensaje de error.
        """
        url = f"{self.base_url}/assets"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            assets = response.json()
            return {
                "status": "success",
                "message": f"Conexión exitosa. Se encontraron {len(assets)} activos.",
                "example_assets": assets[:5]  # Retornar los primeros 5 activos como ejemplo
            }
        except requests.exceptions.HTTPError as e:
            if response.status_code == 403:
                return {
                    "status": "error",
                    "message": "Error 403: Acceso prohibido. Verifica tus claves API y permisos."
                }
            elif response.status_code == 401:
                return {
                    "status": "error",
                    "message": "Error 401: No autorizado. Las claves API son incorrectas."
                }
            else:
                return {
                    "status": "error",
                    "message": f"Error HTTP: {e}"
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error al conectar con Alpaca: {e}"
            }
