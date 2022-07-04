import math
import datetime
from datetime import timedelta
import yfinance as yf
import yahoo_fin.options as ops
import pandas as pd

import BSfunction as BS



date = datetime.datetime.now()
eastern = date + timedelta(hours=-7)
midnightdiff = datetime.datetime(eastern.year, eastern.month,eastern.day, 23, 59, 59) - eastern

ticker1 = 'TSLA'
r = 0.0228
spot_price = yf.Ticker(ticker1).info['regularMarketPrice']

expirationd = ops.get_expiration_dates(ticker1)
expirationmins_all = []

def get_exp_time():
    alfa = int(round(eastern.timestamp()))
    for i in expirationd:
        format = '%B %d, %Y'
        date_object = datetime.datetime.strptime(i, format)
        timestamp = int(round(date_object.timestamp()))
        mins = (timestamp - alfa)/(60)
        expirationmins_all.append(mins)
get_exp_time()

M_C = midnightdiff.seconds / 60
N_365 = 525600

def GEX(expdayindex):

    t = expirationmins_all[expdayindex] + 900 + M_C
    T = t / N_365

    calls = ops.get_calls(ticker1, date=expirationd[expdayindex])
    puts = ops.get_puts(ticker1, date=expirationd[expdayindex])

    def OIdeleter(optionlist):
        droplist = []
        for option in range(len(optionlist)):
                if optionlist.at[option, 'Open Interest'] == '-':
                    droplist.append(option)
        droplist = list(dict.fromkeys(droplist))
        optionlist = optionlist.drop(index=droplist)
        return optionlist

    calls = OIdeleter(calls)
    puts = OIdeleter(puts)

    calls['Open Interest'] = calls['Open Interest'].astype(int)
    puts['Open Interest'] = puts['Open Interest'].astype(int)

    def IV_to_percent(dflist):
        Percentlist = []
        z = dflist['Implied Volatility'].tolist()
        for i in z:
            i = i.replace(',', '')
            prosent = float(i.strip('%'))/100
            Percentlist.append(prosent)
        dflist['Implied Volatility'] = Percentlist

    IV_to_percent(calls)
    IV_to_percent(puts)

    calls['Gamma'] = BS.BSGreeks.BSgamma(spot_price, calls['Strike'], calls['Implied Volatility'], T, r)
    calls['GEX'] = calls['Gamma'] * calls['Open Interest'] * 100 * 0.01 * spot_price ** 2
    puts['Gamma'] = BS.BSGreeks.BSgamma(spot_price, puts['Strike'], puts['Implied Volatility'], T, r)
    puts['GEX'] = puts['Gamma'] * puts['Open Interest'] * 100 * 0.01 * spot_price ** 2

    callgex = calls['GEX'].sum() / (1*(10**9))
    putgex = puts['GEX'].sum() / (1*(10**9))

    gex = callgex + putgex * (-1)   
    print(expirationd[expdayindex],t, gex)
    return gex

gexsumma = 0

for maturtiteettipäivä in range(len(expirationd)-2):
    gexsumma += GEX(maturtiteettipäivä)

print(gexsumma)
