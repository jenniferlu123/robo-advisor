# robo-advisor

# Introduction:  

The goal of this python application is to automate the process of providing clients or users with stock trading recommendations. Specifically, users will be able to enter one or more stock or cryptocurrency symbols (tickers) and provide historical trading data as well as a recommendation as to whether or not the user should buy the given stocks or cryptocurrencies.  

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

## Email template set up

If you are interested in using this program's email capabilities to send out receipts to customers, please set up an account at [Sendgrid] (https://signup.sendgrid.com/), and obtain a Sendgrid. Then, please update the ".env" file using your Sendgrid API key and email address (the one you used to set up the Sendgrid account): 

    SENDGRID_API_KEY="EXAMPLE" 
    MY_EMAIL_ADDRESS="EXAMPLE" 

## SMS template set up

If you are interested in using this program's SMS capabilities to send stock price movement alert messages, please set up an account at [Twilio](https://www.twilio.com/try-twilio), and obtain an Twilio Account SID, Twilio Auth Token, and Twilio phone number to send out SMS messages. Then, please update the following three credentials in ".env" file : 

    TWILIO_ACCOUNT_SID="EXAMPLE"
    TWILIO_AUTH_TOKEN="EXAMPLE"
    SENDER_SMS="+11234567891" # no dashes or spaces, but do include a '+' sign and country area code at the begining (e.g. +1 for a U.S. phone followed by the actual phone number 1234567891)


# Usage:

Run the python script:

```py
python app/robo_advisor.py
```

## Overview of the "steps" of the robo-advisor program:

1. Enter your stock ticker(s). If you have multiple tickers, type one at a time, and press the 'ENTER' key to enter the next one

2. After you have entered all the tickers, enter DONE

3. The program will ask for user's email address where they would like to receive stock price movement alerts by Email

4. The program will ask for the user's phone number where they would like to receive stock price movement alerts by SMS

    Note: Please ask the user to enter a phone number including a '+' sign and the country area code but no dashes or spaces (e.g. +1 for a U.S. phone followed by the actual phone number)

5. After entering the email address and phone number, the program will present some historical trading information for the stock ticker that was requested as well as a live stock price chart (opening a new web browser window)

6. If at the time of the request, the stock price has moved 5% higher or lower than the previous days' closing price, the user will receive an email and SMS alert with the stock price movement information