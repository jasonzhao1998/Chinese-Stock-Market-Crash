import matplotlib.pyplot as plt
import csv

dates = []
closingPrices = []
percentGain = []
percentShortSale = []
percentMargin = []

with open('stock1.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        dates.append(float(row[22]))
        closingPrices.append(float(row[10]))
        percentGain.append(float(row[16]))
        percentShortSale.append(float(row[23]))
        percentMargin.append(float(row[24]))

plt.plot(dates, closingPrices)
plt.xlabel('Dates')
plt.ylabel('Prices')
plt.title('Closing Prices')
plt.show()

plt.plot(dates, percentGain)
plt.xlabel('Dates')
plt.ylabel('% Gain')
plt.title('% Gain')
plt.show()

plt.plot(dates, percentShortSale)
plt.xlabel('Dates')
plt.ylabel('% Short Sale')
plt.title('% Short Sale')
plt.show()

plt.plot(dates, percentMargin)
plt.xlabel('Dates')
plt.ylabel('% Margin')
plt.title('% Margin')
plt.show()