import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import pytz
import os

# List of stock URLs
STOCK_URLS = {
    "AMWAY": "https://www.tradingview.com/symbols/MYX-AMWAY/",
    "APOLLO": "https://www.tradingview.com/symbols/MYX-APOLLO/",
    "MAYBANK": "https://www.tradingview.com/symbols/MYX-MAYBANK/",
    "PANAMY": "https://www.tradingview.com/symbols/MYX-PANAMY/",
    "PCHEM": "https://www.tradingview.com/symbols/MYX-PCHEM/",
    "PETGAS": "https://www.tradingview.com/symbols/MYX-PETGAS/",
    "PETDAG": "https://www.tradingview.com/symbols/MYX-PETDAG/",
}

# Extract price from TradingView
def get_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        price_element = soup.find("div", class_="tv-symbol-price-quote__value")
        return price_element.text.strip() if price_element else "N/A"
    except Exception as e:
        return f"Error: {e}"

# Write to CSV
def write_to_csv(data):
    os.makedirs("data", exist_ok=True)  # ✅ create 'data' folder if missing
    with open("data/stock_prices.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for symbol, price in data.items():
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), symbol, price])

# Main job to run
def crawl_prices():
    print("Running crawl at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    results = {}
    for symbol, url in STOCK_URLS.items():
        print(f"Fetching price for {symbol}...")
        price = get_price(url)
        results[symbol] = price
        print(f"{symbol}: {price}")
    write_to_csv(results)
    print("Finished writing to CSV.\n")

# No scheduler needed — we call the function directly
if __name__ == "__main__":
    crawl_prices()
