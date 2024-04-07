import yfinance as yf
import numpy as np
import streamlit as st
import pandas as pd


def load_data(stock: str) -> pd.DataFrame:
    data = yf.download(stock, "2023-01-01", "2024-01-01")
    data.reset_index(inplace=True)
    return data


if __name__ == "__main__":
    st.write(load_data('KO').tail())
