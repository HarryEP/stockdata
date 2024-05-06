'''module to run everything at once in order to fill the database and extract the data'''

import os
from dotenv import load_dotenv
from extract import extract
from transform import clean
from load import get_connection, load


def how_many_inputs() -> int:
    try:
        answer = int(input("How many stocks would you like to input: "))
    except TypeError as e:
        print(f"TypeError {e} occured! Returning 1 as default")
        return 1
    if answer < 1:
        print("Number is too low! Returning 1 as default")
        return 1
    if answer > 5:
        print("Number is too high! Returning 1 as default")
        return 5


def main():
    '''the function to run everything in'''
    number_of_inputs = how_many_inputs()
    for i in range(number_of_inputs):
        ticker, data = extract()
        cleaned_data = clean(data)
        load_dotenv()
        connection = get_connection(os.environ["DB_HOST"], os.environ["DB_NAME"],
                                    os.environ["DB_PASS"], os.environ["DB_USER"])

        load(connection, cleaned_data, ticker, os.environ["SCHEMA"])


if __name__ == "__main__":
    main()
