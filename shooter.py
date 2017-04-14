import matplotlib.pyplot as plt
import numpy as np
import subprocess
import math
import datetime
date_string = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M")
import csv

def clear():
    subprocess.run(['adb', 'logcat', '-c'], stdout=subprocess.PIPE)

def get_log():
    result = subprocess.run(['adb', 'logcat', '-d', '-s', 'auto'], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')

def process_log(log):
    a = []
    b = []
    c = []
    lines = log.split('\n')
    for q, line in enumerate(lines):
        if len(line) != 0:
            if line[0] != '-':
                data = line.split()
                print(data)
                data = data[7:]
                #data[-1] = data[-1][:-1]
                for i, datum in enumerate(data):
                    print(data[i])
                    if i == 0:
                        if 'E' not in data[i]:
                            a.append(float(data[i]))
                        else:
                            a.append(0)
                    elif i == 1:
                        if 'E' not in data[i]:
                            b.append(float(data[i]))
                        else:
                            b.append(0)
                    elif i == 2:
                        if 'E' not in data[i]:
                            c.append(float(data[i]))
                        else:
                            c.append(0)

    return [a, b, c]

def derivative(values, time, smooth):
    derivs = []
    for i, (value, sec) in enumerate(zip(values, time)):
        if i != 0:
            dt = time[i] - time[i - 1]
            if dt == 0:
                if len(derivs) == (i - 1):
                    deriv = derivs[i - 2]
                else:
                    deriv = 0
            else:
                sample_size = smooth
                deriv = (values[i] - values[i - sample_size]) / (time[i] -
                        time[i - sample_size])
            if time[i] < 2.5 and time[i] > 2.3:
                print("time: ")
                print(values[i - 1])
                print(values[i])
                print(deriv)

            derivs.append(deriv)

    return derivs

log = process_log(get_log())
clear()

plt.plot(log[0], log[1], 'b-')
plt.ylabel('cpns')
plt.xlabel('time')

with open(date_string + '-shooter.csv', 'w', newline='') as csvfile:
    csv = csv.writer(csvfile)
    for time, value in zip(log[0], log[2]):
        csv.writerow([time, value])

plt.savefig(date_string + ".png")

plt.show()
