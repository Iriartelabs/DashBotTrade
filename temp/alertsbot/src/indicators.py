# addons/alertsbot/src/indicators.py
import numpy as np
import pandas as pd

def get_available_indicators():
    """
    Devuelve un diccionario con los indicadores disponibles y sus parámetros.
    
    Returns:
        dict: Diccionario con los indicadores disponibles.
    """
    return {
        "RSI": {
            "description": "Relative Strength Index - Indicador de sobrecompra/sobreventa",
            "parameters": {
                "period": {"type": "number", "default": 14, "min": 2, "max": 50}
            },
            "function": calculate_rsi,
            "output": "single_value",
            "category": "momentum"
        },
        "SMA": {
            "description": "Simple Moving Average - Media Móvil Simple",
            "parameters": {
                "period": {"type": "number", "default": 20, "min": 2, "max": 200}
            },
            "function": calculate_sma,
            "output": "line",
            "category": "trend"
        },
        "EMA": {
            "description": "Exponential Moving Average - Media Móvil Exponencial",
            "parameters": {
                "period": {"type": "number", "default": 20, "min": 2, "max": 200}
            },
            "function": calculate_ema,
            "output": "line",
            "category": "trend"
        },
        "MACD": {
            "description": "Moving Average Convergence Divergence",
            "parameters": {
                "fast_period": {"type": "number", "default": 12, "min": 2, "max": 50},
                "slow_period": {"type": "number", "default": 26, "min": 3, "max": 100},
                "signal_period": {"type": "number", "default": 9, "min": 2, "max": 50}
            },
            "function": calculate_macd,
            "output": "multi_line",
            "category": "momentum"
        },
        "Bollinger Bands": {
            "description": "Bandas de Bollinger - Indicador de volatilidad",
            "parameters": {
                "period": {"type": "number", "default": 20, "min": 2, "max": 100},
                "std_dev": {"type": "float", "default": 2.0, "min": 0.5, "max": 5.0}
            },
            "function": calculate_bollinger_bands,
            "output": "bands",
            "category": "volatility"
        },
        "Stochastic": {
            "description": "Oscilador Estocástico - Indicador de momento",
            "parameters": {
                "k_period": {"type": "number", "default": 14, "min": 2, "max": 50},
                "d_period": {"type": "number", "default": 3, "min": 1, "max": 20},
                "slowing": {"type": "number", "default": 3, "min": 1, "max": 20}
            },
            "function": calculate_stochastic,
            "output": "multi_line",
            "category": "momentum"
        },
        "ATR": {
            "description": "Average True Range - Indicador de volatilidad",
            "parameters": {
                "period": {"type": "number", "default": 14, "min": 2, "max": 50}
            },
            "function": calculate_atr,
            "output": "single_value",
            "category": "volatility"
        },
        "OBV": {
            "description": "On-Balance Volume - Indicador de volumen",
            "parameters": {},
            "function": calculate_obv,
            "output": "line",
            "category": "volume"
        },
        "ADX": {
            "description": "Average Directional Index - Indicador de fuerza de tendencia",
            "parameters": {
                "period": {"type": "number", "default": 14, "min": 2, "max": 50}
            },
            "function": calculate_adx,
            "output": "single_value",
            "category": "trend"
        },
        "Ichimoku Cloud": {
            "description": "Ichimoku Kinko Hyo - Sistema de trading japonés",
            "parameters": {
                "tenkan_period": {"type": "number", "default": 9, "min": 2, "max": 50},
                "kijun_period": {"type": "number", "default": 26, "min": 2, "max": 100},
                "senkou_span_b_period": {"type": "number", "default": 52, "min": 2, "max": 200}
            },
            "function": calculate_ichimoku,
            "output": "cloud",
            "category": "trend"
        }
    }

def calculate_indicator(indicator_name, market_data, params):
    """
    Calcula un indicador técnico usando los datos de mercado proporcionados.
    
    Args:
        indicator_name (str): Nombre del indicador a calcular.
        market_data (dict): Datos de mercado organizados en un diccionario.
        params (dict): Parámetros para el cálculo del indicador.
    
    Returns:
        float or dict: Valor(es) del indicador calculado.
    """
    indicators = get_available_indicators()
    
    if indicator_name not in indicators:
        raise ValueError(f"Indicador '{indicator_name}' no disponible.")
    
    # Convertir datos de mercado a DataFrame si no lo es
    if not isinstance(market_data, pd.DataFrame):
        market_data = pd.DataFrame({
            'date': market_data['dates'],
            'open': market_data['open'],
            'high': market_data['high'],
            'low': market_data['low'],
            'close': market_data['close'],
            'volume': market_data['volume']
        })
        market_data.set_index('date', inplace=True)
    
    # Obtener la función del indicador
    indicator_func = indicators[indicator_name]["function"]
    
    # Calcular el indicador
    result = indicator_func(market_data, **params)
    
    # Si el resultado es un DataFrame o Series con múltiples valores,
    # devolver el valor más reciente para alertas
    if isinstance(result, (pd.DataFrame, pd.Series)):
        return result.iloc[-1]
    
    return result

def calculate_rsi(data, period=14):
    """
    Calcula el Relative Strength Index (RSI).
    
    Args:
        data (pd.DataFrame): DataFrame con los datos de mercado.
        period (int, optional): Período para el cálculo del RSI. Por defecto 14.
    
    Returns:
        float: Valor del RSI (entre 0 y 100).
    """
    # Asegurarse de que data tiene una columna 'close'
    if 'close' not in data.columns:
        raise ValueError("Los datos deben tener una columna 'close'.")
    
    # Calcular cambios diarios
    delta = data['close'].diff()
    
    # Separar ganancias y pérdidas
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    
    # Calcular promedios
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    
    # Calcular RS (Relative Strength)
    rs = avg_gain / avg_loss
    
    # Calcular RSI
    rsi = 100 - (100 / (1 + rs))
    
    # Devolver el valor más reciente del RSI
    return rsi.iloc[-1]

def calculate_sma(data, period=20):
    """
    Calcula la Simple Moving Average (SMA).
    
    Args:
        data (pd.DataFrame): DataFrame con los datos de mercado.
        period (int, optional): Período para el cálculo de la SMA. Por defecto 20.
    
    Returns:
        float: Valor de la SMA.
    """
    if 'close' not in data.columns:
        raise ValueError("Los datos deben tener una columna 'close'.")
    
    sma = data['close'].rolling(window=period).mean()
    
    return sma.iloc[-1]

def calculate_ema(data, period=20):
    """
    Calcula la Exponential Moving Average (EMA).
    
    Args:
        data (pd.DataFrame): DataFrame con los datos de mercado.
        period (int, optional): Período para el cálculo de la EMA. Por defecto 20.
    
    Returns:
        float: Valor de la EMA.
    """
    if 'close' not in data.columns:
        raise ValueError("Los datos deben tener una columna 'close'.")
    
    ema = data['close'].ewm(span=period, adjust=False).mean()
    
    return ema.iloc[-1]

def calculate_macd(data, fast_period=12, slow_period=26, signal_period=9):
    """
    Calcula el Moving Average Convergence Divergence (MACD).
    
    Args:
        data (pd.DataFrame): DataFrame con los datos de mercado.
        fast_period (int, optional): Período para la EMA rápida. Por defecto 12.
        slow_period (int, optional): Período para la EMA lenta. Por defecto 26.
        signal_period (int, optional): Período para la línea de señal. Por defecto 9.
    
    Returns:
        dict: Diccionario con valores para 'macd', 'signal' y 'histogram'.
    """
    if 'close' not in data.columns:
        raise ValueError("Los datos deben tener una columna 'close'.")
    
    # Calcular EMAs
    ema_fast = data['close'].ewm(span=fast_period, adjust=False).mean()
    ema_slow = data['close'].ewm(span=slow_period, adjust=False).mean()
    
    # Calcular MACD
    macd_line = ema_fast - ema_slow
    
    # Calcular línea de señal
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    
    # Calcular histograma
    histogram = macd_line - signal_line
    
    return {
        'macd': macd_line.iloc[-1],
        'signal': signal_line.iloc[-1],
        'histogram': histogram.iloc[-1]
    }

def calculate_bollinger_bands(data, period=20, std_dev=2.0):
    """
    Calcula las Bandas de Bollinger.
    
    Args:
        data (pd.DataFrame): DataFrame con los datos de mercado.
        period (int, optional): Período para la SMA. Por defecto 20.
        std_dev (float, optional): Número de desviaciones estándar. Por defecto 2.0.
    
    Returns:
        dict: Diccionario con valores para 'upper', 'middle' y 'lower'.
    """
    if 'close' not in data.columns:
        raise ValueError("Los datos deben tener una columna 'close'.")
    
    # Calcular SMA
    middle_band = data['close'].rolling(window=period).mean()
    
    # Calcular desviación estándar
    std = data['close'].rolling(window=period).std()
    
    # Calcular bandas superior e inferior
    upper_band = middle_band + (std * std_dev)
    lower_band = middle_band - (std * std_dev)
    
    return {
        'upper': upper_band.iloc[-1],
        'middle': middle_band.iloc[-1],
        'lower': lower_band.iloc[-1]
    }

def calculate_stochastic(data, k_period=14, d_period=3, slowing=3):
    """
    Calcula el Oscilador Estocástico.
    
    Args:
        data (pd.DataFrame): DataFrame con los datos de mercado.
        k_period (int, optional): Período para %K. Por defecto 14.
        d_period (int, optional): Período para %D. Por defecto 3.
        slowing (int, optional): Período de ralentización. Por defecto 3.
    
    Returns:
        dict: Diccionario con valores para 'k' y 'd'.
    """
    if not all(col in data.columns for col in ['high', 'low', 'close']):
        raise ValueError("Los datos deben tener columnas 'high', 'low' y 'close'.")
    
    # Calcular el máximo y mínimo para el período k_period
    lowest_low = data['low'].rolling(window=k_period).min()
    highest_high = data['high'].rolling(window=k_period).max()
    
    # Calcular %K
    k = 100 * ((data['close'] - lowest_low) / (highest_high - lowest_low))
    
    # Aplicar ralentización (slowing)
    if slowing > 1:
        k = k.rolling(window=slowing).mean()
    
    # Calcular %D (media móvil de %K)
    d = k.rolling(window=d_period).mean()
    
    return {
        'k': k.iloc[-1],
        'd': d.iloc[-1]
    }

def calculate_atr(data, period=14):
    """
    Calcula el Average True Range (ATR).
    
    Args:
        data (pd.DataFrame): DataFrame con los datos de mercado.
        period (int, optional): Período para el cálculo del ATR. Por defecto 14.
    
    Returns:
        float: Valor del ATR.
    """
    if not all(col in data.columns for col in ['high', 'low', 'close']):
        raise ValueError("Los datos deben tener columnas 'high', 'low' y 'close'.")
    
    # Calcular True Range
    high_low = data['high'] - data['low']
    high_close = (data['high'] - data['close'].shift()).abs()
    low_close = (data['low'] - data['close'].shift()).abs()
    
    # True Range es el máximo de los tres valores
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    
    # Calcular ATR (media móvil del True Range)
    atr = tr.rolling(window=period).mean()
    
    return atr.iloc[-1]

def calculate_obv(data):
    """
    Calcula el On-Balance Volume (OBV).
    
    Args:
        data (pd.DataFrame): DataFrame con los datos de mercado.
    
    Returns:
        float: Valor del OBV.
    """
    if not all(col in data.columns for col in ['close', 'volume']):
        raise ValueError("Los datos deben tener columnas 'close' y 'volume'.")
    
    # Calcular cambios diarios en el precio
    price_change = data['close'].diff()
    
    # Inicializar OBV
    obv = pd.Series(index=data.index)
    obv.iloc[0] = 0
    
    # Calcular OBV
    for i in range(1, len(data)):
        if price_change.iloc[i] > 0:
            # Si el precio sube, añadir volumen
            obv.iloc[i] = obv.iloc[i-1] + data['volume'].iloc[i]
        elif price_change.iloc[i] < 0:
            # Si el precio baja, restar volumen
            obv.iloc[i] = obv.iloc[i-1] - data['volume'].iloc[i]
        else:
            # Si el precio no cambia, mantener OBV
            obv.iloc[i] = obv.iloc[i-1]
    
    return obv.iloc[-1]

def calculate_adx(data, period=14):
    """
    Calcula el Average Directional Index (ADX).
    
    Args:
        data (pd.DataFrame): DataFrame con los datos de mercado.
        period (int, optional): Período para el cálculo del ADX. Por defecto 14.
    
    Returns:
        float: Valor del ADX.
    """
    if not all(col in data.columns for col in ['high', 'low', 'close']):
        raise ValueError("Los datos deben tener columnas 'high', 'low' y 'close'.")
    
    # Calcular +DM y -DM
    high_diff = data['high'].diff()
    low_diff = data['low'].diff()
    
    pos_dm = high_diff.where((high_diff > 0) & (high_diff > low_diff.abs()), 0)
    neg_dm = low_diff.abs().where((low_diff < 0) & (low_diff.abs() > high_diff), 0)
    
    # Calcular TR
    high_low = data['high'] - data['low']
    high_close = (data['high'] - data['close'].shift()).abs()
    low_close = (data['low'] - data['close'].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    
    # Calcular medias móviles exponenciales de +DM, -DM y TR
    pos_di = 100 * (pos_dm.ewm(span=period, adjust=False).mean() / tr.ewm(span=period, adjust=False).mean())
    neg_di = 100 * (neg_dm.ewm(span=period, adjust=False).mean() / tr.ewm(span=period, adjust=False).mean())
    
    # Calcular DX
    dx = 100 * ((pos_di - neg_di).abs() / (pos_di + neg_di))
    
    # Calcular ADX
    adx = dx.ewm(span=period, adjust=False).mean()
    
    return adx.iloc[-1]

def calculate_ichimoku(data, tenkan_period=9, kijun_period=26, senkou_span_b_period=52):
    """
    Calcula el Ichimoku Kinko Hyo.
    
    Args:
        data (pd.DataFrame): DataFrame con los datos de mercado.
        tenkan_period (int, optional): Período para Tenkan-sen. Por defecto 9.
        kijun_period (int, optional): Período para Kijun-sen. Por defecto 26.
        senkou_span_b_period (int, optional): Período para Senkou Span B. Por defecto 52.
    
    Returns:
        dict: Diccionario con valores para las líneas de Ichimoku.
    """
    if not all(col in data.columns for col in ['high', 'low', 'close']):
        raise ValueError("Los datos deben tener columnas 'high', 'low' y 'close'.")
    
    # Calcular Tenkan-sen (Línea de Conversión)
    tenkan_sen = (data['high'].rolling(window=tenkan_period).max() + 
                  data['low'].rolling(window=tenkan_period).min()) / 2
    
    # Calcular Kijun-sen (Línea Base)
    kijun_sen = (data['high'].rolling(window=kijun_period).max() + 
                 data['low'].rolling(window=kijun_period).min()) / 2
    
    # Calcular Senkou Span A (Primera Línea Principal)
    senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(kijun_period)
    
    # Calcular Senkou Span B (Segunda Línea Principal)
    senkou_span_b = ((data['high'].rolling(window=senkou_span_b_period).max() + 
                      data['low'].rolling(window=senkou_span_b_period).min()) / 2).shift(kijun_period)
    
    # Calcular Chikou Span (Línea de Retraso)
    chikou_span = data['close'].shift(-kijun_period)
    
    return {
        'tenkan_sen': tenkan_sen.iloc[-1],
        'kijun_sen': kijun_sen.iloc[-1],
        'senkou_span_a': senkou_span_a.iloc[-1],
        'senkou_span_b': senkou_span_b.iloc[-1],
        'chikou_span': chikou_span.iloc[-1] if len(chikou_span) > kijun_period else None
    }