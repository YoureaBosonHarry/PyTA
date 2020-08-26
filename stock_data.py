import datetime
import pandas as pd
import pandas_datareader.data as web
import time

current_year = datetime.datetime.now().year
current_month = datetime.datetime.now().month
current_day = datetime.datetime.now().day
two_years_from_today = datetime.datetime(current_year - 2, current_month, current_day)
today = datetime.datetime.now().date().isoformat()

def get_dataframe_by_ticker(ticker, start_time=two_years_from_today, end_time=today):
    try:
        ticker_df = web.get_data_yahoo(ticker, start=start_time, end=end_time)
        print(f"Retrieved data for {ticker}")
        return ticker_df.reset_index()
    except:
        print(f"Failed to retrieve data for {ticker}")
        time.sleep(5)
        return None


