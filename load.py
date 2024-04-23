'''loads the data into the database'''

import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection
from utilities import get_company_name


def get_connection(host: str, db_name: str, password: str, user: str) -> connection:
    '''Connects to the database'''
    try:
        conn = psycopg2.connect(host=host,
                                dbname=db_name,
                                password=password,
                                user=user,
                                cursor_factory=RealDictCursor)
        return conn
    except psycopg2.Error as e:
        print(f"Error {e} occured!")
        return None


def reorder_data(dataframe, symbol_id):
    '''reorders data to allow symbol_id in'''
    dataframe['Company_id'] = symbol_id
    dataframe = dataframe[['Company_id', 'Date', 'Opening_Price',
                           'High', 'Low', 'Closing_Price', 'Adj Close', 'Volume']]
    return dataframe


def set_schema_path(conn: connection, schema: str):
    '''function to set schema'''
    with conn.cursor() as cur:
        cur.execute("SET search_path TO %s", (schema,))
    conn.commit()


def load_single_company_info(conn: connection, company_details: list[str]):
    '''add one company info into the company table'''
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO company (symbol,company_name)
                    VALUES (%s,%s) ON CONFLICT DO NOTHING""", company_details)
    conn.commit()


def load_data_into_prices(conn: connection, data, symbol: str):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT company_id FROM company WHERE symbol = %s", (symbol,))
        command_result = cur.fetchone()
        symbol_id = command_result['company_id']
        data = reorder_data(data, symbol_id)
        data_tuples = [tuple(row) for row in data.values]
        cur.executemany("""INSERT INTO prices (company_id, price_date, open_price,high,
                        low, close_price, adj_close_price, volume) VALUES
                        (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""",
                        data_tuples)
    conn.commit()


def load(new_conn: connection, data, stock_symbol, schema_name):
    '''function to load to psql'''
    company_info = [stock_symbol, get_company_name(stock_symbol)]
    set_schema_path(new_conn, schema_name)
    load_single_company_info(new_conn, company_info)
    load_data_into_prices(new_conn, data, stock_symbol)
