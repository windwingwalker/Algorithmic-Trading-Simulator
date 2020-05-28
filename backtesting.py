import pandas as pd


def find_min(mins, i, df):
    min_df = df["Ema_" + str(mins[0])][i]
    for j in range(1, len(mins)):
        min_df = min(min_df, df["Ema_" + str(mins[j])][i])
    return min_df


def find_max(maxs, i, df):
    max_df = df["Ema_" + str(maxs[0])][i]
    for j in range(1, len(maxs)):
        max_df = max(max_df, df["Ema_" + str(maxs[j])][i])
    return max_df


def backtesting(ticker, maxs, mins):
    df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
    maxs = [int(max) for max in maxs]
    mins = [int(min) for min in mins]
    for y in maxs:
        df["Ema_" + str(y)] = round(df['Adj Close'].ewm(span=y, adjust=False).mean(), 2)
    for z in mins:
        df["Ema_" + str(z)] = round(df['Adj Close'].ewm(span=z, adjust=False).mean(), 2)


    #df = df.iloc[60:]

    pos = 0
    num = 0
    percentchange = []

    for i in df.index:
        cmin = find_min(mins, i, df)
        cmax = find_max(maxs, i, df)

        close = df["Adj Close"][i]

        if (cmin > cmax):
            #print("Red White Blue")
            if (pos == 0):
                bp = close
                pos = 1
                print("Buying now at " + str(bp))


        elif (cmin < cmax):
            #print("Blue White Red")
            if (pos == 1):
                pos = 0
                sp = close
                print("Selling now at " + str(sp))
                pc = (sp / bp - 1) * 100
                percentchange.append(pc)
        if (num == df["Adj Close"].count() - 1 and pos == 1):
            pos = 0
            sp = close
            print("Selling now at " + str(sp))
            pc = (sp / bp - 1) * 100
            percentchange.append(pc)

        num += 1

    print(percentchange)

    gains = 0
    ng = 0
    losses = 0
    nl = 0
    totalR = 1

    for i in percentchange:
        if (i > 0):
            gains += i
            ng += 1
        else:
            losses += i
            nl += 1
        totalR = totalR * ((i / 100) + 1)

    totalR = round((totalR - 1) * 100, 2)

    if (ng > 0):
        avgGain = gains / ng
        maxR = str(max(percentchange))
    else:
        avgGain = 0
        maxR = "undefined"

    if (nl > 0):
        avgLoss = losses / nl
        maxL = str(min(percentchange))
        ratio = str(-avgGain / avgLoss)
    else:
        avgLoss = 0
        maxL = "undefined"
        ratio = "inf"

    if (ng > 0 or nl > 0):
        battingAvg = ng / (ng + nl)
    else:
        battingAvg = 0

    print()
    print("Results for " + ticker + " going back to " + str(df.index[0]) + ", Sample size: " + str(ng + nl) + " trades")
    #print("EMAs used: " + str(emasUsed))
    print("EMAs used: " + str(mins) + str(maxs))
    print("Batting Avg: " + str(battingAvg))
    print("Gain/loss ratio: " + ratio)
    print("Average Gain: " + str(avgGain))
    print("Average Loss: " + str(avgLoss))
    print("Max Return: " + maxR)
    print("Max Loss: " + maxL)
    print("Total return over " + str(ng + nl) + " trades: " + str(totalR) + "%")
    return [ng+nl, mins+maxs, battingAvg, ratio, avgGain, avgLoss, maxR, maxL, totalR]
    print()





