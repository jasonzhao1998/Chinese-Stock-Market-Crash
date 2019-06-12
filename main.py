"""Run plots for analysis on dataset."""
import os
import csv
import shutil
import datetime
import numpy as np
import matplotlib.pyplot as plt


# change file name, only in csv format
FILE_NAME = '600111'


def plot(x, y, x_label, y_label, title, log=False, xlim=None, ylim=None, path=''):
    """Helper function for plotting data."""
    if log:
        plt.yscale('log')
    plt.plot(x, y)
    if xlim:
        plt.xlim(xlim[0], xlim[1])
    if ylim:
        plt.ylim(ylim[0], ylim[1])
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    if path:
        if not os.path.exists(FILE_NAME + '/' + path):
            os.mkdir(FILE_NAME + '/' + path)
        path += '/'
    plt.savefig(FILE_NAME + '/' + path + title + '.png')
    plt.clf()


def read_data(date_range):
    """Reads data from a given range of dates stored in a list."""
    # initialize lists
    dates = []
    remaining_margin = []
    margin_buy = []
    margin_repay = []
    remaining_shortsell = []
    short_sell = []
    short_repay = []
    closing_prices = []
    highest_prices = []
    lowest_prices = []
    opening_prices = []
    percent_gain = []
    turnover_rate = []
    trading_volume = []
    turnover = []

    with open(FILE_NAME + '.csv', 'r') as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        for row in data:
            if row[8] == 'date':  # skip first row
                continue

            # date
            cur_date = row[8].split('-')
            cur_date = [int(i) for i in cur_date]
            if cur_date[0] < date_range[0] or cur_date[0] > date_range[2]:
                continue
            elif cur_date[0] == date_range[0] and cur_date[1] < date_range[1]:
                continue
            elif cur_date[0] == date_range[2] and cur_date[1] > date_range[3]:
                continue
            dates.append(datetime.datetime(cur_date[0], cur_date[1], cur_date[2]))

            # all other data
            remaining_margin.append(float(row[2]))
            margin_buy.append(float(row[3]))
            margin_repay.append(float(row[4]))
            remaining_shortsell.append(float(row[5]))
            short_sell.append(float(row[6]))
            if float(row[7]) != 0:
                short_repay.append(float(row[7]))
            else:
                short_repay.append(0.1)
            closing_prices.append(float(row[10]))
            highest_prices.append(float(row[11]))
            lowest_prices.append(float(row[12]))
            opening_prices.append(float(row[13]))
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
        "highest prices": np.array(highest_prices, dtype=np.float),
        "lowest prices": np.array(lowest_prices, dtype=np.float),
        "opening prices": np.array(opening_prices, dtype=np.float),
        "percent gain": np.array(percent_gain, dtype=np.float),
        "turnover rate": np.array(turnover_rate, dtype=np.float),
        "trading volume": np.array(trading_volume, dtype=np.float),
        "turnover": np.array(turnover, dtype=np.float)
    }


def plot_index(dates, ratio, x_label, y_label, title, log=False, xlim=None, ylim=None,
               window_size=5, path=""):
    """Helper function for plotting frequency indices."""
    indices = []
    for i in range(len(ratio) - window_size + 1):
        total = 0
        for j in range(window_size):
            total += ratio[i + j]
        indices.append(total / window_size)
    plot(dates[:-(window_size - 1)], indices, x_label, y_label, title, log, xlim, ylim, path)


def save_index_plots(data):
    # resize plots
    plt.rcParams["figure.figsize"] = [25, 6]
    delay_range = [1, 3, 5, 7, 10, 15, 30]
    for delay in delay_range:
        plot_index(
            data["dates"][delay:], data["short sell"][:-delay] / data["short repay"][delay:],
            "Dates", "Short index", "Short Index with Delay " + str(delay) + " Days", ylim=[0, 3],
            window_size=5, path='short ratio'
        )

    delay_range = [1, 3, 5, 7, 10, 15, 30]
    for delay in delay_range:
        plot_index(
            data["dates"][delay:], data["margin buy"][:-delay] / data["margin repay"][delay:],
            "Dates", "Margin index", "Margin Index with Delay " + str(delay) + " Days",
            ylim=[0, 3], window_size=5, path='margin ratio'
        )


def save_plots(data):
    # resize plots
    plt.rcParams["figure.figsize"] = [25, 6]

    # closing price, percent gain, and short margin ratio
    plot(data["dates"], data["closing prices"], "Dates", "Prices in yuan", "Closing Prices")
    plot(data["dates"], data["percent gain"], "Dates", "Percent gain", "Percent Gain")
    plot(
        data["dates"],
        (data["short sell"] / data["short repay"]) / (data["margin buy"] / data["margin repay"]),
        "Dates", "Ratio", "Short Ratio Over Margin Ratio"
    )

    # margin trading plots
    plot(data["dates"], data["margin buy"] / data["turnover"], "Dates",
         "Ratio", "Margin Buy Over Turnover", path='margin delay')
    plot(data["dates"], data["margin repay"] / data["turnover"], "Dates",
         "Ratio", "Margin Repay Over Turnover", path='margin delay')

    delay_range = [1, 3, 5, 7, 10, 15, 30]
    plot(data["dates"], data["margin buy"] / data["margin repay"], "Dates",
         "Ratio", "Margin Buy Over Margin Repay", path='margin delay')
    for delay in delay_range:
        plot(
            data["dates"][delay:],
            data["margin buy"][:-delay] / data["margin repay"][delay:],
            "Dates", "Ratio", "Margin Buy Over Margin Repay in " + str(delay) + " Days",
            path='margin delay'
        )

    # short selling plots
    plot(data["dates"], data["short sell"] / data["trading volume"], "Dates",
         "Ratio", "Short Sell Over Trading Volume", path='short delay')
    plot(data["dates"], data["short repay"] / data["trading volume"], "Dates",
         "Ratio", "Short Repay Over Trading Volume", path='short delay')

    delay_range = [1, 3, 5, 7, 10, 15, 30]
    for delay in delay_range:
        plot(
            data["dates"][delay:], data["short sell"][:-delay] / data["short repay"][delay:],
            "Dates", "Ratio", "Short Sell Over Short Repay in " + str(delay) + " Days", log=True,
            path='short delay'
        )


def main():
    # create directory if does not exist
    if not os.path.exists(FILE_NAME):
        os.mkdir(FILE_NAME)
    else:
        shutil.rmtree(FILE_NAME)
        os.mkdir(FILE_NAME)

    data = read_data([2014, 11, 2015, 9])
    save_plots(data)
    save_index_plots(data)


if __name__ == '__main__':
    main()
