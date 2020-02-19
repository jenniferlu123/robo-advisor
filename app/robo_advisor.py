# app/robo_advisor.py

import csv
import json
import os
import datetime

from dotenv import load_dotenv
import requests

load_dotenv()
api_key = os.getenv("ALPHAVANTAGE_API_KEY", default="OOPS")

# Define a variable that can be used to convert prices to USD format
def to_usd (price):
    return "${0:.2f}".format(price)

# INFO INPUTS

# Request time
request_time = datetime.datetime.now()

# Ask user to input stock symbole/tickers
tickers = []

while True:
    ticker = input("Please enter a stock ticker: ")
    if len(ticker) > 8 or ticker.isnumeric == True:
        print("Please enter a valid ticker")
    elif ticker == "DONE":
        break
    else: 
        tickers.append(ticker)
 

 # Request information 

for t in tickers:
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={t}&apikey={api_key}"
    response = requests.get(request_url)
    
    if "Error Message" in response.text:
        print(request_url)
        print(type(response)) # 'requests.models.Response'
        print(response.status_code)
        print(response.text)

        print("Sorry, could not find your ticker. Please try again")
    else:
        parsed_response = json.loads(response.text)

        tsd = parsed_response["Time Series (Daily)"]
        dates = list(tsd.keys())
       
        #print(type(response)) # 'requests.models.Response'
        #print(response.status_code)
        #print(response.text)

        # Create a csv file for each stock request

        csv_file_name = "prices_" + t + ".csv"
        csv_file_path = os.path.join(os.path.dirname(__file__),"..", "data", csv_file_name)

        csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]


        with open(csv_file_path, "w") as csv_file: 
            writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
            writer.writeheader() 

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
            # for date, prices in tsd.items():

    
        # Latest Day
        last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]


        # Latest Close

        latest_day = dates[0]
        latest_close = tsd[latest_day]["4. close"]


        # Recent High and Low
        high_prices = []
        low_prices = []

        for each_day in dates:
            daily_prices = tsd[each_day]
            
            high_price = float(daily_prices["2. high"])
            high_prices.append(high_price)

            low_price = float(daily_prices["3. low"])
            low_prices.append(low_price)

        recent_high = max(high_prices)
        recent_low = min(low_prices)

        # Provide investment recommendation
        current = float(latest_close)
        lowest = float(recent_low)

        percent_difference = str((current/lowest - 1) * 100)

        if current <= (lowest *1.1):
            recommendation = "Strong buy"
            recommendation_reason = "Current Stock Price is " + percent_difference + " % of recent low"
        elif current > (lowest * 1.1) and current <= (lowest * 1.25):
            recommendation = "Buy"
            recommendation_reason = "Current Stock Price is " + percent_difference + " % of recent low"
        elif current > (lowest * 1.25) and current <= (lowest * 1.5):
            recommendation = "Neutral"
            recommendation_reason = "Current Stock Price is " + percent_difference + " % of recent low"
        elif current > (lowest * 1.5) and current <= (lowest * 1.75):
            recommendation = "Sell"
            recommendation_reason = "Current Stock Price is " + percent_difference + " % of recent low"
        elif current > (lowest * 1.75):
            recommendation = "Strong sell"
            recommendation_reason = "Current Stock Price is " + percent_difference + " % of recent low"
        


# Create csv file for each request:

#csv_file_name = "prices_" + ticker + ".csv"
#csv_file_path = os.path.join(os.path.dirname(__file__),"..", "data", csv_file_name)
#
#csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]
#
#with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
#    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
#    writer.writeheader() 
#    
#    # need some sort of loop
#    for each_day in dates:
#        daily_prices = tsd[each_day]
#        writer.writerow({
#            "timestamp": each_day, 
#            "open": daily_prices["1. open"], 
#            "high": daily_prices["2. high"],
#            "low": daily_prices["3. low"],
#            "close": daily_prices["4. close"],
#            "volume": daily_prices["5. volume"]
#        })
    

# INFORMATION OUTPUT

        output = "-------------------------"
        output += "\n"
        output += "SELECTED TICKER: " + t
        output += "\n"
        output += "-------------------------"
        output += "\n"
        output += "REQUESTING STOCK MARKET DATA..."
        output += "\n"
        output += "REQUEST AT: " + request_time.strftime("%Y-%m-%d %I:%M %p")
        output += "\n"
        output += "-------------------------"
        output += "\n"
        output += f"LATEST DAY: {last_refreshed}"
        output += "\n"
        output += f"LATEST CLOSE: {to_usd(float(latest_close))}"
        output += "\n"
        output += f"RECENT HIGH: {to_usd(float(recent_high))}"
        output += "\n"
        output += f"RECENT LOW: {to_usd(float(recent_low))}"
        output += "\n"
        output += "-------------------------"
        output += "\n"
        output += f"RECOMMENDATION: {recommendation}!"
        output += "\n"
        output += f"RECOMMENDATION REASON: {recommendation_reason}"
        output += "\n"
        output += "-------------------------"
        output += "\n"
        output += "HAPPY INVESTING!"
        output += "\n"
        output += "-------------------------"
        print(output)