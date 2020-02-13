# app/robo_advisor.py

import csv
import json
import os

from dotenv import load_dotenv
import requests

load_dotenv()

def to_usd (price):
    return "${0:.2f}".format(price)

# INFO INPUTS


symbole = "MSFT"
#input("Please enter a ticker")
api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbole}&apikey={api_key}"
response = requests.get(request_url)

#print(type(response)) # 'requests.models.Response'
#print(response.status_code)
#print(response.text)

parsed_response = json.loads(response.text)
last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

tsd = parsed_response["Time Series (Daily)"]

dates = list(tsd.keys())

latest_day = dates[0]
latest_close = tsd[latest_day]["4. close"]


# Recent High
high_prices = []

for each_day in dates:
    high_price = float(tsd[each_day]["2. high"])
    high_prices.append(high_price)

recent_high = max(high_prices)

# Recent Low
low_prices = []

for each_day in dates:
    low_price = float(tsd[each_day]["3. low"])
    low_prices.append(low_price)

recent_low = min(low_prices)


# csv

csv_file_path = os.path.join(os.path.dirname(__file__),"..", "data", "prices.csv")

csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader() # uses fieldnames set above
    
    # need some sort of loop
    for each_day in dates:
        daily_prices = tsd[each_day]
        writer.writerow({
            "timestamp": each_day, 
            "open": daily_prices["1. open"], 
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["5. volume"]
        })
    

# INFO OUTPUTS

print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print("LATEST DAY: " + last_refreshed)
#print(f"LATEST DAY: {last_refreshed}")
print("LATEST CLOSE: " + to_usd(float(latest_close)))
print("RECENT HIGH: " + to_usd(float(recent_high)))
print("RECENT LOW: " + to_usd(float(recent_low)))
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")
