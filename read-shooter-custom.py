import matplotlib.pyplot as plt
import numpy as np
import math
import csv

actual = []
time = []
counts = []

with open('2017-04-14-01:08-shooter.csv', newline='') as csvfile:
    csv_file = csv.reader(csvfile)
    for row in csv_file:
        time.append(float(row[0]) * 1000)
        actual.append(float(row[0]))
        counts.append(float(row[1]))

def derivative(values, time, sample_size):
    loop_counter = 0
    count_list = [0 for i in range(sample_size)]
    time_list = [0 for i in range(sample_size)]
    derivs = []

    for i, value in enumerate(counts):
        d = 0
        if count_list[loop_counter] != 0 and time_list[loop_counter] != 0:
            denom = time[i] - time_list[0]
            num = counts[i] - count_list[0]
            d = num / denom
            for j, tv in enumerate(time_list):
                if j != len(time_list) - 1:
                    time_list[j] = time_list[j + 1]

            for k, cv in enumerate(count_list):
                if k != len(count_list) - 1:
                    count_list[k] = count_list[k + 1]

            time_list[sample_size - 1] = time[i]
            count_list[sample_size - 1] = counts[i]

        derivs.append(d)
        if time_list[loop_counter] == 0:
            time_list[loop_counter] = time[loop_counter]

        if count_list[loop_counter] == 0:
            count_list[loop_counter] = counts[loop_counter]

        if loop_counter < sample_size - 1:
            loop_counter += 1

    return derivs

derivs = derivative(counts, time, 20)

plt.plot(actual, derivs, 'b-')
plt.ylabel('cpns')
plt.xlabel('time')

plt.show()
