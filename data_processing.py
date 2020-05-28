import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf
import datetime as dt
from datetime import timedelta


def compile_data(tickers):
    main_df = pd.DataFrame()

    for count, ticker in enumerate(tickers):
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        df.set_index('Date', inplace=True)

        df.rename(columns={'Adj Close': ticker}, inplace=True)
        df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace=True)

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')

        if count % 10 == 0:
            print(count)
    print(main_df.head())
    main_df.to_csv('joined_closes.csv')


def advance_graph(stock, mytype, myvolume, mynontrad, mymav, period):
    df = pd.read_csv("stock_dfs/" + stock + ".csv", parse_dates=True, index_col=0).tail(period)
    myfig = mpf.plot(df, type=mytype, returnfig=True, volume=myvolume,
                     show_nontrading=mynontrad, mav=mymav)
    myfig = myfig[0]
    return myfig


def gen_heatmap(tickers):
    compile_data(tickers)
    df = pd.read_csv('joined_closes.csv')
    df_corr = df.corr()  # build correlation
    df_corr.to_csv('corr.csv')

    myfig = plt.figure(figsize=(20, 10), dpi=80, facecolor='w', edgecolor='k')
    data1 = df_corr.values  # an array of corr value
    ax1 = myfig.add_subplot(111)  # create a 1 x1 grid
    heatmap1 = ax1.pcolor(data1, cmap=plt.cm.RdYlGn)  # cmap=plt.cm.RdYlGn is the color range
    myfig.colorbar(heatmap1)  # side bar
    ax1.set_xticks(np.arange(data1.shape[1]) + 0.5, minor=False)  # set x axis from 0,1,2 to company name
    ax1.set_yticks(np.arange(data1.shape[0]) + 0.5, minor=False)  # same as above

    ax1.invert_yaxis()  # flip y axis
    ax1.xaxis.tick_top()  # flip x axis

    column_labels = df_corr.columns
    row_labels = df_corr.index
    ax1.set_xticklabels(column_labels)
    ax1.set_yticklabels(row_labels)

    plt.xticks(rotation=90)  # rotate the x axis label
    heatmap1.set_clim(-1, 1)  # set the limit of range
    return myfig


def visualize_data():
    df = pd.read_csv('joined_closes.csv')
    df_corr = df.corr()  # build correlation
    df_corr.to_csv('corr.csv')

    # start doing heatmap
    data1 = df_corr.values  # an array of corr value
    #fig1 = plt.figure(figsize=(20, 10), dpi=80, facecolor='w', edgecolor='k')
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)  # create a 1 x1 grid

    heatmap1 = ax1.pcolor(data1, cmap=plt.cm.RdYlGn)  # cmap=plt.cm.RdYlGn is the color range
    fig1.colorbar(heatmap1)  # side bar

    ax1.set_xticks(np.arange(data1.shape[1]) + 0.5, minor=False)  # set x axis from 0,1,2 to company name
    ax1.set_yticks(np.arange(data1.shape[0]) + 0.5, minor=False)  # same as above

    ax1.invert_yaxis()  # flip y axis
    ax1.xaxis.tick_top()  # flip x axis

    column_labels = df_corr.columns
    row_labels = df_corr.index
    ax1.set_xticklabels(column_labels)
    ax1.set_yticklabels(row_labels)

    plt.xticks(rotation=90)  # rotate the x axis label
    heatmap1.set_clim(-1, 1)  # set the limit of range
    plt.tight_layout()
    plt.show()


def basic(stock, basic_criteria, period):
    myfig = plt.figure()
    a = plt.subplot2grid((7, 6), (0, 0), rowspan=5, colspan=6)
    a2 = plt.subplot2grid((7, 6), (6, 0), rowspan=1, colspan=6, sharex=a)
    a.clear()  # clear current figure

    actual_num = period
    today = dt.datetime.now()
    for i in range(period):
        today = today - timedelta(days=1)
        if today.weekday() == 5 or today.weekday() == 6:
            actual_num -= 1

    df = pd.read_csv("stock_dfs/" + stock + ".csv", parse_dates=True, index_col=0).tail(actual_num)
    for criteria in basic_criteria:

        a.plot(df.index, df[criteria], label=criteria)
    a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3, ncol=2, borderaxespad=0)
    a2.fill_between(df.index, 0, df['Volume'], facecolor="#183A54")
    a.set_title(stock.upper())
    return myfig
