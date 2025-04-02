# addons/alertsbot/src/symbols_manager.py
import os
import json
from datetime import datetime
import pandas as pd
import sys

# Verificar si el módulo está disponible
try:
    from services.alpaca_integration_extended import AlpacaExtended
except ImportError:
    # Si no, usar la clase base
    from services.alpaca_integration import AlpacaIntegration

class SymbolsManager:
    """
    Gestor para administrar los símbolos de activos (stocks, crypto, forex, etc.)
    """
    
    def __init__(self, symbols_file=None):
        """
        Inicializa el gestor de símbolos.
        
        Args:
            symbols_file (str, optional): Ruta al archivo JSON con los símbolos.
                Si no se proporciona, se usará una ruta predeterminada.
        """
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Definir ruta al archivo de símbolos
        if symbols_file is None:
            self.symbols_file = os.path.join(self.base_dir, "data", "symbols.json")
        else:
            self.symbols_file = symbols_file
        
        # Crear directorio de datos si no existe
        os.makedirs(os.path.dirname(self.symbols_file), exist_ok=True)
        
        # Cargar símbolos
        self.symbols = self._load_symbols()
        
        # Inicializar integración con Alpaca (preferentemente la versión extendida)
        try:
            self.alpaca = AlpacaExtended()
        except NameError:
            self.alpaca = AlpacaIntegration()
    
    def _load_symbols(self):
        """
        Carga los símbolos desde el archivo JSON.
        
        Returns:
            dict: Diccionario con los símbolos cargados.
        """
        if os.path.exists(self.symbols_file):
            try:
                with open(self.symbols_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error al cargar símbolos: {e}")
                return {}
        else:
            # Añadir algunos símbolos por defecto
            default_symbols = {
                "AAPL": {
                    "name": "Apple Inc.",
                    "type": "stock",
                    "exchange": "NASDAQ",
                    "available": True,
                    "added_at": datetime.now().isoformat()
                },
                "MSFT": {
                    "name": "Microsoft Corporation",
                    "type": "stock",
                    "exchange": "NASDAQ",
                    "available": True,
                    "added_at": datetime.now().isoformat()
                },
                "AMZN": {
                    "name": "Amazon.com Inc.",
                    "type": "stock",
                    "exchange": "NASDAQ",
                    "available": True,
                    "added_at": datetime.now().isoformat()
                },
                "GOOGL": {
                    "name": "Alphabet Inc.",
                    "type": "stock",
                    "exchange": "NASDAQ",
                    "available": True,
                    "added_at": datetime.now().isoformat()
                },
                "BTC/USD": {
                    "name": "Bitcoin / US Dollar",
                    "type": "crypto",
                    "exchange": "Various",
                    "available": True,
                    "added_at": datetime.now().isoformat()
                },
                "ETH/USD": {
                    "name": "Ethereum / US Dollar",
                    "type": "crypto",
                    "exchange": "Various",
                    "available": True,
                    "added_at": datetime.now().isoformat()
                }
            }
            
            # Guardar símbolos por defecto
            self._save_symbols(default_symbols)
            
            return default_symbols
    
    def _save_symbols(self, symbols_dict=None):
        """
        Guarda los símbolos en el archivo JSON.
        
        Args:
            symbols_dict (dict, optional): Diccionario con los símbolos a guardar.
                Si no se proporciona, se usará self.symbols.
        
        Returns:
            bool: True si la operación fue exitosa, False en caso contrario.
        """
        if symbols_dict is None:
            symbols_dict = self.symbols
        
        try:
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(self.symbols_file), exist_ok=True)
            
            with open(self.symbols_file, 'w') as f:
                json.dump(symbols_dict, f, indent=4)
            return True
        except Exception as e:
            print(f"Error al guardar símbolos: {e}")
            return False
    
    def get_symbols_list(self):
        """
        Obtiene la lista de símbolos disponibles.
        
        Returns:
            list: Lista de símbolos disponibles.
        """
        # Filtrar símbolos disponibles
        available_symbols = [
            symbol for symbol, data in self.symbols.items()
            if data.get("available", True)
        ]
        
        return available_symbols
    
    def get_symbol_data(self, symbol):
        """
        Obtiene los datos de un símbolo específico.
        
        Args:
            symbol (str): Símbolo a consultar.
        
        Returns:
            dict: Datos del símbolo o None si no existe.
        """
        return self.symbols.get(symbol)
    
    def symbol_exists(self, symbol):
        """
        Verifica si un símbolo existe en el gestor.
        
        Args:
            symbol (str): Símbolo a verificar.
        
        Returns:
            bool: True si el símbolo existe, False en caso contrario.
        """
        return symbol in self.symbols
    
    def add_symbol(self, symbol, name=None, symbol_type="stock", exchange=None):
        """
        Añade un nuevo símbolo al gestor.
        
        Args:
            symbol (str): Símbolo a añadir.
            name (str, optional): Nombre del activo.
            symbol_type (str, optional): Tipo de activo (stock, crypto, forex, etc.).
            exchange (str, optional): Mercado o exchange.
        
        Returns:
            bool: True si la operación fue exitosa, False en caso contrario.
        """
        if self.symbol_exists(symbol):
            return False
        
        # Crear datos del símbolo
        self.symbols[symbol] = {
            "name": name or symbol,
            "type": symbol_type,
            "exchange": exchange or "Unknown",
            "available": True,
            "added_at": datetime.now().isoformat()
        }
        
        # Guardar cambios
        return self._save_symbols()
    
    def update_symbol(self, symbol, **kwargs):
        """
        Actualiza los datos de un símbolo existente.
        
        Args:
            symbol (str): Símbolo a actualizar.
            **kwargs: Pares clave-valor con los campos a actualizar.
        
        Returns:
            bool: True si la operación fue exitosa, False en caso contrario.
        """
        if not self.symbol_exists(symbol):
            return False
        
        # Actualizar los campos proporcionados
        for key, value in kwargs.items():
            self.symbols[symbol][key] = value
        
        # Guardar cambios
        return self._save_symbols()
    
    def delete_symbol(self, symbol):
        """
        Elimina un símbolo del gestor.
        
        Args:
            symbol (str): Símbolo a eliminar.
        
        Returns:
            bool: True si la operación fue exitosa, False en caso contrario.
        """
        if not self.symbol_exists(symbol):
            return False
        
        # Eliminar símbolo
        del self.symbols[symbol]
        
        # Guardar cambios
        return self._save_symbols()
    
    def enable_symbol(self, symbol):
        """
        Habilita un símbolo.
        
        Args:
            symbol (str): Símbolo a habilitar.
        
        Returns:
            bool: True si la operación fue exitosa, False en caso contrario.
        """
        return self.update_symbol(symbol, available=True)
    
    def disable_symbol(self, symbol):
        """
        Deshabilita un símbolo.
        
        Args:
            symbol (str): Símbolo a deshabilitar.
        
        Returns:
            bool: True si la operación fue exitosa, False en caso contrario.
        """
        return self.update_symbol(symbol, available=False)
    
 Alpaca
            symbol_type = self.symbols.get(symbol, {}).get("type", "stock")
            
            if symbol_type == "crypto":
                # Formato especial para criptomonedas en Alpaca
                # Convertir BTC/USD a BTC-USD si es necesario
                alpaca_symbol = symbol.replace("/", "-")
                data = self.alpaca.get_crypto_bars(alpaca_symbol, timeframe)
            else:
                # Stocks y otros activos
                data = self.alpaca.get_bars(symbol, timeframe)
            
            return data
        except Exception as e:
            return {"error": str(e)}
    
    def sync_symbols_from_alpaca(self):
        """
        Sincroniza la lista de símbolos con los disponibles en Alpaca.
        
        Returns:
            int: Número de símbolos importados/actualizados.
        """
        try:
            # Obtener lista de activos de Alpaca
            assets = self.alpaca.get_assets()
            
            if isinstance(assets, dict) and "error" in assets:
                raise Exception(assets["error"])
            
            count = 0
            
            for asset in assets:
                symbol = asset.get("symbol")
                
                if symbol:
                    # Verificar si el símbolo ya existe
                    if self.symbol_exists(symbol):
                        # Actualizar datos
                        self.update_symbol(
                            symbol,
                            name=asset.get("name") or symbol,
                            type=asset.get("class", "stock").lower(),
                            exchange=asset.get("exchange", "Unknown"),
                            tradable=asset.get("tradable", True)
                        )
                    else:
                        # Añadir nuevo símbolo
                        self.add_symbol(
                            symbol,
                            name=asset.get("name") or symbol,
                            symbol_type=asset.get("class", "stock").lower(),
                            exchange=asset.get("exchange", "Unknown")
                        )
                    
                    count += 1
            
            # Si tenemos acceso a la versión extendida de Alpaca, obtener también criptomonedas
            if hasattr(self.alpaca, 'get_crypto_assets'):
                try:
                    crypto_assets = self.alpaca.get_crypto_assets()
                    
                    if isinstance(crypto_assets, dict) and "error" in crypto_assets:
                        print(f"Error al obtener criptomonedas: {crypto_assets['error']}")
                    else:
                        for asset in crypto_assets:
                            # Para criptomonedas, usamos formato de pares como "BTC/USD"
                            symbol = asset.get("symbol")
                            base = asset.get("base_currency", "")
                            quote = asset.get("quote_currency", "")
                            
                            if base and quote:
                                crypto_symbol = f"{base}/{quote}"
                                
                                if self.symbol_exists(crypto_symbol):
                                    # Actualizar datos
                                    self.update_symbol(
                                        crypto_symbol,
                                        name=f"{base}/{quote}",
                                        type="crypto",
                                        exchange="Alpaca",
                                        tradable=asset.get("tradable", True)
                                    )
                                else:
                                    # Añadir nuevo símbolo
                                    self.add_symbol(
                                        crypto_symbol,
                                        name=f"{base}/{quote}",
                                        symbol_type="crypto",
                                        exchange="Alpaca"
                                    )
                                
                                count += 1
                except Exception as crypto_error:
                    print(f"Error al sincronizar criptomonedas: {crypto_error}")
            
            return count
        except Exception as e:
            print(f"Error al sincronizar símbolos desde Alpaca: {e}")
            raise
    
    def get_latest_price(self, symbol):
        """
        Obtiene el precio más reciente para un símbolo.
        
        Args:
            symbol (str): Símbolo a consultar.
        
        Returns:
            float: Precio más reciente o None si hay error.
        """
        try:
            # Verificar si tenemos acceso a la versión extendida de Alpaca
            if hasattr(self.alpaca, 'get_latest_quote'):
                # Obtener datos de la última cotización
                quote = self.alpaca.get_latest_quote(symbol)
                
                if isinstance(quote, dict) and "error" not in quote:
                    # Para criptomonedas, la estructura puede ser diferente
                    if "ask_price" in quote:
                        return (float(quote["ask_price"]) + float(quote["bid_price"])) / 2
                    elif "quote" in quote:
                        return (float(quote["quote"]["ap"]) + float(quote["quote"]["bp"])) / 2
            
            # Fallback: obtener los últimos datos de precio
            market_data = self.get_price_data(symbol, limit=1)
            
            if isinstance(market_data, pd.DataFrame) and not market_data.empty:
                return market_data["close"].iloc[-1]
            elif isinstance(market_data, dict) and "bars" in market_data and market_data["bars"]:
                return float(market_data["bars"][-1]["c"])
            
            return None
        except Exception as e:
            print(f"Error al obtener precio reciente para {symbol}: {e}")
            return None
    
    def get_multiple_prices(self, symbols):
        """
        Obtiene precios recientes para múltiples símbolos.
        
        Args:
            symbols (list): Lista de símbolos a consultar.
        
        Returns:
            dict: Diccionario con símbolos y sus precios.
        """
        result = {}
        
        # Verificar si tenemos acceso a la versión extendida de Alpaca
        if hasattr(self.alpaca, 'get_market_snapshot'):
            try:
                # Obtener snapshot del mercado para múltiples símbolos
                snapshot = self.alpaca.get_market_snapshot(symbols)
                
                if isinstance(snapshot, dict) and "error" not in snapshot:
                    for symbol, data in snapshot.items():
                        # Extraer precio según la estructura
                        if "latestTrade" in data:
                            result[symbol] = float(data["latestTrade"]["p"])
                        elif "minuteBar" in data:
                            result[symbol] = float(data["minuteBar"]["c"])
                        elif "dailyBar" in data:
                            result[symbol] = float(data["dailyBar"]["c"])
                
                # Si obtuvimos todos los precios, retornar
                if len(result) == len(symbols):
                    return result
            except Exception as e:
                print(f"Error en snapshot de mercado: {e}")
        
        # Fallback: obtener precios individualmente
        for symbol in symbols:
            price = self.get_latest_price(symbol)
            if price is not None:
                result[symbol] = price
        
        return result
