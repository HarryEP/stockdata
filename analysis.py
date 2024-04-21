'''data to show findings'''

import os
from dotenv import load_dotenv
import streamlit as st
import psycopg2
from psycopg2.extensions import connection
from load import get_connection


def choose_companies(conn: connection):
    with conn.cursor() as cur:
        cur.execute("SET search_path TO pricing")
        cur.execute("SELECT company_id, symbol FROM company")
        companies = cur.fetchall()
        # [RealDictRow([('company_id', 1), ('symbol', 'KO')]), RealDictRow([('company_id', 2), ('symbol', 'AAPL')]), RealDictRow([('company_id', 3), ('symbol', 'MSFT')])]
        symbols = []
        for company in companies:
            symbols.append(company['symbol'])
        print(symbols)
    st.sidebar.multiselect('Select companies: ', symbols)


def main():

    load_dotenv()
    new_conn = get_connection(os.environ["DB_HOST"], os.environ["DB_NAME"],
                              os.environ["DB_PASS"], os.environ["DB_USER"])
    choose_companies(new_conn)


if __name__ == "__main__":

    main()
