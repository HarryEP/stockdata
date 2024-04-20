'''transforms/cleans the data'''

import pandas as pd


def clean(data):
    '''cleans the data ready to load it'''
    data['Date'] = pd.to_datetime(data['Date'])
    data.rename(columns={'Close': 'Closing_Price'}, inplace=True)
    data.rename(columns={'Open': 'Opening_Price'}, inplace=True)
    return data
