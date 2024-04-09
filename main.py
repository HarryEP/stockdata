'''gets stock data from yahoo finance'''

from datetime import date
import yfinance as yf
import numpy as np
import streamlit as st
import pandas as pd

TODAY = date.today().strftime("%Y-%m-%d")


def load_data(stock: str, start: date, end: date) -> pd.DataFrame:
    '''load the data to a dataframe to use within the code'''
    data = yf.download(stock, start, end)
    data.reset_index(inplace=True)
    return data


def choose_stock():
    '''function to select a certain stock'''
    pass


def get_start_date() -> date:
    '''function to get and validate a start date'''
    poss_date = st.sidebar.date_input('start date:')
    if poss_date >= TODAY:
        return TODAY
    return poss_date


def get_end_date(start: date) -> date:
    '''function to get and validate a start date'''
    poss_date = st.sidebar.date_input('start date:')
    if poss_date <= start:
        return start
    if poss_date > TODAY:
        return TODAY
    return poss_date


def main():
    '''function to run everything'''
    start_date = get_start_date()
    end_date = get_end_date(start_date)
    st.write(load_data('KO', start_date, end_date).tail())


if __name__ == "__main__":

    main()
