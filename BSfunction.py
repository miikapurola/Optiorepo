
import numpy as np
import math

from matplotlib import pyplot as plt

from scipy.stats import norm

#Test variables
c_1 = 1
s = 9
x_1 = 8
q = 0.3
t = 20/365
r = 0.0218
q_1 = 0.5

suunta = 'Short'
cop = 'Call'

class BSoptions():
    def BSCall(S, X, Q, T, r):

        d_1 = ((np.log(S / X) + (r + Q * Q * 0.5) * T)) / (Q * (T ** 0.5))
        d_2 = d_1 - Q * math.sqrt(T)

        N_1 = norm.cdf(d_1)

        N_2 = norm.cdf(d_2)

        C_0 = (S * N_1) - (X * math.exp(-1 * r * T)) * N_2
        return C_0

    def BSPut(S, X, Q, T, r):

        P_0 = X * math.exp(-1 * r * T) - S + BSoptions.BSCall(S, X, Q, T, r)

        return P_0
class BSGreeks():
    def BSdelta(S, X, Q, T, r, porc):
        d_1 = ((np.log(S / X) + (r + Q * Q * 0.5) * T)) / (Q * (T ** 0.5))
        N_1 = norm.cdf(d_1)
        if porc == 'Call':
            return N_1
        else:
            return - N_1

    def BSvega(S, X, Q, T, r):
        
        d_1 = ((np.log(S / X) + (r + Q * Q * 0.5) * T)) / (Q * (T ** 0.5))

        N_1 = norm.pdf(d_1)
    
        V_0 = S * N_1 * (T ** 0.5)

        V_0 = V_0 / 100

        return V_0

    def BSgamma(S, X, Q, T, r):
        
        d_1 = ((np.log(S / X) + (r + Q * Q * 0.5) * T)) / (Q * (T ** 0.5))

        N_1 = norm.pdf(d_1)
    
        G_0 = N_1 / (S * Q * (T ** 0.5))

        G_0 = G_0 / 100

        return G_0

    def BSTheta(S, X, Q, T, r, porc):

        d_1 = ((np.log(S / X) + (r + Q * Q * 0.5) * T)) / (Q * (T ** 0.5))
        d_2 = d_1 - Q * math.sqrt(T)

        print(d_1)
        N_1 = norm.pdf(d_1)

        if porc == 'Call':
            N_2 = norm.cdf(d_2)
            Theta_0 = -((S * N_1 * Q) / (2 * (T ** 0.5))) - r * X * N_2 * ((math.e) ** (-r*T))
            print(N_1 , r * X * N_2 * ((math.e) ** (-r*T)))
        else:
            N_2 = norm.cdf(-d_2)
            Theta_0 = -((S * N_1 * Q) / (2 * (T ** 0.5))) + r * X * N_2 * ((math.e) ** (-r*T))
        return Theta_0 / 365

    def BSRho(S, X, Q, T, r, porc):

        d_1 = ((np.log(S / X) + (r + Q * Q * 0.5) * T)) / (Q * (T ** 0.5))
        d_2 = d_1 - Q * math.sqrt(T)

        if porc == 'Call':
            N_2 = norm.cdf(d_2)
            Rho_0 = X * T * N_2 * ((math.e) ** (-r*T))
        else: 
            N_2 = norm.cdf(-d_2)
            Rho_0 = -X * T * N_2 * ((math.e) ** (-r*T))

        return Rho_0
class Diagram():
    def graphbasics(strike):
        distance = strike * 2
        x_axis = np.linspace(int(strike * 0.5), distance, int(strike * 1.5)*100)
        zero = np.array([0] * int(strike * 1.5)*100)
        return x_axis, zero


    def Graphcalc(x_akseli, C, X, type, direction):
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


    def plotter(x, y1, y2, s, fill):
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
        plt.axvline(x=s, ymin=0.05, ymax=0.95, color='black', linestyle='dashed')

#x, y_0 = Diagram.graphbasics(x_1)
# y_1 = Diagram.Graphcalc(x, BSoptions.BSPut(s, x_1, q, t, r), 'Put', 'Short')
# y_2 = Diagram.Graphcalc(x, BSoptions.BSCall(s, x_#1, q, t, r), 'Call', 'Long')
#y_21 = Diagram.Graphcalc(x, c_1, cop, suunta)
# y_3 = BSoptions.BSCall(x, x_1, q, t, r)

# y_gamma  = BSGreeks.BSgamma(x, x_1, q, t, r)
# y_gamma1  = BSGreeks.BSgamma(-x, -4000, q, t, r)
#Diagram.plotter(x, y_0, y_21, 1)

# Diagram.plotter(x, y_0, y_gamma1, 0)


def summafunctio(array):
    summa = np.sum(array, axis=0)
    return summa
#y_gammagregaatti = summafunctio(y_gamma, y_gamma1)

#Diagram.plotter(x, y_0, y_gammagregaatti, 0)
def shorteq(list, eq):
    shrt = []
    for i in range(len(list)):
        shrt.append(eq - list[i])
    return shrt

def realtime(lista, ops):
    rt = []
    for i in range(len(lista)):
        rt.append(lista[i] - ops)
    return rt

# shorty = shorteq(x, s)

# y_4 = realtime(y_3, BSoptions.BSCall(s, x_1, q, t, r))

def deltaratio(vol, equity, optio):
    hedger = summafunctio(equity, optio)
    i = 1 / vol - 1
    while i > 0:
        hedger = summafunctio(hedger, optio)
        i=i-1
    return hedger

# ysum = deltaratio(q, shorty, y_4)

# symma = summafunctio(x, y_2)

# y_5 = BSoptions.BSPut(x, x_1, q, t, r)

#Graph labels

# plt.ylabel("Sijoituksen arvo")
# plt.title(
#     f"Sijoituksen P&L diagrammi erääntymispäivänä. T = {t} K = {x_1} C = {c_1}"
# )

#plt.show()