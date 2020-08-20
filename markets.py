from get_all_tickers import get_tickers
from get_all_tickers import Region

def get_nyse():
    nyse_tickers = get_tickers.get_tickers(NYSE=True, NASDAQ=False, AMEX=False)
    return nyse_tickers

def get_nasdaq():
    nasdaq_tickers = get_tickers.get_tickers(NYSE=False, NASDAQ=True, AMEX=False)
    return nasdaq_tickers

def get_amex():
    amex_tickers = get_tickers.get_tickers(NYSE=False, NASDAQ=False, AMEX=True)
    return amex_tickers

def get_min_mkt_cap(mkt_cap=1000):
    tickers = get_tickers.get_tickers_filtered(mktcap_min=mkt_cap)
    return sorted(tickers)

if __name__ == '__main__':
    nasdaq = get_nasdaq()