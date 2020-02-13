# app/robo_advisor.py

import requests
import json

def to_usd (price):
    return "${0:.2f}".format(price)

# INFO INPUTS

request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo"

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
