import BSfunction as BS
import pandas as pd 
import numpy as np
import math 
from scipy.stats import norm
from matplotlib import pyplot as plt

k = 111.5
r_a = 0.0218
t = 30.5/365
q = 0.28
s = 100

x = np.linspace(0,100,101)
vega_x = np.linspace(0,1,366)

print(BS.BSoptions.BSCall(5, 5, 0.23,1,0.0218))
print(BS.BSGreeks.BSdelta(s,k,q,t,r_a,'Put'))
print(BS.BSGreeks.BSdelta(s,k,q,t,r_a,'Call'))
print(BS.BSoptions.BSPut(s,k,q,t,r_a))
print(BS.BSoptions.BSPut(s,100,q,t,r_a))
print(- BS.BSoptions.BSPut(s,100,q,t,r_a) + BS.BSoptions.BSPut(s,k,q,t,r_a))

vega = []
gamma = []
lista_1 = []
delta = []
n = 5
def withdifferent_vol(n):
    while n > 0:
        delta = []
        q_1 = n/5
        for i in x:
            delta.append(BS.BSGreeks.BSdelta(s, k, q_1, t, r_a, 'Call'))
        lista_1.append(delta)
        n -= 1
    return lista_1
lista_1 = withdifferent_vol(n)
# for i in vega_x:
#     vega.append(BS.BSGreeks.BSvega(s, k, q, i, r_a))

# for i in x:
#     delta.append(BS.BSGreeks.BSdelta(i, k, q, t, r_a, 'Call'))

# for i in delta:
#     gamma

# for i in lista_1:
#     plt.plot(x, i)

# plt.show()

# plt.plot(vega_x, vega)
# plt.show()


  