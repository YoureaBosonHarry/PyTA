import datetime
import matplotlib.pyplot as plt
import pandas as pd
import stock_data

fourteen_days_ago = datetime.datetime.today() - datetime.timedelta(days=14)

def get_volume(ticker, start=fourteen_days_ago, end=stock_data.today):
    data = stock_data.get_dataframe_by_ticker(ticker, start_time=fourteen_days_ago, end_time=stock_data.today)
    plt.plot(data['Date'], data['Volume'])
    plt.show()

get_volume("BMRN")