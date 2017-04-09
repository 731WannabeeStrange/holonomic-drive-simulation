import matplotlib.pyplot as plt
import numpy as np
import subprocess
import math

def clear():
    subprocess.run(['adb', 'logcat', '-c'], stdout=subprocess.PIPE)

def get_log():
    result = subprocess.run(['adb', 'logcat', '-d', '-s', 'auto'], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')

def process_log(log):
    a = []
    b = []
    lines = log.split('\n')
    for line in lines:
        if len(line) != 0:
            if line[0] != '-':
                data = line.split()
                data = data[7:]
                data[-1] = data[-1][:-1]
                for i, datum in enumerate(data):
                    if i == 0:
                        a.append(float(data[i]))
                    elif i == 1:
                        b.append(float(data[i]))

    return [a, b]

def derivative(values, time):
    derivs = []
    for i, (value, sec) in enumerate(zip(values, time)):
        if i != 0:
            deriv = (values[i] - values[i - 1]) / (time[i] - time[i - 1])
            derivs.append(deriv)

    return derivs

distance = 4 # feet
max_acc = 3 # feet/sec^2

diagonal_distance = 2*distance/math.sqrt(2)

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

#log = process_log(get_log())
#plot(log[0], log[1])
# derived_time = np.array(log[0])

# have to use derived time to calculate 

x = np.linspace(0, T, 100)
vposition = np.vectorize(position)
vvelocity = np.vectorize(velocity)
vacceleration = np.vectorize(acceleration)
a = vacceleration(x)
v = vvelocity(x)
p = vposition(x)
derived_position = .95 * p
derived_velocity = derivative(derived_position, x)
derived_acceleration = derivative(derived_velocity, x)
d_p = derived_position
d_v = np.append(derived_velocity, [0])
d_a = np.append(derived_acceleration, [0, 0])

plt.plot(x, v, 'b-')
plt.plot(x, a, 'r-')
plt.plot(x, p, 'g-')
plt.plot(x, d_v, 'o-')
plt.plot(x, d_a, 'p-')
plt.plot(x, d_p, 'v-')
plt.ylabel('feet')
plt.xlabel('time')
plt.show()
