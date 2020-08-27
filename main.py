import averages
import csv
import datetime
import markets
import numpy as np
import os
import rsi
import time

today = datetime.datetime.now().date().isoformat()

def scan_markets():
    tickers = markets.get_min_mkt_cap()
    for i in tickers:
        rsi_of_interest(i)
        sma_intersections_of_interest(i)
        time.sleep(2)

def rsi_of_interest(ticker, min_interest=30, max_interest=70):
    print(f"Calculating RSI For {ticker}...")
    data = rsi.get_rsi_dataframe(f"{ticker}")
    rsi_vals = data.tail()['RSI'].iloc[-1] if data is not None else 50
    rounded = np.round(rsi_vals , 2)
    if rounded > 70 or rounded < 30:
        write_data_to_csv(ticker, rounded, "rsi", os.path.join(os.getcwd(), 'rsi'))

def sma_intersections_of_interest(ticker, windows=[20, 50]):
    print(f"Checking Intersections for {ticker}...")
    data = averages.get_intersection(ticker, windows=windows)
    if data:
        write_data_to_csv(ticker, data, "sma_intersection", os.path.join(os.getcwd(), 'sma_intersection'))

def write_data_to_csv(ticker, data, indicator_name, path):
    if not os.path.isdir(path):
        os.makedirs(path)
    with open(os.path.join(path, f'{indicator_name}_{today}.csv'), 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([f'{ticker}', f'{data}'])

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
