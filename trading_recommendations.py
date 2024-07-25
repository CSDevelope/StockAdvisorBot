def generate_signals(data):
    data['Signal'] = 0
    data.loc[data['RSI'] < 30, 'Signal'] = 1  # Buy Signal
    data.loc[data['RSI'] > 70, 'Signal'] = -1  # Sell Signal
    return data
