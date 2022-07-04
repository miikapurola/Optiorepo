import math
from numpy import NaN
import pandas as pd
import yfinance as yf
import numpy as np
from matplotlib import pyplot as plt
tckrlist = ['^GSPC']
aikaväli = '15y'
intervalli = '1d'

def dfcreater(tckrlist, period, intervalli):
    dflist = pd.DataFrame()
    for i in tckrlist:
        df = yf.Ticker(i).history(period=period, interval=intervalli)
        dflist = dflist.append(df['Close'])
        dflist = dflist.rename(index= {'Close' : i})
    dflist = dflist.T
    dflist = dflist.sort_index(axis=0)
    return dflist

dflist = dfcreater(tckrlist, aikaväli, intervalli)

def returncalc(df):
    arvot = df['^GSPC'].values.tolist()
    palauta = [NaN]
    for i in range(len(arvot)-1):
        palauta.append(((arvot[i+1]/arvot[i]) - 1))
    df['tuotto'] = palauta

returncalc(dflist)

print(dflist.head())

def MAVar(dflista, interval):
    array = [np.NaN] * (interval -1)
    i = 0
    a = 0
    muuttuja = 0
    while interval <= len(dflista) - i:
        a = i
        muuttuja = []
        while a<i+interval:
            muuttuja.append(dflista[a])
            a = a + 1
        array.append(np.var(muuttuja))
        i = i+1
    print(array)
    return array

dflist['20Var'] = MAVar(dflist['tuotto'], 20)

print(dflist.head())

plt.plot(dflist['20Var'])
plt.show()
