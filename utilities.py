'''utilities for retrieving information'''

import yfinance as yf


def get_company_name(symbol: str) -> str:
    '''to get company name using the symbol'''
    try:
        ticker = yf.Ticker(symbol)
        stock_info = ticker.info
        return stock_info["longName"]
    except Exception as e:
        print(f'{e} Error occured')
        stock_name = input("Enter stock name manually: ")
        return stock_name
