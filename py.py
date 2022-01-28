from credentials import API_KEY,API_SECRET
from binance import Client
from ta.momentum import RSIIndicator as rsi
import pandas as pd

client = Client(API_KEY,API_SECRET)

def getCandles(coinSymbol,interval,startDate):

    return client.get_historical_klines(coinSymbol, interval, startDate)
  
over = {"BUY": 70, "SELL":30 }

list_order = []
list_trade = []

a_trade_grafic = []
a_rsi_grafic = []

overbuy = True
oversell = False

last_order = "none"
open_order = False

trade_id, trigger = 0,0


symbol = "ADA"
leverage = 1
amount = 100


candles = pd.DataFrame( getCandles("ADAUSDT","1m","10 hours ago UTC") )

candles_close = candles[4].map(float)

rsi = rsi( candles_close, 14, 1)

candles_close = list(candles_close)

rsi_list = list(rsi._rsi)

def makeOrder( orderType, amount, symbol, leverage, stoploss = 1 ):
  global trade_id, last_order, open_order
  
  last_order = orderType
   
  list_order.append([ trade_id, orderType, amount, close_price, trigger])
  
  if open_order == True:
    trade_type = "SHORT" if last_order == "BUY" else "LONG"
    
    price_aperture = list_order[-2][3]
    price_close = list_order[-1][3]
    
    variation =  price_aperture - price_close
    if last_order == "SELL" : variation = -variation 
    
    list_trade.append([ trade_type, price_aperture, price_close, variation])
    
    last_order = "none"
    trade_id += 1
    
  open_order = (not open_order)
  
def verTrade( situation, leverage = 0, stoploss = 1 ):
  
      
  if situation == overbuy :
    
    if not open_order : makeOrder("SELL",amount, symbol, leverage)
    
    if last_order == "SELL" : pass #Do Nothing Wait Stoploss
    
    if last_order == "BUY"  : #Close Long
      makeOrder("SELL",amount, symbol, leverage)


  if situation == oversell :
    
    if not open_order : makeOrder("BUY",amount, symbol, leverage)
    
    if last_order == "BUY" : pass #Do Nothing Wait Stoploss
    
    if last_order == "SELL"  : #Close Long
      makeOrder("BUY",amount, symbol, leverage)
      

for ( close_price, rsi_value ) in zip( candles_close, rsi_list ):
  
  if over["BUY"] > rsi_value > over["SELL"] : pass

  else:
    
    #Triggers
    if rsi_value > over["BUY"]  : situation = overbuy
    if rsi_value < over["SELL"] : situation = oversell
    
    trigger = "RSI"

    verTrade( situation )
    
  a_trade_grafic.append( close_price if open_order else 1.01)

a_rsi_grafic = [ [30,rsi,70] for rsi in rsi_list ]