import averages
import csv
import datetime
import markets
import numpy as np
import os
import pandas as pd
import rsi
import time

today = datetime.datetime.now().date().isoformat()

indicators = ["rsi", "sma_intersection", "macd_intersection"]

def scan_markets():
    tickers = markets.get_min_mkt_cap()
    for i in tickers:
        rsi_of_interest(i)
        sma_intersections_of_interest(i)
        macd_intersections(i)
        time.sleep(2)

def rsi_of_interest(ticker, min_interest=30, max_interest=70):
    print(f"Calculating RSI For {ticker}...")
    data = rsi.threshold_rsi(ticker, min_interest=min_interest, max_interest=max_interest)
    if data:
        write_data_to_csv(data, "rsi", os.path.join(os.getcwd(), 'rsi'))

def sma_intersections_of_interest(ticker, windows=[20, 50]):
    print(f"Checking Intersections for {ticker}...")
    data = averages.get_sma_intersection(ticker, windows=windows)
    if data:
        write_data_to_csv(data, "sma_intersection", os.path.join(os.getcwd(), 'sma_intersection'))

def macd_intersections(ticker):
    data = averages.get_macd_intersection(ticker)
    if data:
        write_data_to_csv(data, "macd_intersection", os.path.join(os.getcwd(), 'macd_intersection'))

def write_data_to_csv(data, indicator_name, path):
    if not os.path.isdir(path):
        os.makedirs(path)
    csv_cols = data.keys()
    with open(os.path.join(path, f'{indicator_name}_{today}.csv'), 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(data.values())

def read_csv(indicator_name):
    with open(os.path.join(os.getcwd(), indicator_name, f'{indicator_name}_{today}.csv'), 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)   
        rows = [i for i in reader]
        return rows

def add_sentiment(rows, sentiment_dict):
    for i in rows:
        if i[0] not in sentiment_dict:
            sentiment_dict[i[0]] = int(i[3])
        else:
            sentiment_dict[i[0]] += int(i[3])
    return sentiment_dict

def threshold_sentiment(min_thresh, max_thresh):
    sentiment_dict = count_sentiment()
    keys = list(sentiment_dict.keys())
    for i in keys[:]:
        if sentiment_dict[i] < max_thresh or sentiment_dict[i] > min_thresh:
            sentiment_dict.pop(i, None)
    return sentiment_dict

def count_sentiment():
    sentiment_dict = {}
    for i in indicators:
        rows = read_csv(i)
        sentiment_dict = add_sentiment(rows, sentiment_dict)
    return sentiment_dict

def scheduler():
    market_close = datetime.datetime.now().replace(hour=20, minute=0, second=0)
    close_delta = (datetime.datetime.utcnow() - market_close)
    indicators_pulled_today = False
    while close_delta.seconds > 0 and close_delta < 600 and indicators_pulled_today is False:
        scan_markets()
        indicators_pulled_today = True
        print(f"Successfully Pulled Indicators For {today}")

if __name__ == '__main__':
    scan_markets()