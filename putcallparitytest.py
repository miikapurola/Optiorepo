import math
import pandas as pd
import yfinance as yf
import yahoo_fin.options as ops
import numpy as np
from matplotlib import pyplot as plt

import math
import datetime
from datetime import timedelta
import yfinance as yf
import yahoo_fin.options as ops
import pandas as pd

#T komponentin parametrit

date = datetime.datetime.now()
eastern = date + timedelta(hours=-7)
midnightdiff = datetime.datetime(eastern.year, eastern.month,eastern.day, 23, 59, 59) - eastern

def get_expirationdays():
    expirationmins_all = []
    expirationmins = []
    expirationd = ops.get_expiration_dates('^SPX')
    alfa = int(round(eastern.timestamp()))
    for i in expirationd:
        format = '%B %d, %Y'
        date_object = datetime.datetime.strptime(i, format)
        timestamp = int(round(date_object.timestamp()))
        mins = (timestamp - alfa)/(60)
        expirationmins_all.append(mins)
    counter = 0
    for i in expirationmins_all:
        if 23*24*60 < i < 37*24*60:
            expirationmins.append([i, expirationd[counter]])
        counter += 1
    return expirationmins[0], expirationmins[-1]

M_01, M_02 = get_expirationdays()

print(M_01, M_02)

M_C = midnightdiff.seconds / 60 #minutes remaining until midnight of the current day
M_S1 = 510 #minutes from midnight until 9:30 a.m. ET for “standard” SPX expirations; or minutes from midnight until 4:00 p.m. ET for “weekly” SPX expirations
M_S2 = 900
N_1 = M_C + M_S1 + M_01[0]
N_2 = M_C + M_S2 + M_02[0]
N_30 = 43200
N_365 = 525600
T_1 = N_1 / N_365 #Time to expration 1
T_2 = N_2 / N_365 #Time to expration 2

spot_price = yf.Ticker('^SPX').info['regularMarketPrice']
calls_near = ops.get_calls('^SPX', date=M_01[1])
#calls_next = ops.get_calls('^SPX', date=M_02[1])
puts_near = ops.get_puts('^SPX', date=M_01[1])
#puts_next = ops.get_puts('^SPX', date=M_02[1])
calls_near['Midpoint'] = (calls_near['Bid'] + calls_near['Ask']) / 2
puts_near['Midpoint'] = (puts_near['Bid'] + puts_near['Ask']) / 2
#calls_next['Midpoint'] = (calls_next['Bid'] + calls_next['Ask']) / 2
#puts_next['Midpoint'] = (puts_next['Bid'] + puts_next['Ask']) / 2
def delete_itm(optionlist):
    droplist = []
    for option in range(len(optionlist)):
            if optionlist.at[option, 'Bid'] == 0.0:
                droplist.append(option)
    droplist = list(dict.fromkeys(droplist))
    optionlist = optionlist.drop(index=droplist)
    return optionlist

calls_near = delete_itm(calls_near)
puts_near = delete_itm(puts_near)

print(calls_near)


put_price = 4200
call_price = 37
r_annum = 0.0218
time_to_maturity = T_1
stock_t0 = 29983
strike = 34000

S_P_C = stock_t0 + put_price - call_price
Ke = strike * ((math.e) ** (-r_annum * time_to_maturity))
print(S_P_C)
print(Ke)
def borrowed(SPC, r, t):
    return SPC * ((math.e) ** (r * t))

def diff(repaid, striker, SPC, KE):
    if SPC <= KE:
        return striker - repaid
    else:
        return repaid - striker


def differencecal(calls, puts):
    spot_price = yf.Ticker('^SPX').info['regularMarketPrice']
    cstrikelist = calls['Strike'].values.tolist()
    cmidpoint = calls['Midpoint'].values.tolist()
    pstrikelist = puts['Strike'].values.tolist()
    pmidpoint = puts['Midpoint'].values.tolist()
    strikelist1 = []
    strikelist2 = []
    strikelist = []
    diffilist = []
    for i in range(len(cstrikelist)):
        strikelist1.append([cstrikelist[i],cmidpoint[i]])
    for i in range(len(pstrikelist)):
        strikelist2.append([pstrikelist[i],pmidpoint[i]])
    for i in range(len(strikelist1)):
        for j in range(len(strikelist2)):
            if strikelist1[i][0] == strikelist2[j][0]:
                S_P_C = spot_price + strikelist2[j][1]-strikelist1[i][1]
                rpid = borrowed(S_P_C,r_annum,time_to_maturity)
                diffi = diff(rpid, strikelist1[i][0],S_P_C, (strikelist1[i][0]*((math.e) ** (r_annum * time_to_maturity))))
                diffilist.append(diffi/S_P_C)
                strikelist.append(strikelist1[i][0])
    return strikelist, diffilist

strikes, diffibiffi = differencecal(calls_near, puts_near)

print(strikes)
print(diffibiffi)

plt.plot(strikes, diffibiffi)
plt.show()
