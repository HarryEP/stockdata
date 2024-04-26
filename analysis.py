'''data to show findings'''

import os
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from psycopg2.extensions import connection
from load import get_connection


def choose_companies(conn: connection, schema_name: str) -> list[str]:
    '''allows you to select the companies you want to analyse in streamlit'''
    with conn.cursor() as cur:
        cur.execute("SET search_path TO %s", (schema_name,))
        cur.execute("SELECT company_id, symbol FROM company")
        companies = cur.fetchall()
        symbols = [company['symbol'] for company in companies]
    selected_companies = st.sidebar.multiselect('Select companies: ', symbols)
    return selected_companies


def retrieve_data(conn: connection, selected_companies, start_date, end_date) -> pd.DataFrame:
    '''function to use SQL to get all the required data'''
    with conn.cursor() as cur:
        cur.execute('''SELECT c.symbol, p.price_date, p.open_price, p.high, p.low,
                    p.close_price, p.adj_close_price, p.volume
                    FROM prices p
                    JOIN company c ON p.company_id=c.company_id
                    ''')
        data = cur.fetchall()
        df = pd.DataFrame(data, columns=['symbol', 'price_date', 'open_price', 'high',
                                         'low', 'close_price', 'adj_close_price', 'volume'])
        new_df = df[df['symbol'].isin(selected_companies)]
        new_df = new_df[(new_df['price_date'] >= start_date)]
        new_df = new_df[(new_df['price_date'] <= end_date)]
        return new_df


def plot_grouped_line_graph(parameters: dict):
    '''to plot each line graph'''
    plt.figure(figsize=(10, 6))
    for symbol, data in parameters['grouped_data']:
        plt.plot(data[parameters['x_data_desc']],
                 data[parameters['y_data_desc']], label=symbol)
    plt.xlabel(parameters['x_lab'])
    plt.ylabel(parameters['y_lab'])
    plt.title(parameters['graph_title'])
    plt.legend()
    st.pyplot(plt)


def main():
    '''function to run everything in one'''
    st.title("Analysis of stock market data for certain companies")
    load_dotenv()
    new_conn = get_connection(os.environ["DB_HOST"], os.environ["DB_NAME"],
                              os.environ["DB_PASS"], os.environ["DB_USER"])
    companies = choose_companies(new_conn, os.environ["SCHEMA"])
    start = pd.to_datetime(st.sidebar.date_input('start date: '))
    end = pd.to_datetime(st.sidebar.date_input('end date: '))
    df = retrieve_data(new_conn, companies, start, end)
    group_df = df.groupby('symbol')

    st.write('This graph is to show the price of the stock(s) over time selected.')
    plot_grouped_line_graph({
        'grouped_data': group_df,
        'x_data_desc': 'price_date',
        'y_data_desc': 'close_price',
        'x_lab': 'Price Date',
        'y_lab': 'Close Price',
        'graph_title': 'Close Price Over Time'
    })

    st.write("""This graph is to show the close price over the average price for
             the stock over time.""")
    avg_close = group_df['close_price'].transform('mean')

    plt.figure(figsize=(10, 6))
    for symbol, data in group_df:
        close_price_ratio = data['close_price'] / avg_close[data.index]
        plt.plot(data['price_date'], close_price_ratio, label=symbol)

    plt.xlabel('Price Date')
    plt.ylabel('Close Price Ratio to Average')
    plt.title('Close Price Ratio to Average Over Time')
    plt.legend()
    st.pyplot(plt)


if __name__ == "__main__":

    main()
