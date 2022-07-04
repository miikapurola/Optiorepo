import numpy as np
import math
from scipy.stats import norm
import matplotlib.pyplot as plt

class Diagram():
    def graphbasics(strike):
        distance = strike * 2
        x_axis = np.linspace(0, distance, int(strike * 1.5)*100)
        zero = np.array([0] * distance*100)
        return x_axis, zero



    def Graphcalc(x_akseli, C, X, type, direction, ):
        n = []
        if type == 'Call':
            for i in range(len(x_akseli)):
                if x_akseli[i] <= X:
                    n.append(-C)
                else:
                    n.append(x_akseli[i] - X - C)
        elif type == 'Put':
            for i in range(len(x_akseli)):
                if x_akseli[i] >= X:
                    n.append(-C)
                else:
                    n.append(X - x_akseli[i] - C)

        if direction == 'Short':
            for i in range(len(n)):
                n[i] = n[i] * -1
        else:
            n = n
        return np.array(n)

    def plotter(x, y1, y2, fill):
        if fill == 1:
            plt.plot(x,y1, color='black')
            plt.plot(x,y2, color='black')
            plt.fill_between(x, y1, y2, where=(y1 > y2), color='red',
                        interpolate=True)
            plt.fill_between(x, y1, y2, where=(y1 <= y2), color='green',
                        interpolate=True)
        else:
            plt.plot(x,y1, color='black')
            plt.plot(x,y2, color='black')

S  = 5
X =  5*1.21
r = 0.0228
Q = 0.23
T = 1

x_axis, y_0 = Diagram.graphbasics(7)

array = []
for i in x_axis:
    d_1 = ((np.log(i / X) + (r + Q * Q * 0.5) * T)) / (Q * (T ** 0.5))
    d_2 = d_1 - Q * math.sqrt(T)

    N_1 = norm.cdf(d_1)

    N_2 = norm.cdf(d_2)

    array.append(N_2)
d_1 = ((np.log(S / X) + (r + Q * Q * 0.5) * T)) / (Q * (T ** 0.5))
d_2 = d_1 - Q * math.sqrt(T)
N_2 = norm.cdf(d_2)
print(N_2)
plt.plot(x_axis, array)
plt.show()
