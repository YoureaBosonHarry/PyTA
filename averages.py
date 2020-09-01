import datetime
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import stock_data

# When short-term crosses above long-term we get a buy signal.
# When short-term passes below the longer-term we get a sell signal.

def sma(ticker, rolling_windows=[20, 50], hide_price=False, bollinger=False, graph_path=os.path.join(os.getcwd(), "sma")):
    data = stock_data.get_dataframe_by_ticker(ticker)[-2*(max(rolling_windows)):]
    rolling_means = [data['Adj Close'].rolling(window=i).mean() for i in rolling_windows]
    for i, rolling_mean in enumerate(rolling_means):
        plt.plot(data['Date'], rolling_mean, label=f'{ticker} {rolling_windows[i]} Simple Moving Average')
    if bollinger is True:
        data = bollinger_bands(data, window=rolling_windows[0])
        plt.plot(data['Date'], data['Lower Bollinger'], label=f'{ticker} {rolling_windows[0]} Lower Bollinger Band')
        plt.plot(data['Date'], data['Upper Bollinger'], label=f'{ticker} {rolling_windows[0]} Upper Bollinger Band')
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

def bollinger_bands(data, window=20):
    moving_average = data['Adj Close'].rolling(window=window).mean()
    std = data['Adj Close'].rolling(window=window).std()
    data['Upper Bollinger'] = moving_average + (2 * std)
    data['Lower Bollinger'] = moving_average - (2 * std)
    return data

def get_sma_intersection(ticker, windows=[20, 50], look_back_time=5):
    data = stock_data.get_dataframe_by_ticker(ticker)
    if data is None or len(data) < min(windows):
        return None
    data[f'{windows[0]} SMA'] = data['Adj Close'].rolling(window=windows[0]).mean()
    data[f'{windows[1]} SMA'] = data['Adj Close'].rolling(window=windows[1]).mean()
    intersections = {}
    for i in range(len(data['Date'][-look_back_time:])):
        if len(data['Date'][:]) - look_back_time + 1 + i < len(data['Date'][:]):
            y11 = data[f'{windows[0]} SMA'][len(data['Date'][:]) - look_back_time + i] # short window n day price
            y21 = data[f'{windows[1]} SMA'][len(data['Date'][:]) - look_back_time + i] # long window n day price
            y12 = data[f'{windows[0]} SMA'][len(data['Date'][:]) - look_back_time + 1 + i] # short window n + 1 price
            y22 = data[f'{windows[1]} SMA'][len(data['Date'][:]) - look_back_time + 1 + i] # long window n + 1 price
            if y11 > y21 and y12 < y22:
                intersections = {"ticker": ticker, "cross_date": data['Date'][len(data['Date'][:]) - look_back_time + 1 + i], "sentiment": "Bearish", "count": -1}
            if y21 > y11 and y22 < y12:
                intersections = {"ticker": ticker, "cross_date": data['Date'][len(data['Date'][:]) - look_back_time + 1 + i], "sentiment": "Bullish", "count": 1}
    return intersections

def graph_macd(ticker, windows=[12, 26], signal_line=9):
    data = stock_data.get_dataframe_by_ticker(ticker)
    if data is None  or len(data) < min(windows):
        return None
    data[f'{windows[0]} ema'] = data['Adj Close'].ewm(span=windows[0], adjust=False, min_periods=1).mean()
    data[f'{windows[1]} ema'] = data['Adj Close'].ewm(span=windows[1], adjust=False, min_periods=1).mean()
    data['MACD'] = data[f'{windows[0]} ema'] - data[f'{windows[1]} ema']
    data[f'signal line'] = data['MACD'].ewm(span=signal_line, adjust=False).mean()
    fig, ax = plt.subplots(1)
    ax.plot(data['Date'][-30:], data['MACD'][-30:], label=f'MACD')
    ax.plot(data['Date'][-30:], data['signal line'][-30:], label=f'Signal Line')
    ax.axhline(0, linestyle='--')
    ax.legend(loc='upper left')
    plt.show()

def get_macd_intersection(ticker, windows=[12, 26], signal_line=9, look_back_time=100):
    data = stock_data.get_dataframe_by_ticker(ticker)
    data[f'{windows[0]} ema'] = data['Adj Close'].ewm(span=windows[0], adjust=False, min_periods=1).mean()
    data[f'{windows[1]} ema'] = data['Adj Close'].ewm(span=windows[1], adjust=False, min_periods=1).mean()
    data['MACD'] = data[f'{windows[0]} ema'] - data[f'{windows[1]} ema']
    data[f'signal line'] = data['MACD'].ewm(span=signal_line, adjust=False).mean()
    if data is None or len(data) < min(windows):
        return None
    intersections = {}
    for i in range(len(data['Date'][-look_back_time:])):
        if len(data['Date'][:]) - look_back_time + 1 + i < len(data['Date'][:]):
            y11 = data[f'MACD'][len(data['Date'][:]) - look_back_time + i] # short window n day price
            y21 = data[f'signal line'][len(data['Date'][:]) - look_back_time + i] # long window n day price
            y12 = data[f'MACD'][len(data['Date'][:]) - look_back_time + 1 + i] # short window n + 1 price
            y22 = data[f'signal line'][len(data['Date'][:]) - look_back_time + 1 + i] # long window n + 1 price
            if y11 > y21 and y12 < y22:
                intersections = {"ticker": ticker, "cross_date": data['Date'][len(data['Date'][:]) - look_back_time + 1 + i], "sentiment": "Bearish", "count": -1}
            if y21 > y11 and y22 < y12:
                intersections = {"ticker": ticker, "cross_date": data['Date'][len(data['Date'][:]) - look_back_time + 1 + i], "sentiment": "Bullish", "count": 1}
    print(intersections)


if __name__ == '__main__':
    get_macd_intersection("TSLA")