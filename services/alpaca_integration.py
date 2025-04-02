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

    def test_connection(self):
        """
        Prueba la conexión con la API de Alpaca y devuelve un ejemplo de activos.
        
        Returns:
            dict: Respuesta de la API o mensaje de error.
        """
        url = f"{self.base_url}/assets"
        try:
            response = requests.get(url, headers={
                "APCA-API-KEY-ID": self.api_key,
                "APCA-API-SECRET-KEY": self.api_secret
            })
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

    def get_assets(self):
        """
        Obtiene la lista de activos disponibles desde la API de Alpaca.
        Returns:
            list: Lista de activos o un mensaje de error.
        """
        url = f"{self.base_url}/assets"
        try:
            response = requests.get(url, headers={
                "APCA-API-KEY-ID": self.api_key,
                "APCA-API-SECRET-KEY": self.api_secret
            })
            response.raise_for_status()
            return response.json()  # Devuelve la lista de activos
        except requests.exceptions.RequestException as e:
            return {"error": f"Error al obtener activos: {e}"}
