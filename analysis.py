'''data to show findings'''

import os
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
import psycopg2
from psycopg2.extensions import connection
from load import get_connection
from extract import get_end_date, get_start_date


def choose_companies(conn: connection, schema_name: str) -> list[str]:
    with conn.cursor() as cur:
        cur.execute("SET search_path TO %s", (schema_name,))
        cur.execute("SELECT company_id, symbol FROM company")
        companies = cur.fetchall()
        # [RealDictRow([('company_id', 1), ('symbol', 'KO')]), RealDictRow([('company_id', 2), ('symbol', 'AAPL')]), RealDictRow([('company_id', 3), ('symbol', 'MSFT')])]
        symbols = [company['symbol'] for company in companies]
    selected_companies = st.sidebar.multiselect('Select companies: ', symbols)
    return selected_companies


def retrieve_data(conn: connection, selected_companies):
    '''function to use SQL to get all the required data'''
    with conn.cursor() as cur:
        cur.execute('''SELECT c.symbol, p.price_date, p.open_price, p.high, p.low,
                    p.close_price, p.adj_close_price, p.volume
                    FROM prices p
                    JOIN company c ON p.company_id=c.company_id
                    ''')
        data = cur.fetchall()
        # print(data)
        df = pd.DataFrame(data, columns=['symbol', 'price_date', 'open_price', 'high',
                                         'low', 'close_price', 'adj_close_price', 'volume'])
        new_df = df[df['symbol'].isin(selected_companies)]
        print(df)
        st.write(df)
        st.write(new_df)


def main():

    load_dotenv()
    new_conn = get_connection(os.environ["DB_HOST"], os.environ["DB_NAME"],
                              os.environ["DB_PASS"], os.environ["DB_USER"])
    companies = choose_companies(new_conn, os.environ["SCHEMA"])
    start = get_start_date()
    end = get_end_date(start)
    st.write(retrieve_data(new_conn, companies))


if __name__ == "__main__":

    main()
