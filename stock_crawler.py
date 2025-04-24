import yfinance as yf
import csv
from datetime import datetime

# List of stock symbols in Yahoo Finance format
stock_symbols = {
    "AMWAY": "6351.KL",
    "APOLLO": "6432.KL",
    "MBB": "1155.KL",
    "PETDAG": "5681.KL",
    "PETGAS": "6033.KL",
    "PETCHEM": "5183.KL",
    "PANAMY": "3719.KL",
    # Add more symbols here if needed
}

# Output CSV file
output_file = "stock_prices.csv"

#def fetch_price_yfinance(symbol: str) -> float:
#    ticker = yf.Ticker(symbol)
#    data = ticker.history(period="1d", interval="1m")
#    if not data.empty:
#        latest_price = data['Close'].iloc[-1]
#        return round(latest_price, 2)
#    else:
#        raise ValueError(f"No data returned for symbol: {symbol}")

def get_price_yfinance(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        price = info.get("regularMarketPrice") or info.get("currentPrice")

        if not price:
            # fallback to historical data
            hist = stock.history(period="1d")
            price = hist["Close"].iloc[-1] if not hist.empty else None

        return price if price else "NA"
    except Exception as e:
        print(f"⚠️ Error fetching {symbol}: {e}")
        return "NA"

def write_to_csv(timestamp: str, prices: dict):
    file_exists = False
    try:
        with open(output_file, "r"):
            file_exists = True
    except FileNotFoundError:
        pass

    with open(output_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            # Write header if file is new
            writer.writerow(["Timestamp"] + list(prices.keys()))
        writer.writerow([timestamp] + list(prices.values()))

def crawl_prices():
    print(f"Running crawl at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    prices = {}
    for name, symbol in stock_symbols.items():
        try:
            print(f"Fetching price for {name} ({symbol})...")
            price = fetch_price_yfinance(symbol)
            prices[name] = price
            print(f"✅ {name} = {price}")
        except Exception as e:
            print(f"❌ Failed to fetch {name}: {e}")
            prices[name] = "N/A"
    write_to_csv(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), prices)
    print("✅ Prices written to", output_file)

if __name__ == "__main__":
    crawl_prices()
