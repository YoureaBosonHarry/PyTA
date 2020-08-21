import csv
import datetime
import matplotlib.pyplot as plt
import markets
import numpy as np
import pandas as pd
import pandas_datareader.data as web
import stock_data
import time

current_year = datetime.datetime.now().year
current_month = datetime.datetime.now().month
current_day = datetime.datetime.now().day
two_years_from_today = datetime.datetime(current_year - 2, current_month, current_day)
today = datetime.datetime.now().date().isoformat()

def compute_rsi(data, time_window):
    diff = data.diff(1).dropna()
    up_change = 0 * diff
    down_change = 0 * diff

    up_change[diff > 0] = diff[diff > 0]
    down_change[diff < 0] = diff[diff < 0]

    up_change_average = up_change.ewm(com=time_window-1, min_periods=time_window).mean()
    down_change_average = down_change.ewm(com=time_window-1, min_periods=time_window).mean()

    rs = abs(up_change_average/down_change_average)
    rsi = 100 - 100/(1+rs)
    return rsi

def get_rsi_dataframe(ticker, start=two_years_from_today, end=today, time_window=14):
    df = stock_data.get_dataframe_by_ticker(ticker, start, end)
    if df is not None:
        df['RSI'] = compute_rsi(df['Adj Close'], time_window)
    return df

def get_rsi_plot(ticker, start=two_years_from_today, end=today, time_window=14):
    df = stock_data.get_dataframe_by_ticker(ticker, start, end)
    df['RSI'] = compute_rsi(df['Adj Close'], time_window)
    fig, (ax1, ax2) = plt.subplots(2)
    fig.set_figwidth(15)
    fig.set_figheight(5)
    fig.tight_layout(pad=3.0)
    ax1.set_title("Time vs Price")
    ax1.set
    ax1.plot(df['Date'], df['Adj Close'])
    ax2.set_title('RSI chart')
    ax2.plot(df['Date'], df['RSI'])
    ax2.axhline(0, linestyle='--', alpha=0.1)
    ax2.axhline(20, linestyle='--', alpha=0.5)
    ax2.axhline(30, linestyle='--')
    ax2.axhline(70, linestyle='--')
    ax2.axhline(80, linestyle='--', alpha=0.5)
    ax2.axhline(100, linestyle='--', alpha=0.1)
    #plt.savefig(f'{ticker}_RSI.png')
    plt.show()

get_rsi_plot("SLV")