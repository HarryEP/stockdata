'''data to show findings'''

import os
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
# import psycopg2
from psycopg2.extensions import connection
from load import get_connection
# from extract import get_end_date, get_start_date


def choose_companies(conn: connection, schema_name: str) -> list[str]:
    '''allows you to select the companies you want to analyse in streamlit'''
    with conn.cursor() as cur:
        cur.execute("SET search_path TO %s", (schema_name,))
        cur.execute("SELECT company_id, symbol FROM company")
        companies = cur.fetchall()
        symbols = [company['symbol'] for company in companies]
    selected_companies = st.sidebar.multiselect('Select companies: ', symbols)
    return selected_companies


def retrieve_data(conn: connection, selected_companies) -> pd.DataFrame:
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
        return new_df


def plot_grouped_line_graph(grouped_data, x_data_desc, y_data_desc,
                            x_lab, y_lab, graph_title):
    '''to plot each line graph'''
    plt.figure(figsize=(10, 6))
    for symbol, data in grouped_data:
        plt.plot(data[x_data_desc], data[y_data_desc], label=symbol)
    plt.xlabel(x_lab)
    plt.ylabel(y_lab)
    plt.title(graph_title)
    plt.legend()
    st.pyplot(plt)


def main():
    '''function to run everything in one'''
    load_dotenv()
    new_conn = get_connection(os.environ["DB_HOST"], os.environ["DB_NAME"],
                              os.environ["DB_PASS"], os.environ["DB_USER"])
    companies = choose_companies(new_conn, os.environ["SCHEMA"])
    df = retrieve_data(new_conn, companies)
    # start = get_start_date()
    # end = get_end_date(start)
    group_df = df.groupby('symbol')
    plot_grouped_line_graph(group_df, 'price_date', 'close_price',
                            'Price Date', 'Close Price', 'Close Price Over Time')


if __name__ == "__main__":

    main()
