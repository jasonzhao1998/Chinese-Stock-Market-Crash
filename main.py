import os
import csv
import datetime
import numpy as np
import matplotlib.dates as dt
import matplotlib.pyplot as plt

# change file name, only in csv format
FILE_NAME = '600111'


def plot(x, y, x_label, y_label, title, log=False):
    if log:
        plt.yscale('log')
    plt.plot(x, y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.savefig(FILE_NAME + '/' + title + '.png')
    plt.clf()


def read_data():
    # initialize lists
    dates = []
    remaining_margin = []
    margin_buy = []
    margin_repay = []
    remaining_shortsell = []
    short_sell = []
    short_repay = []
    closing_prices = []
    percent_gain = []
    turnover_rate = []
    trading_volume = []
    turnover = []

    with open(FILE_NAME + '.csv', 'Ur') as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        for row in data:
            if row[8] == 'date':  # skip first row
                continue

            # date
            cur_date = row[8].split('-')
            cur_date = [int(i) for i in cur_date]
            if cur_date[0] < 2014 or cur_date[0] > 2015:
                continue
            elif cur_date[0] == 2014 and cur_date[1] < 10:
                continue
            dates.append(datetime.datetime(cur_date[0], cur_date[1], cur_date[2]))

            # all other data
            remaining_margin.append(float(row[2]))
            margin_buy.append(float(row[3]))
            margin_repay.append(float(row[4]))
            remaining_shortsell.append(float(row[5]))
            short_sell.append(float(row[6]))
            short_repay.append(float(row[7])) if float(row[7]) != 0 else short_repay.append(0.1)
            closing_prices.append(float(row[10]))
            percent_gain.append(float(row[16]))
            turnover_rate.append(float(row[17]))
            trading_volume.append(float(row[18]))
            turnover.append(float(row[19]))

    return {
        "dates": dates,
        "remaining margin": np.array(remaining_margin, dtype=np.float),
        "margin buy": np.array(margin_buy, dtype=np.float),
        "margin repay": np.array(margin_repay, dtype=np.float),
        "remaining shortsell": np.array(remaining_shortsell, dtype=np.float),
        "short sell": np.array(short_sell, dtype=np.float),
        "short repay": np.array(short_repay, dtype=np.float),
        "closing prices": np.array(closing_prices, dtype=np.float),
        "percent gain": np.array(percent_gain, dtype=np.float),
        "turnover rate": np.array(turnover_rate, dtype=np.float),
        "trading volume": np.array(trading_volume, dtype=np.float),
        "turnover": np.array(turnover, dtype=np.float)
    }


def save_plots(data):
    # create directory if does not exist
    if not os.path.exists(FILE_NAME):
        os.mkdir(FILE_NAME)

    # resize plots
    plt.rcParams["figure.figsize"] = [25, 6]

    plot(data["dates"], data["closing prices"], "Dates", "Prices in yuan", "Closing Prices")
    plot(data["dates"], data["percent gain"], "Dates", "Percent gain", "Percent Gain")

    # margin trading plots
    plot(data["dates"], data["margin buy"] / data["margin repay"], "Dates", "Ratio", "Margin Buy Over Margin Repay")
    plot(data["dates"], data["margin buy"] / data["turnover"], "Dates", "Ratio", "Margin Buy Over Turnover")
    plot(data["dates"], data["margin repay"] / data["turnover"], "Dates", "Ratio", "Margin Repay Over Turnover")

    # short selling plots
    plot(data["dates"], data["short sell"] / data["short repay"], "Dates",
         "Ratio", "Short Sell Over Short Repay", log=True)
    plot(data["dates"], data["short sell"] / data["trading volume"], "Dates", "Ratio", "Short Sell Over Trading Volume")
    plot(data["dates"], data["short repay"] / data["trading volume"], "Dates",
         "Ratio", "Short Repay Over Trading Volume")

    # skipping margin trading plots
    plot(data["dates"][:-30], data["margin buy"][:-30] / data["margin repay"][30:],
         "Dates", "Ratio", "Margin Buy Over Margin Repay in 30 Days")
    plot(data["dates"][:-15], data["margin buy"][:-15] / data["margin repay"][15:],
         "Dates", "Ratio", "Margin Buy Over Margin Repay in 15 Days")
    plot(data["dates"][:-7], data["margin buy"][:-7] / data["margin repay"][7:],
         "Dates", "Ratio", "Margin Buy Over Margin Repay in 7 Days")
    plot(data["dates"][:-3], data["margin buy"][:-3] / data["margin repay"][3:],
         "Dates", "Ratio", "Margin Buy Over Margin Repay in 3 Days")

    # skipping short selling plots
    plot(data["dates"][:-30], data["short sell"][:-30] / data["short repay"][30:], "Dates",
         "Ratio", "Short Sell Over Short Repay in 30 Days", log=True)
    plot(data["dates"][:-15], data["short sell"][:-15] / data["short repay"][15:], "Dates",
         "Ratio", "Short Sell Over Short Repay In 15 Days", log=True)
    plot(data["dates"][:-7], data["short sell"][:-7] / data["short repay"][7:], "Dates",
         "Ratio", "Short Sell Over Short Repay In 7 Days", log=True)
    plot(data["dates"][:-3], data["short sell"][:-3] / data["short repay"][3:], "Dates",
         "Ratio", "Short Sell Over Short Repay In 3 Days", log=True)


def main():
    data = read_data()
    save_plots(data)


if __name__ == '__main__':
    main()
