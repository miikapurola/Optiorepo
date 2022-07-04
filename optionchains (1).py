import yfinance as yf
import yahoo_fin.options as ops
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from datetime import datetime

ticker1 = 'TSLA'

expirationd = ops.get_expiration_dates(ticker1)
print(expirationd)
calls = ops.get_calls(ticker1, date=expirationd[1])
puts = ops.get_puts(ticker1)

def opschainfunc(tikkeri):
    välipd = pd.DataFrame()
    for i in expirationd:
        opt = ops.get_calls(ticker=tikkeri, date=i)
        välidex = []
        for j in range(len(opt)):
            välidex.append(i)
        opt['Exp'] = välidex
        välipd = välipd.append(opt)
    return välipd

df = opschainfunc(ticker1)

x = df['Strike'].tolist()
y = df['Exp'].tolist()
z = df['Implied Volatility'].tolist()

curr_dt = datetime.now()
 
alfa = int(round(curr_dt.timestamp()))

paska = []
for i in y:
    format = '%B %d, %Y'
    date_object = datetime.strptime(i, format)
    timestamp = int(round(date_object.timestamp()))
    days = (timestamp - alfa)/(60*60*24)
    paska.append(days)

y = paska

kakka = []

for i in z:
    i = i.replace(',', '')
    prosent = float(i.strip('%'))/100
    kakka.append(prosent) 

z = kakka

fig = plt.figure()
ax = Axes3D(fig)
surf = ax.plot_trisurf(x, y, z, cmap='viridis')
fig.colorbar(surf, shrink=0.5, aspect=5)

ax.set_xlabel('Strike', fontweight ='bold')
ax.set_ylabel('Exp days', fontweight ='bold')
ax.set_zlabel('Implied Volatility', fontweight ='bold')

plt.show()