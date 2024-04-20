'''module to run everything at once.'''

import os
from dotenv import load_dotenv
from extract import extract
from transform import clean
from load import get_connection, load


def main():
    '''the function to run everything in'''
    ticker, data = extract()
    cleaned_data = clean(data)
    load_dotenv()
    connection = get_connection(os.environ["DB_HOST"], os.environ["DB_NAME"],
                                os.environ["DB_PASS"], os.environ["DB_USER"])

    load(connection, cleaned_data, ticker, os.environ["SCHEMA"])


if __name__ == "__main__":
    main()
