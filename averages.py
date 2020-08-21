import datetime
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import stock_data

# When short-term crosses above long-term we get a buy signal.
# When short-term passes below the longer-term we get a sell signal.

def sma(ticker, rolling_windows=[20, 50], hide_price=False, graph_path=os.path.join(os.getcwd(), "sma")):
    data = stock_data.get_dataframe_by_ticker(ticker)
    rolling_means = [data['Adj Close'].rolling(window=i).mean() for i in rolling_windows]
    for i, rolling_mean in enumerate(rolling_means):
        plt.plot(data['Date'], rolling_mean, label=f'{ticker} {rolling_windows[i]} Simple Moving Average')
    if hide_price is False:
        plt.plot(data['Date'], data['Adj Close'], label=f'{ticker} {max(rolling_windows)} Price', color='magenta')
    plt.legend(loc='upper left')
    try:
        plt.savefig(os.path.join(graph_path, f'{ticker}_{datetime.datetime.now().date().isoformat()}.png'), format='png')
    except FileNotFoundError:
        os.makedirs(graph_path)
        plt.savefig(os.path.join(graph_path, f'{ticker}_{datetime.datetime.now().date().isoformat()}.png'), format='png')
        
def ema(ticker, rolling_windows=[20, 50], hide_price=False, graph_path=os.path.join(os.getcwd(), "ema")):
    data = stock_data.get_dataframe_by_ticker(ticker)
    exp_means = [data['Adj Close'].ewm(span=i, adjust=False).mean() for i in rolling_windows]
    for i, exp_mean in enumerate(exp_means):
        plt.plot(data['Date'], exp_mean,  label=f'{ticker} {rolling_windows[i]} Exponential Moving Average')
    if hide_price is False:
        plt.plot(data['Date'], data['Adj Close'], label=f'{ticker} {max(rolling_windows)} Price', color='magenta')
    plt.legend(loc='upper left')
    try:
        plt.savefig(os.path.join(graph_path, f'{ticker}_{datetime.datetime.now().date().isoformat()}.png'), format="png")
    except FileNotFoundError:
        os.makedirs(graph_path)
        plt.savefig(os.path.join(graph_path, f'{ticker}_{datetime.datetime.now().date().isoformat()}.png'), format="png")

def check_for_cross(ticker, windows={"short": 20, "long": 50}):
    data = stock_data.get_dataframe_by_ticker(ticker)
    short_term_mean = data['Adj Close'].rolling(window=windows['short']).mean()
    long_term_mean = data['Adj Close'].rolling(window=windows['long']).mean()

