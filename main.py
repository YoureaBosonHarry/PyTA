import csv
import markets
import numpy as np
import rsi
import time

def scan_markets():
    tickers = markets.get_min_mkt_cap()
    for i in tickers:
        print(f"Calculating RSI For {i}...")
        data = rsi.get_rsi_dataframe(f"{i}")
        rsi_vals = data.tail()['RSI'].iloc[-1] if data is not None else 50
        rounded = np.round(rsi_vals , 2)
        if rounded > 70 or rounded < 30:
            write_rsi_to_csv(i, rounded)
        time.sleep(2)

def write_rsi_to_csv(ticker, rsi):
    with open(f'rsi_{today}.csv', 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([f'{ticker}', f'{rsi}'])

if __name__ == '__main__':
    scan_markets()
