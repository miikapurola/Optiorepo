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

spot_price = yf.Ticker('^SPX').info['regularMarketPrice']
calls_near = ops.get_calls('^SPX', date=M_01[1])
calls_next = ops.get_calls('^SPX', date=M_02[1])
puts_near = ops.get_puts('^SPX', date=M_01[1])
puts_next = ops.get_puts('^SPX', date=M_02[1])
calls_near['Midpoint'] = (calls_near['Bid'] + calls_near['Ask']) / 2
puts_near['Midpoint'] = (puts_near['Bid'] + puts_near['Ask']) / 2
calls_next['Midpoint'] = (calls_next['Bid'] + calls_next['Ask']) / 2
puts_next['Midpoint'] = (puts_next['Bid'] + puts_next['Ask']) / 2

def delete_itm(optionlist, corp):
    droplist = []
    tuplanolla1 = 0
    tuplanolla = []
    puttupla = []
    first = 0
    indeksi = 0
    if corp == 'C':
        for option in range(len(optionlist)):
            if optionlist.at[option,'Strike'] < spot_price:
                droplist.append(option)
            elif first != 1 and option < len(optionlist)-1:
                if optionlist.at[option, 'Bid'] == 0.0 and optionlist.at[option + 1, 'Bid'] == 0.0:
                    tuplanolla1 = option + 1
                    first = 1
            if optionlist.at[option, 'Bid'] == 0.0:
                droplist.append(option)
        if tuplanolla1 != 0:
            for i in range(tuplanolla1,len(optionlist)):
                droplist.append(i)
    else:
        for option in range(len(optionlist)-1):
            if optionlist.at[option,'Strike'] > spot_price:
                droplist.append(option)
            if optionlist.at[option,'Strike'] > spot_price and first != 1:
                first = 1
                indeksi = option
            if optionlist.at[len(optionlist) - option-1, 'Bid'] == 0.0 and optionlist.at[len(optionlist) - option - 2, 'Bid'] == 0.0:
                tuplanolla.append(len(optionlist) - option-1)
            if optionlist.at[option, 'Bid'] == 0.0:
                droplist.append(option)
        for i in tuplanolla:
            if i < indeksi:
                puttupla.append(i)
        if len(puttupla) > 0:
            for i in range(0,puttupla[0]):
                droplist.append(i)
        droplist.append(len(optionlist)-1)
    droplist = list(dict.fromkeys(droplist))
    optionlist = optionlist.drop(index=droplist)
    return optionlist

def delete_itm1(optionlist):
    droplist = []
    for option in range(len(optionlist)):
            if optionlist.at[option, 'Bid'] == 0.0:
                droplist.append(option)
    droplist = list(dict.fromkeys(droplist))
    optionlist = optionlist.drop(index=droplist)
    return optionlist

def differencecal(calls, puts):
    cstrikelist = calls['Strike'].values.tolist()
    cmidpoint = calls['Midpoint'].values.tolist()
    pstrikelist = puts['Strike'].values.tolist()
    pmidpoint = puts['Midpoint'].values.tolist()
    strikelist1 = []
    strikelist2 = []
    strikelist = []
    pienin = [121212, 1000000000,'realvalue']
    for i in range(len(cstrikelist)):
        strikelist1.append([cstrikelist[i],cmidpoint[i]])
    for i in range(len(pstrikelist)):
        strikelist2.append([pstrikelist[i],pmidpoint[i]])
    for i in range(len(strikelist1)):
        for j in range(len(strikelist2)):
            if strikelist1[i][0] == strikelist2[j][0]:
                strikelist.append([strikelist1[i][0],abs(strikelist2[j][1]-strikelist1[i][1])])
                if abs(strikelist2[j][1]-strikelist1[i][1]) <= pienin[1]:
                    pienin = [strikelist1[i][0],abs(strikelist1[i][1]-strikelist2[j][1]),strikelist1[i][1]-strikelist2[j][1]]
    return pienin
print(delete_itm1(calls_near))
print(delete_itm1(puts_near))
smalldiff_1 = differencecal(delete_itm1(calls_near), delete_itm1(puts_near))
smalldiff_2 = differencecal(delete_itm1(calls_next), delete_itm1(puts_next))

K_0 = 3820 #First strike below the forward index level, F
R = 0.005 #Risk-free interest rate to expiration
M_C = midnightdiff.seconds / 60 #minutes remaining until midnight of the current day
M_S1 = 510 #minutes from midnight until 9:30 a.m. ET for “standard” SPX expirations; or minutes from midnight until 4:00 p.m. ET for “weekly” SPX expirations
M_S2 = 900
N_1 = M_C + M_S1 + M_01[0]
N_2 = M_C + M_S2 + M_02[0]
N_30 = 43200
N_365 = 525600
T_1 = N_1 / N_365 #Time to expration 1
T_2 = N_2 / N_365 #Time to expration 2
print(smalldiff_2[0], smalldiff_2[2],(math.e) ** (0.0005 * T_1))
F_1 = smalldiff_1[0] + smalldiff_1[2]*(math.e) ** (0.0005 * T_1)
F_2 = smalldiff_2[0] + smalldiff_2[2]*(math.e) ** (0.0005 * T_2)
print(smalldiff_1[0], smalldiff_1[2],(math.e) ** (0.0005 * T_1))
print(F_1,F_2)

calls_near = delete_itm(calls_near, 'C')
puts_near = delete_itm(puts_near, 'P')
calls_next = delete_itm(calls_next, 'C')
puts_next = delete_itm(puts_next, 'P')

def striketable(calls, puts, r_12, t, K, F):
    cmid = calls['Midpoint'].values.tolist()
    pmid = puts['Midpoint'].values.tolist()
    mids = pmid + cmid
    cstrikelist = calls['Strike'].values.tolist()
    pstrikelist = puts['Strike'].values.tolist()
    strikelist = pstrikelist + cstrikelist
    strike_difference = [mids[0]*(strikelist[1]-strikelist[0])/(strikelist[0] ** 2)*((math.e)**(r_12*t))]
    for i in range(1,len(strikelist)-1):
        strike_difference.append(mids[i]*((strikelist[i+1]-strikelist[i-1])/2)/(strikelist[i] ** 2)*((math.e)**(r_12*t)))
    strike_difference.append(mids[-1]*(strikelist[-1]-strikelist[-2])/(strikelist[-1] ** 2)*((math.e)**(r_12*t)))
    res = (2/t)*sum(strike_difference)-(1/t)*(((F/K)-1)**2)
    print((1/t)*(((F/K)-1)**2), F/K-1, 1/t)
    return res

sigmasqrd1 = striketable(calls_near, puts_near, R, T_1, K_0, F_1)
sigmasqrd2 = striketable(calls_next, puts_next, R, T_2, K_0, F_2)
print(sigmasqrd1, T_1, T_2, sigmasqrd2)
VIX = math.sqrt(((T_1*sigmasqrd1*((N_2-N_30)/(N_2-N_1)))+(T_2*sigmasqrd2*((N_30-N_1)/(N_2-N_1))))*(N_365/N_30))*100

print(VIX)