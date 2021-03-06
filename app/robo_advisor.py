# robo-advisor/app/robo_advisor.py

import csv
import json
import os
import datetime
import plotly
import plotly.graph_objs as go

from dotenv import load_dotenv
import requests
import sendgrid
from sendgrid.helpers.mail import * 
from twilio.rest import Client

load_dotenv()

# Alpha Advantage
ALPHAVANTAGE_API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY", default="OOPS")

# Sendgrid Integration
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", default="OOPS")
MY_EMAIL_ADDRESS = os.environ.get("MY_EMAIL_ADDRESS", default="OOPS")

# Twilio Integration
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", default="OOPS")
TWILIO_AUTH_TOKEN  = os.environ.get("TWILIO_AUTH_TOKEN", default="OOPS")
SENDER_SMS  = os.environ.get("SENDER_SMS", default="OOPS")


def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.

    Source: https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/datatypes/numbers.md#formatting-as-currency
    
    Param: my_price (int or float) like 4000.444444
    
    Example: to_usd(4000.444444)
    
    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" 

def to_one_decimal_perc(my_number):
    """
    Converts a numeric value to percentage format with one decimal number, for printing and display purposes.
    
    Source: https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/datatypes/numbers.md#formatting-as-currency
    
    Param: my_number (int or float) like 35.87
    
    Example: to_one_decimal_perc(35.87)
    
    Returns: 35.9%
    """
    return "{0:.1f}%".format(my_number)

def get_response(my_ticker):
    """
    Takes stock ticker as input, makes a request for this stock's price information from Alpha Advantage website, and returns the request response
    (the returned response is not parsed)

    Source: https://github.com/prof-rossetti/intro-to-python/blob/50ffd90b31143edcb686a525c889977fda1b5d11/notes/python/packages/requests.md
    
    Param: my_ticker (string or combination of string and int/float) like "MSFT"
    
    Example: get_response("MSFT")
    """
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={my_ticker}&apikey={ALPHAVANTAGE_API_KEY}&outputsize=full"
    response = requests.get(request_url)
    return response

def write_csv_file_name(ticker_input):
    """
    Takes in any stock ticker and creates a CSV file name concatenating the word "price" with the stock ticker (with .csv extension)

    Source: https://github.com/prof-rossetti/intro-to-python/blob/7adaa47921be090406fd43e2e67cbd7c72092bde/notes/python/modules/csv.md
    
    Param: ticker_input (string format) like "AAPL"
    
    Example: write_csv_file_name("AAPL")
    
    Returns: prices_AAPL.csv
    """
    csv_file_name = f"prices_{ticker_input}.csv"
    return csv_file_name
    

if __name__ == "__main__":

    # INFO INPUTS

    # Request time
    request_time = datetime.datetime.now()
    today = datetime.date.today()

    # Ask user to input stock tickers
    tickers = []

    while True:
        ticker = input("Please enter a stock ticker or DONE when you are finished: ")
        if len(ticker) > 8 or ticker.isnumeric == True:
            print("Please enter a valid ticker. It should not be longer than 8 characters or be all-numeric.")
        elif ticker == "DONE":
            user_email = input("To receive price movement alerts by email, please enter your email address: ")
            user_sms = input("To receive price movement alerts by SMS, please enter you phone number including a '+' sign and country area code (no dashes or spaces): ")
            break
        else: 
            tickers.append(ticker)
    
    # Request information 
    for t in tickers:
        response = get_response(t)

        if "Error Message" in response.text:
            print("-------------------------")
            print("SELECTED TICKER: " + t)
            print("Sorry, could not find your ticker.")
            print("-------------------------")
        else:
            parsed_response = json.loads(response.text)
            
            tsd = parsed_response["Time Series (Daily)"]
            all_dates = list(tsd.keys())
            dates = all_dates[0:252]

            # Create a csv file for each stock request
            csv_file_path = os.path.join(os.path.dirname(__file__),"..", "data", write_csv_file_name(t))
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

            one_year_high = max(high_prices)
            one_year_low = min(low_prices)


            # Provide investment recommendation
            current = float(latest_close)
            percent_diff = (current/one_year_low - 1) * 100

            if current <= (one_year_low *1.1):
                recommendation = "Strong buy"
                recommendation_reason = "Current Stock Price (" + to_usd(current) + ") is only " 
                recommendation_reason += str(to_one_decimal_perc(percent_diff)) + " higher than its 52-week low of " + to_usd(one_year_low)
            elif current > (one_year_low * 1.1) and current <= (one_year_low * 1.25):
                recommendation = "Buy"
                recommendation_reason = "Current Stock Price (" + to_usd(current) + ") is only " 
                recommendation_reason += str(to_one_decimal_perc(percent_diff)) + " higher than its 52-week low of " + to_usd(one_year_low)
            elif current > (one_year_low * 1.25) and current <= (one_year_low * 1.5):
                recommendation = "Neutral"
                recommendation_reason = "Current Stock Price (" + to_usd(current) + ") is " 
                recommendation_reason += str(to_one_decimal_perc(percent_diff)) + " higher than its 52-week low of " + to_usd(one_year_low)
            elif current > (one_year_low * 1.5) and current <= (one_year_low * 1.75):
                recommendation = "Sell"
                recommendation_reason = "Current Stock Price (" + to_usd(current) + ") is " 
                recommendation_reason += str(to_one_decimal_perc(percent_diff)) + " higher than its 52-week low of " + to_usd(one_year_low)
            elif current > (one_year_low * 1.75):
                recommendation = "Strong sell"
                recommendation_reason = "Current Stock Price (" + to_usd(current) + ") is " 
                recommendation_reason += str(to_one_decimal_perc(percent_diff)) + " higher than its 52-week low of " + to_usd(one_year_low)
            

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
            output += f"LATEST CLOSE: {to_usd(current)}"
            output += "\n"
            output += f"52-WEEK HIGH: {to_usd(one_year_high)}"
            output += "\n"
            output += f"52-WEEk LOW: {to_usd(one_year_low)}"
            output += "\n"
            output += "-------------------------"
            output += "\n"
            output += f"RECOMMENDATION: {recommendation}"
            output += "\n"
            output += f"RECOMMENDATION REASON: {recommendation_reason}"
            output += "\n"
            output += "-------------------------"
            output += "\n"

            print(output)


            # Plot prices over time using thrid-party package Plotly
            plotly.offline.plot({
                "data": [go.Scatter(x=[each_day for each_day in dates], 
                        y=[tsd[each_day]["4. close"] for each_day in dates])],
                "layout": go.Layout(title="Stock Price for " + t)
            }, auto_open=True) 


            # Send price movement alerts via Email and SMS
            previous_day = dates[1]
            previous_day_close = float(tsd[previous_day]["4. close"])
            change = (current/previous_day_close-1) * 100

            if current >= (previous_day_close*1.05) or current <= (previous_day_close*0.95):
                alert_message = "This is an notification alert to informe you that :"
                alert_message += "\n"
                alert_message += f"Stock {t} has moved {to_one_decimal_perc(change)} from last trading day's closing price."
                alert_message += "\n"
                alert_message += f"It currently trades at {to_usd(current)}. "

                # via Email 
                sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)

                from_email = Email(MY_EMAIL_ADDRESS)
                to_email = Email(user_email) 
                subject = "5% Price Movement Alert"
                message_text = alert_message
                content = Content("text/plain", message_text)
                mail = Mail(from_email, subject, to_email, content)

                response = sg.client.mail.send.post(request_body=mail.get())

                # via SMS
                client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                message = client.messages.create(to=user_sms, from_=SENDER_SMS, body=alert_message)
                
            else: 
                pass