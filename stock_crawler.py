import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import pytz
import os
from playwright.sync_api import sync_playwright

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
def get_price_with_playwright(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_selector("div.tv-symbol-price-quote__value", timeout=10000)
        price = page.query_selector("div.tv-symbol-price-quote__value").inner_text()
        browser.close()
        return price

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
        price = get_price_with_playwright(url)
        results[symbol] = price
        print(f"{symbol}: {price}")
    write_to_csv(results)
    print("Finished writing to CSV.\n")

# No scheduler needed — we call the function directly
if __name__ == "__main__":
    crawl_prices()
