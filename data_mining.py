import datetime as dt
import pandas_datareader.data as web
import requests
import bs4
import pickle
import os
import pandas as pd
from datetime import timedelta


# using web scrawling to get SP500 companies' ticker, store them in sp500ticker.pickle
def save_sp500_tickers():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'}
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies', headers=headers)
    soup = bs4.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text.strip('\n')
        if '.' in ticker:
            ticker = ticker.replace('.', '-')
        tickers.append(ticker)

    with open("sp500tickers.pickle", "wb") as f:  # serializes Python objects for us
        pickle.dump(tickers, f)

    return tickers


# base on sp500ticker, get all 500 stocks info, and store them into stock_dfs in .csv
def retrieve_sp500_stocks(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)  # load data in f to tickers
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    end = dt.datetime.now()
    start = dt.datetime(end.year-1, end.month, end.day)

    for ticker in tickers:
        # just in case connection breaks
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            retrieve_a_stock(ticker, start, end)
    print("End")


# input start date, end date and stock name(sticker)
# output a csv file about that company (including high, low, open ,close, volume)
def retrieve_a_stock(ticker, start, end):
    df = web.DataReader(ticker, 'yahoo', start, end)
    df.reset_index(inplace=True)
    df.set_index("Date", inplace=True)  # set Date as file index
    file = "stock_dfs/" + ticker + ".csv"
    df.to_csv(file)  # save data frame to .csv


def check_df_update(ticker):
    file = "stock_dfs/" + ticker + ".csv"
    df = pd.read_csv(file)
    record_num = df['Date'].count()
    start = df['Date'][record_num - 1].split("-")
    start = dt.datetime(int(start[0]), int(start[1]), int(start[2]))
    end = dt.datetime.now().date()
    start = start + timedelta(days=2)
    start = start.date()
    # check if the record is up-to-date
    tmp = end + timedelta(days=1)
    if tmp == start:
        return

    if start.year != end.year or start.month != end.month or start.day != end.day:
        df2 = web.DataReader(ticker, 'yahoo', start, end)
        df2.reset_index(inplace=True)
        df2.set_index("Date", inplace=True)
        df2.to_csv(file, mode='a', header=False)


def check_exist(ticker):
    if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
        end = dt.datetime.now()
        start = dt.datetime(end.year - 1, end.month, end.day)
        retrieve_a_stock(ticker, start, end)

