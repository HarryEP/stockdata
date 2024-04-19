'''gets stock data from yahoo finance'''

import os
import datetime
import yfinance as yf
import pandas as pd
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection

TODAY = datetime.date.today()


def retrieve_data(stock: str, start: datetime.date, end: datetime.date) -> pd.DataFrame:
    '''retrieve the data for the stock code'''
    data = yf.download(stock, start, end)
    data.reset_index(inplace=True)
    return data


def choose_stock() -> str:
    '''function to select a certain stock'''
    stock = input('what stock code do you want to check?: ')
    if stock == '' or stock is None:
        return 'KO'
    return stock


def get_start_date() -> datetime.date:
    '''function to get and validate a start date'''
    poss_date = input('start date in "YYYY-MM-DD" please: ')
    try:
        start_date = datetime.datetime.strptime(poss_date, '%Y-%m-%d').date()
        if start_date > TODAY:
            return TODAY
        return start_date
    except:
        print("invalid input - try again")
        get_start_date()


def get_end_date(start: datetime.date) -> datetime.date:
    '''function to get and validate a start date'''
    poss_date = input('end date in "YYYY-MM-DD" please: ')
    try:
        end_date = datetime.datetime.strptime(poss_date, '%Y-%m-%d').date()
        if end_date < start:
            return start
        if end_date > TODAY:
            return TODAY
        return end_date
    except:
        print("invalid input - try again")
        get_end_date()


def extract() -> list:
    '''function to run everything'''
    start_date = get_start_date()
    end_date = get_end_date(start_date)
    stock_name = choose_stock()
    data = retrieve_data(stock_name, start_date, end_date)
    print(data)
    return stock_name, data


def clean(data):
    '''cleans the data ready to load it'''
    data['Date'] = pd.to_datetime(data['Date'])
    data.rename(columns={'Close': 'Closing_Price'}, inplace=True)
    data.rename(columns={'Open': 'Opening_Price'}, inplace=True)
    return data


def get_connection(host: str, db_name: str, password: str, user: str) -> connection:
    '''Connects to the database'''
    try:
        conn = psycopg2.connect(host=host,
                                dbname=db_name,
                                password=password,
                                user=user,
                                cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        print(f"Error {e} occured!")


def get_company_name(symbol: str) -> str:
    '''to get company name using the symbol'''
    try:
        ticker = yf.Ticker(symbol)
        stock_info = ticker.info
        return stock_info["longName"]
    except Exception as e:
        print(f'{e} Error occured')
        stock_name = input("Enter stock name manually: ")
        return stock_name


def reorder_data(dataframe, symbol_id):
    '''reorders data to allow symbol_id in'''
    dataframe['Company_id'] = symbol_id
    dataframe = dataframe[['Company_id', 'Date', 'Opening_Price',
                           'High', 'Low', 'Closing_Price', 'Adj Close', 'Volume']]
    return dataframe


def load(new_conn: connection, data, stock_symbol, schema_name):
    '''function to load to psql'''
    company_info = [stock_symbol, get_company_name(stock_symbol)]
    with new_conn.cursor() as cur:
        cur.execute("SET search_path TO %s", (schema_name,))
        cur.execute("""INSERT INTO company (symbol,company_name)
                    VALUES (%s,%s) ON CONFLICT DO NOTHING""", company_info)
        cur.execute(
            "SELECT company_id FROM company WHERE symbol = %s", (stock_symbol,))
        command_result = cur.fetchone()
        symbol_id = command_result['company_id']
        data = reorder_data(data, symbol_id)
        print(data)
        data_tuples = [tuple(row) for row in data.values]
        cur.executemany("""INSERT INTO prices (company_id, price_date, open_price,high,
                        low, close_price, adj_close_price, volume) VALUES
                        (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""",
                        data_tuples)
    new_conn.commit()


def main():
    '''the function to run everything in'''
    ticker, data = extract()
    cleaned_data = clean(data)
    print(cleaned_data)
    load_dotenv()
    connection = get_connection(os.environ["DB_HOST"], os.environ["DB_NAME"],
                                os.environ["DB_PASS"], os.environ["DB_USER"])

    load(connection, cleaned_data, ticker, os.environ["SCHEMA"])


if __name__ == "__main__":

    main()
