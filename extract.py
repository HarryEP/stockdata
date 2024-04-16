'''gets stock data from yahoo finance'''

import datetime
import yfinance as yf
import pandas as pd
from dotenv import load_dotenv

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
    try:
        start_date = datetime.datetime.strptime(poss_date, '%Y-%m-%d').date()
        if start_date > TODAY:
            return TODAY
        return start_date
    except:
        print("invalid input - try again")
        get_start_date()


def get_end_date(start: datetime.date) -> datetime.date:
    '''function to get and validate a start date'''
    poss_date = input('end date in "YYYY-MM-DD" please: ')
    try:
        end_date = datetime.datetime.strptime(poss_date, '%Y-%m-%d').date()
        if end_date < start:
            return start
        if end_date > TODAY:
            return TODAY
        return end_date
    except:
        print("invalid input - try again")
        get_end_date()


def extract() -> list:
    '''function to run everything'''
    start_date = get_start_date()
    end_date = get_end_date(start_date)
    data = retrieve_data(choose_stock(), start_date, end_date)
    print(data)
    return data


def clean(data):
    '''cleans the data ready to load it'''
    data['Date'] = pd.to_datetime(data['Date'])
    data.rename(columns={'Close': 'Closing_Price'}, inplace=True)
    data.rename(columns={'Open': 'Opening_Price'}, inplace=True)
    return data


def get_connection(host: str, db_name: str, user: str):
    '''Connects to the database'''
    pass


def load():
    '''function to load to psql'''
    pass


def main():

    data = extract()
    cleaned_data = clean(data)
    print(cleaned_data)


if __name__ == "__main__":

    main()
