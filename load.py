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
    except Exception as e:
        print(f"Error {e} occured!")


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
