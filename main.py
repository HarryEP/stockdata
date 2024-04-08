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


def main():
    '''function to run everything'''
    start_date = st.sidebar.date_input('start')
    end_date = st.sidebar.date_input('end')
    st.write(load_data('KO', start_date, end_date).tail())


if __name__ == "__main__":

    main()
