from json import dump

def dumpLOD(data,filename):
    s = open(filename,'w')
    for i in data:
        dump(i,s)
        s.write('\n')
    s.close()
    print(filename+' Creado.')

def loadLOD(filename):
    s = open(filename,'r')
    d = s.readlines()
    s.close()
    data = []
    for i in d :

        da = i.replace ('[','')
        da = da.replace(']','')
        da = da.replace('"','')
        da = da.replace(' ','')
        da = da.split  (',')
        da = [ float(i) for i in da]
        data.append( da)

    print(filename+' Importado')
    return data

candleData = loadLOD(r"J:\Jobs\autotrade\Co_ADAUSDT_1d_2M.txt")

trade = { "none":0, "long":1, "short":2 }


# apertura maximo minimo cierre
for i in candleData:
    
    candle_open = float(i[1])
    candle_max = float(i[2])
    candle_min = float(i[3])
    candle_close = float(i[4])
    
    #RESMAS Strategy
    
    #OverBuy Trigger
    if RSI > overBuyLvl : pass #Order Script
    if RSI < overSellLvl : pass #Order Script
    
    def verTrade( situation, amount, leverage = 0, stoploss = 2 ):
        #situation 1 = overbuy - 0 overSell
        
        if situation :
            if   lastTrade == trade["long"] : pass #Close Long Trade Code
            elif lastTrade == trade["short"] : pass #Do Nothing Wait Stoploss
            else : pass #Open Short Trade Code
            
        else :
            if   lastTrade == trade["long"] : pass #Do Nothing Wait Stoploss
            elif lastTrade == trade["short"] : pass #Close Short Trade Code
            else : pass #Open Long Trade Code
        
        