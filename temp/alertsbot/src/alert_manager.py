# addons/alertsbot/src/alert_manager.py
import os
import json
import uuid
from datetime import datetime, timedelta
import threading
import time

class AlertManager:
    """
    Gestor para crear, modificar, eliminar y verificar alertas.
    """
    
    def __init__(self, alerts_file=None):
        """
        Inicializa el gestor de alertas.
        
        Args:
            alerts_file (str, optional): Ruta al archivo JSON con las alertas.
                Si no se proporciona, se usará una ruta predeterminada.
        """
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Definir ruta al archivo de alertas
        if alerts_file is None:
            self.alerts_file = os.path.join(self.base_dir, "data", "alerts.json")
        else:
            self.alerts_file = alerts_file
        
        # Definir ruta al archivo de configuración
        self.settings_file = os.path.join(self.base_dir, "data", "settings.json")
        
        # Crear directorio de datos si no existe
        os.makedirs(os.path.dirname(self.alerts_file), exist_ok=True)
        
        # Cargar alertas
        self.alerts = self._load_alerts()
        
        # Cargar configuración
        self.settings = self._load_settings()
        
        # Iniciar thread de verificación si está habilitado
        self.check_thread = None
        self.stop_checking = threading.Event()
        
        if self.settings.get("auto_check", True):
            self.start_checking()
    
    def _load_alerts(self):
        """Carga las alertas desde el archivo JSON."""
        if os.path.exists(self.alerts_file):
            try:
                with open(self.alerts_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error al cargar alertas: {e}")
                return {}
        else:
            return {}
    
    def _save_alerts(self):
        """Guarda las alertas en el archivo JSON."""
        try:
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(self.alerts_file), exist_ok=True)
            
            with open(self.alerts_file, 'w') as f:
                json.dump(self.alerts, f, indent=4)
            return True
        except Exception as e:
            print(f"Error al guardar alertas: {e}")
            return False
    
    def _load_settings(self):
        """Carga la configuración desde el archivo JSON."""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error al cargar configuración: {e}")
                return self._get_default_settings()
        else:
            return self._get_default_settings()
    
    def _save_settings(self):
        """Guarda la configuración en el archivo JSON."""
        try:
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
            
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
            return True
        except Exception as e:
            print(f"Error al guardar configuración: {e}")
            return False
    
    def _get_default_settings(self):
        """Devuelve la configuración predeterminada."""
        return {
            "check_interval": 60,  # Intervalo de verificación en segundos
            "auto_check": True,    # Verificación automática habilitada
            "notification_settings": {
                "email": {
                    "enabled": False,
                    "smtp_server": "",
                    "smtp_port": 587,
                    "username": "",
                    "password": "",
                    "from_email": ""
                },
                "webhook": {
                    "enabled": False,
                    "default_url": ""
                }
            }
        }
    
    def create_alert(self, symbol, indicator, indicator_params, condition, threshold, 
                    timeframe="1day", notification_channels=None):
        """
        Crea una nueva alerta.
        
        Args:
            symbol (str): Símbolo del activo (ej: AAPL, BTC/USD).
            indicator (str): Nombre del indicador (ej: "RSI", "MACD").
            indicator_params (dict): Parámetros del indicador.
            condition (str): Condición para la alerta (ej: "mayor que", "cruza por arriba").
            threshold (float): Valor umbral para la condición.
            timeframe (str, optional): Marco temporal para los datos. Por defecto "1day".
            notification_channels (dict, optional): Canales de notificación.
        
        Returns:
            str: ID de la alerta creada.
        """
        # Generar ID único para la alerta
        alert_id = str(uuid.uuid4())
        
        # Estructura de la alerta
        alert = {
            "symbol": symbol,
            "indicator": indicator,
            "indicator_params": indicator_params,
            "condition": condition,
            "threshold": threshold,
            "timeframe": timeframe,
            "notification_channels": notification_channels or {"app": True},
            "active": True,
            "created_at": datetime.now().isoformat(),
            "triggered": False,
            "last_trigger": None,
            "last_check": None,
            "last_value": None
        }
        
        # Añadir alerta al diccionario
        self.alerts[alert_id] = alert
        
        # Guardar cambios
        self._save_alerts()
        
        return alert_id
    
    def update_alert(self, alert_id, **kwargs):
        """
        Actualiza una alerta existente.
        
        Args:
            alert_id (str): ID de la alerta a actualizar.
            **kwargs: Pares clave-valor con los campos a actualizar.
        
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        if alert_id not in self.alerts:
            return False
        
        # Actualizar los campos proporcionados
        for key, value in kwargs.items():
            if key in self.alerts[alert_id]:
                self.alerts[alert_id][key] = value
        
        # Guardar cambios
        self._save_alerts()
        
        return True
    
    def delete_alert(self, alert_id):
        """
        Elimina una alerta.
        
        Args:
            alert_id (str): ID de la alerta a eliminar.
        
        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        if alert_id not in self.alerts:
            return False
        
        # Eliminar alerta
        del self.alerts[alert_id]
        
        # Guardar cambios
        self._save_alerts()
        
        return True
    
    def get_alert(self, alert_id):
        """
        Obtiene una alerta por su ID.
        
        Args:
            alert_id (str): ID de la alerta.
        
        Returns:
            dict: Datos de la alerta o None si no existe.
        """
        return self.alerts.get(alert_id)
    
    def get_all_alerts(self):
        """
        Obtiene todas las alertas.
        
        Returns:
            dict: Diccionario con todas las alertas.
        """
        return self.alerts
    
    def activate_alert(self, alert_id):
        """
        Activa una alerta.
        
        Args:
            alert_id (str): ID de la alerta.
        
        Returns:
            bool: True si la activación fue exitosa, False en caso contrario.
        """
        if alert_id not in self.alerts:
            return False
        
        self.alerts[alert_id]["active"] = True
        self._save_alerts()
        
        return True
    
    def deactivate_alert(self, alert_id):
        """
        Desactiva una alerta.
        
        Args:
            alert_id (str): ID de la alerta.
        
        Returns:
            bool: True si la desactivación fue exitosa, False en caso contrario.
        """
        if alert_id not in self.alerts:
            return False
        
        self.alerts[alert_id]["active"] = False
        self._save_alerts()
        
        return True
    
    def check_alert(self, alert_id):
        """
        Verifica una alerta específica.
        
        Args:
            alert_id (str): ID de la alerta a verificar.
        
        Returns:
            dict: Resultado de la verificación con claves 'triggered', 'value', etc.
        """
        if alert_id not in self.alerts:
            return {"error": "Alert not found"}
        
        alert = self.alerts[alert_id]
        
        if not alert["active"]:
            return {"error": "Alert is not active"}
        
        # Aquí iría la lógica para obtener datos del mercado y calcular el indicador
        try:
            # Para implementar: obtener datos de Alpaca o otra fuente
            # Por ahora, simulamos valores
            from addons.alertsbot.src.indicators import calculate_indicator
            
            # Obtener datos del mercado para el símbolo y timeframe
            # market_data = get_market_data(alert["symbol"], alert["timeframe"])
            
            # Simular datos del mercado para pruebas
            import numpy as np
            
            # Simulamos datos básicos: fecha, open, high, low, close, volume
            dates = [datetime.now() - timedelta(days=i) for i in range(100, 0, -1)]
            
            # Crear datos simulados basados en un patrón de tendencia + ruido
            base = 100  # Precio base
            trend = np.linspace(0, 20, 100)  # Tendencia alcista a lo largo del tiempo
            noise = np.random.normal(0, 5, 100)  # Ruido aleatorio
            
            # Crear precios simulados
            close_prices = base + trend + noise
            
            # Generar volatilidad para high, low
            high_prices = close_prices + np.random.uniform(0, 3, 100)
            low_prices = close_prices - np.random.uniform(0, 3, 100)
            open_prices = close_prices - noise  # Abrir cerca del cierre anterior + ruido
            volumes = np.random.uniform(100000, 1000000, 100)
            
            # Crear diccionario de datos simulados
            market_data = {
                "dates": dates,
                "open": open_prices,
                "high": high_prices,
                "low": low_prices,
                "close": close_prices,
                "volume": volumes
            }
            
            # Calcular el indicador con los datos y parámetros de la alerta
            indicator_value = calculate_indicator(
                alert["indicator"],
                market_data,
                alert["indicator_params"]
            )
            
            # Determinar si la alerta debe activarse
            triggered = False
            
            if alert["condition"] == "mayor que":
                triggered = indicator_value > alert["threshold"]
            elif alert["condition"] == "menor que":
                triggered = indicator_value < alert["threshold"]
            elif alert["condition"] in ["cruza por arriba", "cruza por abajo"]:
                # Para cruce, necesitamos el valor anterior
                prev_value = alert.get("last_value")
                
                if prev_value is not None:
                    if alert["condition"] == "cruza por arriba":
                        triggered = prev_value < alert["threshold"] and indicator_value >= alert["threshold"]
                    else:  # cruza por abajo
                        triggered = prev_value > alert["threshold"] and indicator_value <= alert["threshold"]
            
            # Actualizar estado de la alerta
            self.alerts[alert_id]["last_check"] = datetime.now().isoformat()
            self.alerts[alert_id]["last_value"] = indicator_value
            
            # Si la alerta se activó
            if triggered:
                self.alerts[alert_id]["triggered"] = True
                self.alerts[alert_id]["last_trigger"] = datetime.now().isoformat()
                
                # Enviar notificaciones
                self._send_notifications(alert_id)
            
            # Guardar cambios
            self._save_alerts()
            
            return {
                "triggered": triggered,
                "value": indicator_value,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def check_all_alerts(self):
        """
        Verifica todas las alertas activas.
        
        Returns:
            dict: Resultados de verificación para cada alerta.
        """
        results = {}
        
        for alert_id, alert in self.alerts.items():
            if alert["active"]:
                results[alert_id] = self.check_alert(alert_id)
        
        return results
    
    def _send_notifications(self, alert_id):
        """
        Envía notificaciones para una alerta activada.
        
        Args:
            alert_id (str): ID de la alerta activada.
        """
        alert = self.alerts[alert_id]
        channels = alert.get("notification_channels", {})
        
        # Notificación en la aplicación (se almacena en el estado de la alerta)
        if channels.get("app", True):
            # Aquí solo marcamos la alerta como notificada
            self.alerts[alert_id]["app_notified"] = True
        
        # Notificación por email
        if channels.get("email"):
            self._send_email_notification(alert_id, channels["email"])
        
        # Notificación por webhook
        if channels.get("webhook"):
            self._send_webhook_notification(alert_id, channels["webhook"])
    
    def _send_email_notification(self, alert_id, email):
        """
        Envía una notificación por email.
        
        Args:
            alert_id (str): ID de la alerta activada.
            email (str): Dirección de email del destinatario.
        """
        alert = self.alerts[alert_id]
        email_settings = self.settings.get("notification_settings", {}).get("email", {})
        
        if not email_settings.get("enabled", False):
            print(f"Notificación por email deshabilitada para alerta {alert_id}")
            return
        
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            # Crear mensaje
            msg = MIMEMultipart()
            msg['From'] = email_settings.get("from_email", "alertas@dashbottrade.com")
            msg['To'] = email
            msg['Subject'] = f"Alerta DashBotTrade: {alert['symbol']} - {alert['indicator']}"
            
            # Construir cuerpo del mensaje
            body = f"""
            <html>
            <body>
                <h2>Alerta DashBotTrade Activada</h2>
                <p>Se ha activado una alerta en el sistema DashBotTrade.</p>
                <h3>Detalles de la Alerta:</h3>
                <ul>
                    <li><strong>Activo:</strong> {alert['symbol']}</li>
                    <li><strong>Indicador:</strong> {alert['indicator']}</li>
                    <li><strong>Condición:</strong> {alert['condition']} {alert['threshold']}</li>
                    <li><strong>Valor actual:</strong> {alert['last_value']}</li>
                    <li><strong>Fecha y hora:</strong> {alert['last_trigger']}</li>
                </ul>
                <p>Esta es una notificación automática, por favor no responder a este correo.</p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            # Establecer conexión con servidor SMTP
            server = smtplib.SMTP(email_settings.get("smtp_server", ""), 
                                  email_settings.get("smtp_port", 587))
            server.starttls()
            server.login(email_settings.get("username", ""), 
                        email_settings.get("password", ""))
            
            # Enviar email
            server.send_message(msg)
            server.quit()
            
            print(f"Notificación por email enviada para alerta {alert_id}")
            return True
            
        except Exception as e:
            print(f"Error al enviar email para alerta {alert_id}: {e}")
            return False
    
    def _send_webhook_notification(self, alert_id, webhook_url):
        """
        Envía una notificación a un webhook.
        
        Args:
            alert_id (str): ID de la alerta activada.
            webhook_url (str): URL del webhook.
        """
        alert = self.alerts[alert_id]
        
        try:
            import requests
            
            # Preparar datos para el webhook
            payload = {
                "alert_id": alert_id,
                "symbol": alert["symbol"],
                "indicator": alert["indicator"],
                "condition": alert["condition"],
                "threshold": alert["threshold"],
                "current_value": alert["last_value"],
                "triggered_at": alert["last_trigger"]
            }
            
            # Enviar POST al webhook
            response = requests.post(webhook_url, json=payload)
            
            # Verificar respuesta
            if response.status_code == 200:
                print(f"Notificación webhook enviada para alerta {alert_id}")
                return True
            else:
                print(f"Error en webhook para alerta {alert_id}: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"Error al enviar webhook para alerta {alert_id}: {e}")
            return False
    
    def start_checking(self):
        """
        Inicia el thread de verificación periódica de alertas.
        """
        if self.check_thread is not None and self.check_thread.is_alive():
            print("El thread de verificación ya está en ejecución.")
            return
        
        self.stop_checking.clear()
        self.check_thread = threading.Thread(target=self._check_alerts_loop)
        self.check_thread.daemon = True  # El thread se cerrará cuando el programa principal termine
        self.check_thread.start()
        
        print("Thread de verificación de alertas iniciado.")
    
    def stop_checking(self):
        """
        Detiene el thread de verificación periódica de alertas.
        """
        if self.check_thread is not None and self.check_thread.is_alive():
            self.stop_checking.set()
            self.check_thread.join(timeout=2)
            print("Thread de verificación de alertas detenido.")
    
    def _check_alerts_loop(self):
        """
        Loop para verificar alertas periódicamente.
        """
        while not self.stop_checking.is_set():
            try:
                # Verificar todas las alertas activas
                self.check_all_alerts()
                
                # Esperar según el intervalo configurado
                time.sleep(self.settings.get("check_interval", 60))
                
            except Exception as e:
                print(f"Error en el loop de verificación: {e}")
                # Esperar un poco antes de intentar de nuevo
                time.sleep(5)
    
    def update_settings(self, settings_dict):
        """
        Actualiza la configuración del gestor de alertas.
        
        Args:
            settings_dict (dict): Diccionario con los ajustes a actualizar.
        
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        # Actualizar configuración
        for key, value in settings_dict.items():
            self.settings[key] = value
        
        # Guardar cambios
        success = self._save_settings()
        
        # Si se cambió el intervalo de verificación y el thread está activo,
        # reiniciar el thread para aplicar el nuevo intervalo
        if "check_interval" in settings_dict and self.check_thread is not None and self.check_thread.is_alive():
            self.stop_checking()
            self.start_checking()
        
        return success