import matplotlib.pyplot as plt
import numpy as np
import subprocess
import math
import datetime
date_string = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M")

def clear():
    subprocess.run(['adb', 'logcat', '-c'], stdout=subprocess.PIPE)

def get_log():
    result = subprocess.run(['adb', 'logcat', '-d', '-s', 'auto'], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')

def process_log(log):
    a = []
    b = []
    lines = log.split('\n')
    for q, line in enumerate(lines):
        if len(line) != 0:
            if line[0] != '-':
                data = line.split()
                data = data[7:]
                data[-1] = data[-1][:-1]
                for i, datum in enumerate(data):
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

    return [a, b]

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

distance = 1 # feet
max_acc = 5 # feet/sec^2

diagonal_distance = math.sqrt(2)*distance/2

T = math.sqrt((2*math.pi*diagonal_distance)/max_acc) # time to destination
k_one = 2*math.pi/T # max_acc * k_one is max jerk
k_two = max_acc/k_one # 2 * k_two is max speed
k_three = 1/k_one

def acceleration(t):
    return max_acc*math.sin(k_one*t)

def velocity(t):
    return k_two*(1 - math.cos(k_one*t))

def position(t):
    return k_two*(t - k_three*math.sin(k_one*t))

log = process_log(get_log())
clear()

# have to use derived time to calculate 
x = np.array(log[0])

# Used for testing
# x = np.linspace(0, T, 100)

vposition = np.vectorize(position)
vvelocity = np.vectorize(velocity)
vacceleration = np.vectorize(acceleration)
a = vacceleration(x)
v = vvelocity(x)
p = vposition(x)
derived_position = np.array(log[1])
derived_velocity = derivative(derived_position, x, 10)
derived_acceleration = derivative(derived_velocity, x, 10)
d_p = derived_position
d_v = np.append(derived_velocity, [0])
d_a = np.append(derived_acceleration, [0, 0])

plt.plot(x, v, 'b-')
#plt.plot(x, a, 'r-')
plt.plot(x, p, 'g-')
plt.plot(x, d_v, 'b-')
#plt.plot(x, d_a, 'r-')
plt.plot(x, d_p, 'g-')
plt.ylabel('feet')
plt.xlabel('time')

with open(date_string + '-motionpro.csv', 'w', newline='') as csvfile:
    csv_file = csv.writer(csvfile)
    for time, value in zip(log[0], log[1]):
        csv_file.writerow([time, value])

plt.savefig(date_string + ".png")

plt.show()
