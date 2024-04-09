'''gets stock data from yahoo finance'''

import datetime
import yfinance as yf
import numpy as np
import streamlit as st
import pandas as pd

TODAY = datetime.date.today()


def load_data(stock: str, start: datetime.date, end: datetime.date) -> pd.DataFrame:
    '''load the data to a dataframe to use within the code'''
    data = yf.download(stock, start, end)
    data.reset_index(inplace=True)
    return data


def choose_stock() -> str:
    '''function to select a certain stock'''
    return 'KO'


def get_start_date() -> datetime.date:
    '''function to get and validate a start date'''
    poss_date = st.sidebar.date_input('start date:', key='start')
    print(type(poss_date))
    print(type(TODAY))
    if poss_date > TODAY:
        return TODAY
    return poss_date


def get_end_date(start: datetime.date) -> datetime.date:
    '''function to get and validate a start date'''
    poss_date = st.sidebar.date_input('end date:', key='end')
    if poss_date < start:
        return start
    if poss_date > TODAY:
        return TODAY
    return poss_date


def main():
    '''function to run everything'''
    start_date = get_start_date()
    end_date = get_end_date(start_date)
    st.write(load_data(choose_stock(), start_date, end_date).tail())


if __name__ == "__main__":

    main()
