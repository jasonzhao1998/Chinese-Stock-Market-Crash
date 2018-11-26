import matplotlib.pyplot as plt

import datetime

import matplotlib.dates as dt

import csv

import os

# change file name, only in csv format

fileName = '600010'

# initialize data lists

dates = []

closingPrices = []

percentGain = []

percentShortsell = []

percentMargin = []

ratioShortsell = []

ratioMargin = []

with open(fileName + '.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')

    for row in plots:

        if row[8] == 'date':  # skip first row

            continue

        # date

        curDate = row[8].split('-')

        curDate = [int(i) for i in curDate]

        if curDate[0] < 2014 or curDate[0] > 2015:

            continue

        elif curDate[0] == 2014 and curDate[1] < 10:

            continue

        dates.append(datetime.datetime(curDate[0], curDate[1], curDate[2]))

        # closing prices

        closingPrices.append(float(row[10]))

        # 0 percent gain for empty entry

        if len(row[16]):

            percentGain.append(float(row[16]))

        else:

            percentGain.append(0)

        # shortsell percentage

        if float(row[18]) == 0:

            percentShortsell.append(0)

        else:

            percentShortsell.append(500 * float(row[5]) / float(row[18]))

        # margin trading percentage

        if float(row[19]) == 0:

            percentMargin.append(0)

        else:

            percentMargin.append(float(row[2]) / float(row[19]))

        # shortsell ratio

        if float(row[7]) == 0:

            ratioShortsell.append(0)

        else:

            rate = float(row[6]) / float(row[7])

            ratioShortsell.append(rate)

        # margin trading ratio

        if float(row[4]) == 0:

            ratioMargin.append(0)

        else:

            ratioMargin.append(float(row[3]) / float(row[4]))

# create directory if does not exist

if not os.path.exists(fileName):
    os.mkdir(fileName)

# resize plots

plt.rcParams["figure.figsize"] = [25, 6]

plt.plot(dates, closingPrices)

plt.xlabel('Dates')

plt.ylabel('Prices')

plt.title('Closing Prices')

plt.savefig(fileName + '/closingPrices.png')

plt.clf()

plt.plot(dates, percentGain)

plt.xlabel('Dates')

plt.ylabel('Percent Gain')

plt.title('Percent Gain')

plt.savefig(fileName + '/percentGain.png')

plt.clf()

plt.plot(dates, percentShortsell)

plt.xlabel('Dates')

plt.ylabel('Percent Shortsell')

plt.title('Percent Shortsell')

plt.savefig(fileName + '/percentShortsell.png')

plt.clf()

plt.plot(dates, percentMargin)

plt.xlabel('Dates')

plt.ylabel('Percent Margin')

plt.title('Percent Margin')

plt.savefig(fileName + '/percentMargin.png')

plt.clf()

plt.yscale('log')

plt.plot(dates, ratioShortsell)

plt.xlabel('Dates')

plt.ylabel('Ratio Shortshell')

plt.title('Ratio Shortshell')

plt.savefig(fileName + '/ratioShortsell.png')

plt.clf()

plt.plot(dates, ratioMargin)

plt.xlabel('Dates')

plt.ylabel('Ratio Margin')

plt.title('Ratio Margin')

plt.savefig(fileName + '/ratioMargin.png')

plt.clf()


plt.plot(dates, percentMargin, '-b', label='% Margin')
plt.plot(dates, closingPrices, '-r', label='Closing Prices')

plt.xlabel('Dates')

plt.ylabel('% Margin & Closing Prices')

plt.title('% Margin vs. Closing Prices')

plt.legend(loc='upper left')

plt.savefig(fileName + '/marginVsClosingPrice.png')

plt.clf()



plt.plot(dates, percentShortsell, '-b', label='% Short Sell')
plt.plot(dates, closingPrices, '-r', label='Closing Prices')

plt.xlabel('Dates')

plt.ylabel('% Short & Closing Prices')

plt.title('% Short vs. Closing Prices')

plt.legend(loc='upper left')

plt.savefig(fileName + '/shortVsClosingPrice.png')

plt.clf()