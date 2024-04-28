# stockdata

This project fills stock data into a database, analyses it and shows the results.

## Set up

#### Requirements:

Run `pip3 install -r "requirements.txt"`

#### Database:

Load a postgres terminal that is not called 'stockinformation'
Run `\i schema.sql` in your postgres terminal to set up the database (or to reset the database).
This can also be done to reset the database.

## How to run

#### Add to database:

Run `python3 fill_database.py`to add to the database.\
It will ask you for the date range for you to put in. If you don't input anything, it will default to [365 days ago - today].\
Then it will ask you for the stock ticker (please make sure this matches the ticker on yahoo finance). If you don't input anything, it will default to 'KO' (The Coca-Cola Company).\
Repeat for each stock you want in the database as it adds to the database one stock at a time.

#### Running Analysis:

To run the analysis, run `streamlit run analysis.py`

There is a sidebar as follows:\
![Sidebar](https://github.com/HarryEP/stockdata/blob/main/images/sidebar.png)

This allows you to select the stocks you want to see and in what time frame:
Please remember that this is only for the data within the database.

Other outputs will be:\
The close price over time for each stock:\
![Default Price/Time Graph](https://github.com/HarryEP/stockdata/blob/main/images/price_comparison.png)

The Close Price Ratio Graph:\
This is the close price divided by the average price for a stock to see the trend line of said stock.\
![Close Price Ratio Graph](https://github.com/HarryEP/stockdata/blob/main/images/close_price_ratio.png)

### Future updates

Analysing and extracting information about dividends.
Adding automatic updates to the database
More analysis.
Have a stock database and a price database, with intentions to split up later by sector and dividends.
Future prediction models.
