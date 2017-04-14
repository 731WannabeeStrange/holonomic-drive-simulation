import matplotlib.pyplot as plt
import numpy as np
import math
import csv

time = []
counts = []

with open('2017-04-14-01:08-shooter.csv', newline='') as csvfile:
    csv_file = csv.reader(csvfile)
    for row in csv_file:
        time.append(float(row[0]) * 1000)
        counts.append(float(row[1]))

plt.plot(time, counts, 'b-')
plt.ylabel('cpns')
plt.xlabel('time')

plt.show()
