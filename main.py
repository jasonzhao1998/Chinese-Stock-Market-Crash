import matplotlib.pyplot as plt
import csv
import os

# change file name, only in csv format
fileName = '600010'

# initialize data lists
dates = []
openingPrices = []
closingPrices = []
highestPrices = []
lowestPrices = []
percentGain = []
percentShortsell = []
percentMargin = []

with open(fileName + '.csv', 'r') as csvfile:
  plots = csv.reader(csvfile, delimiter=',')
  for count, row in enumerate(plots):
    if count == 0: # skips first row
      continue
    
    dates.append(count)
    closingPrices.append(float(row[10]))
    openingPrices.append(float(row[13]))
    highestPrices.append(float(row[11]))
    lowestPrices.append(float(row[12]))
    
    # margin trading percentage
    if float(row[19]) == 0:
      percentMargin.append(0)
    else:
      percentMargin.append(float(row[2]) / float(row[19]))
    
    # shortsell percentage
    if float(row[18]) == 0:
      percentShortsell.append(0)
    else:
      percentShortsell.append(float(row[5]) / float(row[18]))
    
    # 0 percent gain for empty entry
    if len(row[16]):
      percentGain.append(100 * float(row[16]))
    else:
      percentGain.append(0)

# create directory if does not exist
if not os.path.exists(fileName):
  os.mkdir(fileName)

# resizes plots
plt.rcParams["figure.figsize"] = [24, 5]

plt.plot(dates, closingPrices)
plt.xlabel('Dates')
plt.ylabel('Prices')
plt.title('Closing Prices')
plt.savefig(fileName + '/closingPrices.png')
plt.clf()

plt.plot(dates, highestPrices)
plt.xlabel('Dates')
plt.ylabel('Prices')
plt.title('Highest Prices')
plt.savefig(fileName + '/highestPrices.png')
plt.clf()

plt.plot(dates, lowestPrices)
plt.xlabel('Dates')
plt.ylabel('Prices')
plt.title('Lowest Prices')
plt.savefig(fileName + '/lowestPrices.png')
plt.clf()

plt.plot(dates, openingPrices)
plt.xlabel('Dates')
plt.ylabel('Prices')
plt.title('Opening Prices')
plt.savefig(fileName + '/openingPrices.png')
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
