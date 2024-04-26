'''gets stock data from yahoo finance'''

import datetime
import yfinance as yf
import pandas as pd

TODAY = datetime.date.today()
LAST_YEAR_DATE = TODAY - datetime.timedelta(days=365)


def retrieve_price_data(stock: str, start: datetime.date, end: datetime.date) -> pd.DataFrame:
    '''retrieve the data for the stock code'''
    data = yf.download(stock, start, end)
    data.reset_index(inplace=True)
    return data


def choose_stock() -> str:
    '''function to select a certain stock'''
    stock = input('what stock code do you want to check?: ')
    if stock == '' or stock is None:
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
        print(
            f"invalid input - input is {LAST_YEAR_DATE}")
        return LAST_YEAR_DATE


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
        print(f"invalid input - input is {TODAY}")
        return TODAY


def get_date_choice():
    '''allows the user to choice to add via dates.'''
    user_input = input("Do you want to manually add dates: (Y/N): ")
    if user_input == 'Y' or user_input == 'y':
        return True
    if user_input == 'N' or user_input == 'n':
        return False
    print("invalid input - returning False")
    return False


def extract() -> list:
    '''function to run everything'''
    manual_date_input = get_date_choice()
    if manual_date_input:
        start_date = get_start_date()
        end_date = get_end_date(start_date)
    else:
        start_date = LAST_YEAR_DATE
        end_date = TODAY
    stock_name = choose_stock()
    data = retrieve_price_data(stock_name, start_date, end_date)
    return stock_name, data


if __name__ == "__main__":

    extract()
