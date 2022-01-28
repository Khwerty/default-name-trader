from credentials import API_KEY,API_SECRET
from binance import Client
from ta.momentum import RSIIndicator as rsi
import pandas as pd

client = Client(API_KEY,API_SECRET)

def getCandles(coinSymbol,interval,startDate):

    return client.get_historical_klines(coinSymbol, interval, startDate)
  
over = {"BUY": 70, "SELL":30 }
#tg = {"RSI": 0, "SL": 1}

list_order = []
list_trade = []

overbuy = True
oversell = False

lastOrder = "none"
openOrder = False

trade_id = 0
trigger = 0

a_trade_grafic = []


symbol = "ADA"
leverage = 1
amount = 100

candles = pd.DataFrame( getCandles("ADAUSDT","1m","10 hours ago UTC") )

candles_close = candles[4].map(float)

rsi = rsi( candles_close, 14, 1)

candles_close = list(candles_close)

rsi_list = list(rsi._rsi)

def makeOrder( orderType, amount, symbol, leverage, stoploss = 1 ):
  global trade_id, lastOrder, openOrder
  
  lastOrder = orderType
   
  list_order.append([ trade_id, orderType, amount, close_price, trigger])
  
  if openOrder == True:
    tradeType = "SHORT" if lastOrder == "BUY" else "LONG"
    
    price_aperture = list_order[-2][3]
    price_close = list_order[-1][3]
    
    variation =  price_aperture - price_close
    if lastOrder == "SELL" : variation = -variation 
    
    list_trade.append([ tradeType, price_aperture, price_close, variation])
    
    lastOrder = "none"
    trade_id += 1
    
  openOrder = (not openOrder)
  
def verTrade( situation, leverage = 0, stoploss = 1 ):
      
  if situation == overbuy :
    
    if lastOrder == "SELL" : pass #Do Nothing Wait Stoploss
    
    elif lastOrder == "BUY"  : #Close Long
      makeOrder("SELL",amount, symbol, leverage)
      
    else : #Opening Short orderType
      makeOrder("SELL",amount, symbol, leverage)
      
      
  if situation == oversell :
    if   lastOrder == "BUY"  : pass #Do Nothing Wait Stoploss
    
    elif lastOrder == "SELL" : #Close Short 
      makeOrder("BUY",amount, symbol, leverage) 
    
    else : #Opening Long orderType
      makeOrder("BUY",amount, symbol, leverage)
      

# apertura maximo minimo cierre

for ( close_price, rsi_value ) in zip( candles_close, rsi_list ):
  
  if over["BUY"] > rsi_value > over["SELL"] : pass

  else:
    
    #Triggers
    if rsi_value > over["BUY"]  : situation = overbuy
    if rsi_value < over["SELL"] : situation = oversell
    
    trigger = "RSI"

    verTrade( situation )
    
  if openOrder : a_trade_grafic.append(close_price)
  else : a_trade_grafic.append(1.01)

a_rsi_grafic = [ [30,rsi,70] for rsi in rsi_list ]