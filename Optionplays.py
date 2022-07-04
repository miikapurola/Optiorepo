import numpy as np
import math
import BSfunction as BS
import matplotlib.pyplot as plt


strike = 5

x_axis, y0 = BS.Diagram.graphbasics(strike)

def Longcall(call_option_price, strike, quantity):
    #Buy a call at strike A
    y2 = BS.Diagram.Graphcalc(x_axis, call_option_price, strike, 'Call', 'Long') * quantity
    BS.Diagram.plotter(x_axis, y0, y2, strike, 1)
#Longcall(0.5, strike, 1)
def Shortcall(call_option_price, strike, quantity):
    #Buy a call at strike A
    y2 = BS.Diagram.Graphcalc(x_axis, call_option_price, strike, 'Call', 'Short') * quantity
    BS.Diagram.plotter(x_axis, y0, y2, strike, 1)
#Shortcall(0.5, strike, 1)
def Covered_call(call_option_price, strike, quantity, stock_price):
    y1 = BS.Diagram.Graphcalc(x_axis, call_option_price, strike, 'Call', 'Short') * quantity
    y11 = (x_axis - stock_price) * quantity 
    y2 = BS.summafunctio([y11,y1])
    BS.Diagram.plotter(x_axis, y0, y2, stock_price, 1)
#Covered_call(1, strike, 10, 8)
def Longput(call_option_price, strike, quantity):
    #Buy a call at strike A
    y2 = BS.Diagram.Graphcalc(x_axis, call_option_price, strike, 'Put', 'Long') * quantity
    BS.Diagram.plotter(x_axis, y0, y2, strike , 1)
#Longput(1, strike, 1)
def Shortput(call_option_price, strike, quantity):
    y2 = BS.Diagram.Graphcalc(x_axis, call_option_price, strike, 'Put', 'Short') * quantity
    BS.Diagram.plotter(x_axis, y0, y2, strike , 1)
Shortput(1, strike, 1)
def Protetctive_put(call_option_price, strike, quantity, stock_price):
    y1 = BS.Diagram.Graphcalc(x_axis, call_option_price, strike, 'Put', 'Long') * quantity
    y11 = (x_axis - stock_price) * quantity 
    y2 = BS.summafunctio([y11,y1])
    BS.Diagram.plotter(x_axis, y0, y2, stock_price, 1)
#Protetctive_put(1, strike, 10, 12)
def Bull_put_spread(option_price_1, option_price_2, strike_1, strike_2, quantity_1, quantity_2, stock_price):
    # Buy a put at strike A
    # Sell a put at strike B
    y1 = BS.Diagram.Graphcalc(x_axis, option_price_1, strike_1, 'Put', 'Long') * quantity_1
    y11 = BS.Diagram.Graphcalc(x_axis, option_price_2, strike_2, 'Put', 'Short') * quantity_2
    y2 = BS.summafunctio([y11,y1])
    BS.Diagram.plotter(x_axis, y0, y2, stock_price, 1)
#Bull_put_spread(1, 2, 6, 10, 1, 3, 8)
def Bear_call_spread(option_price_1, option_price_2, strike_1, strike_2, quantity_1, quantity_2, stock_price):
    # Sell a call at strike A
    # Buy a call at strike B
    if strike_2 != stock_price:
        print('System error: Ei oikea ythälö! Kokeile jotain toista nyyppä')
        return
    y1 = BS.Diagram.Graphcalc(x_axis, option_price_1, strike_1, 'Call', 'Short') * quantity_1
    y11 = BS.Diagram.Graphcalc(x_axis, option_price_2, stock_price, 'Call', 'Long') * quantity_2
    y2 = BS.summafunctio([y11,y1])
    BS.Diagram.plotter(x_axis, y0, y2, stock_price, 1)            
#Bear_call_spread(2, 1, 6, 8, 1, 1, 8)
def Bull_call_spread(option_price_1, option_price_2, strike_1, strike_2, quantity_1, quantity_2, stock_price):
    # Buy a call at strike A
    # Sell a call at strike B
    if strike_1 != stock_price:
        print('System error: Ei oikea ythälö! Kokeile jotain toista nyyppä')
        return
    y1 = BS.Diagram.Graphcalc(x_axis, option_price_1, strike_1, 'Call', 'Long') * quantity_1
    y11 = BS.Diagram.Graphcalc(x_axis, option_price_2, strike_2, 'Call', 'Short') * quantity_2
    y2 = BS.summafunctio([y11,y1])
    BS.Diagram.plotter(x_axis, y0, y2, stock_price, 1)            
#Bull_put_spread(2, 3, 8, 10, 1, 1, 8)
def Bear_put_spread(option_price_1, option_price_2, strike_1, strike_2, quantity_1, quantity_2, stock_price):
    # Sell a put at strike A
    # Buy a put at strike B
    if strike_1 != stock_price:
        print('System error: Ei oikea ythälö! Kokeile jotain toista nyyppä')
        return
    y1 = BS.Diagram.Graphcalc(x_axis, option_price_1, strike_1, 'Put', 'Short') * quantity_1
    y11 = BS.Diagram.Graphcalc(x_axis, option_price_2, strike_2, 'Put', 'Long') * quantity_2
    y2 = BS.summafunctio([y11,y1])
    BS.Diagram.plotter(x_axis, y0, y2, stock_price, 1)            
#Bear_put_spread(2, 3, 8, 10, 1, 1, 8)
def Bear_put_spread(option_price_1, option_price_2, strike_1, strike_2, quantity_1, quantity_2, stock_price):
    # Sell a put at strike A
    # Buy a put at strike B
    if strike_1 != stock_price:
        print('System error: Ei oikea ythälö! Kokeile jotain toista nyyppä')
        return
    y1 = BS.Diagram.Graphcalc(x_axis, option_price_1, strike_1, 'Put', 'Short') * quantity_1
    y11 = BS.Diagram.Graphcalc(x_axis, option_price_2, strike_2, 'Put', 'Long') * quantity_2
    y2 = BS.summafunctio([y11,y1])
    BS.Diagram.plotter(x_axis, y0, y2, stock_price, 1)            
#Bear_put_spread(2, 3, 8, 10, 1, 1, 8)
def Custom_strat():
    return
plt.show()
