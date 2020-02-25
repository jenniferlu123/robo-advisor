# robo-advisor

# Introduction:  

The goal of this python application is to automate the process of providing clients with stock trading recommendations. Specifically, clients/users will be able to enter one or more stock or cryptocurrency symbols (tickers) and the program will provide historical trading data as well as a recommendation as to whether or not the user should buy the given stocks or cryptocurrencies.  

# Prerequisites:

  + Anaconda 3.7
  + Python 3.7
  + Pip

# Instalation: 

Fork this [remote repository](https://github.com/jenniferlu123/robo-advisor) to your own GitHub repository, then clone (download) your remote copy onto your local computer.

Then navigate there from the command line :

```sh
cd ~/Desktop/robo-advisor
```

# Setup:

## Virtual environment set up

Use Anaconda to create and activate a new virtual environment named "stocks-env":

```sh
conda create -n stocks-env python=3.7 # (first time only)
conda activate stocks-env
```

## Required packages installation

From inside the virtual environment, install all necessary packages by running the following line:

```sh
pip install -r requirements.txt
```

## Alpha Vantage account set up

Please set up an account at [Alpha Vantage](https://www.alphavantage.co/) and obtain an Alpha Advantage API KEY. Then, update that information in the ".env" file:

    ALPHAVANTAGE_API_KEY = "EXAMPLE"

## Email template set up

If you are interested in using this program's email capabilities to send stock price movement alerts to clients, please set up an account at [Sendgrid](https://signup.sendgrid.com/), and obtain a Sendgrid API KEY. Then, please update the ".env" file using your Sendgrid API KEY and email address (the one you used to set up the Sendgrid account): 

    SENDGRID_API_KEY="EXAMPLE" 
    MY_EMAIL_ADDRESS="EXAMPLE" 

## SMS template set up

If you are interested in using this program's SMS capabilities to send stock price movement alerts to clients, please set up an account at [Twilio](https://www.twilio.com/try-twilio), and obtain a Twilio Account SID, Twilio Auth Token, and Twilio phone number to send out SMS messages. Then, using that information please update the following three credentials in the ".env" file: 

    TWILIO_ACCOUNT_SID="EXAMPLE"
    TWILIO_AUTH_TOKEN="EXAMPLE"
    SENDER_SMS="+11234567891" # include a '+' sign and country area code at the beginning, but no dashes or spaces (e.g. +1 for a U.S. phone followed by the actual phone number 1234567891)


# Usage:

Run the python script:

```py
python app/robo_advisor.py
```

# Overview of the "steps" of the robo-advisor program:

1. Enter your stock or cryptocurrency ticker. If you have multiple tickers, type one ticker at a time, and then press the 'ENTER' key to enter the next one

    Note: The request is limited to a maximum of 5 stocks each time

2. After you have entered all the tickers, enter DONE

3. The program will ask for user's email address where they would like to receive stock price movement alerts by Email

4. The program will ask for the user's phone number where they would like to receive stock price movement alerts by SMS

    Note: Please ask the user to enter a phone number including a '+' sign and the country area code but no dashes or spaces (e.g. +1 for a U.S. phone followed by the actual phone number)

5. After entering the email address and phone number, the program will present some historical trading information for the stock ticker that was requested, the investment recommendation as well as the stock's price chart (opened in a new web browser window)

6. If at the time of the request, the stock price has moved 5% higher or lower than the previous day's closing price, the user will receive an email and SMS alert with the stock price movement information