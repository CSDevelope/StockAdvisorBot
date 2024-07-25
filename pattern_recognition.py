import pandas_ta as ta

def calculate_indicators(data):
    data['SMA'] = ta.sma(data['close'], length=30)
    data['RSI'] = ta.rsi(data['close'], length=14)
    return data
