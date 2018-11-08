import matplotlib.pyplot as plt
import csv

dates = []
closingPrices = []

with open('stock1.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        dates.append(float(row[22]))
        closingPrices.append(float(row[10]))

plt.plot(dates, closingPrices)
plt.xlabel('Dates')
plt.ylabel('Prices')
plt.title('Closing Prices')
plt.legend()
plt.show()