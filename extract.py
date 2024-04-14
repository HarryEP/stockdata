'''gets stock data from yahoo finance'''

import datetime
import yfinance as yf
import pandas as pd

TODAY = datetime.date.today()


def retrieve_data(stock: str, start: datetime.date, end: datetime.date) -> pd.DataFrame:
    '''retrieve the data for the stock code'''
    data = yf.download(stock, start, end)
    data.reset_index(inplace=True)
    return data


def choose_stock() -> str:
    '''function to select a certain stock'''
    stock = input('what stock code do you want to check?: ')
    if stock == '' or stock == None:
        return 'KO'
    return stock


def get_start_date() -> datetime.date:
    '''function to get and validate a start date'''
    poss_date = input('start date in "YYYY-MM-DD" please: ')
    if poss_date > TODAY:
        return TODAY
    return poss_date


def get_end_date(start: datetime.date) -> datetime.date:
    '''function to get and validate a start date'''
    poss_date = input('end date in "YYYY-MM-DD" please: ')
    if poss_date < start:
        return start
    if poss_date > TODAY:
        return TODAY
    return poss_date


def extract() -> list:
    '''function to run everything'''
    start_date = get_start_date()
    end_date = get_end_date(start_date)
    data = retrieve_data(choose_stock(), start_date, end_date)
    return data


def clean(data):
    '''cleans the data ready to load it'''


if __name__ == "__main__":

    data = extract()
    data = clean(data)


if __name__ == "__main__":

    main()
