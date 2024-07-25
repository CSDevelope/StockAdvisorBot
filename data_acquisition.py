from alpha_vantage.timeseries import TimeSeries

def fetch_stock_data(symbol, api_key):
    ts = TimeSeries(key=api_key, output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=symbol, interval='1min', outputsize='compact')
    data.columns = ['open', 'high', 'low', 'close', 'volume']
    return data
