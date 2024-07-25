import yfinance as yf

def fetch_index_data(symbol):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="1d")
    if not hist.empty:
        return hist.iloc[-1]
    else:
        print(f"No data fetched for {symbol}")
        return None

def get_index_summary():
    indices = {
        '^DJI': 'Dow Jones Industrial Average',
        '^GSPC': 'S&P 500',
        '^IXIC': 'Nasdaq Composite'
    }
    summary = []
    for symbol, name in indices.items():
        data = fetch_index_data(symbol)
        if data is not None:
            print(f"Data fetched for {symbol}: {data}")  # Debug information
            price = data['Close']
            change = data['Close'] - data['Open']
            change_pct = (change / data['Open']) * 100
            summary.append(f"{name}: Closed {('up' if change > 0 else 'down')} at {price:.2f} points, {change_pct:.2f}% change")
        else:
            print(f"No data fetched for {symbol}")
    return summary

if __name__ == "__main__":
    summary = get_index_summary()
    for line in summary:
        print(line)
