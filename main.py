import yfinance as yf
import numpy as np
import streamlit as st
import pandas as pd


def load_data(stock: str) -> pd.DataFrame:
    '''load the data to a dataframe to use within the code'''
    data = yf.download(stock, "2023-01-01", "2024-01-01")
    data.reset_index(inplace=True)
    return data


def retrieve_dates():
    '''function to get what dates to use'''
    pass


def main():
    '''function to run everything'''
    st.write(load_data('KO').tail())


if __name__ == "__main__":

    main()
