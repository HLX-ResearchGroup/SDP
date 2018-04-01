import pandas as pd

def rstd(data,datac,i):
    return data['C'].rolling(window = i,center = False).std()

def rsma(data,datac,i):
    return data['C'].rolling(window = i,center = False).mean()

def rema(data,datac,i):
    return data['C'].ewm(alpha = 1.0/float(i),min_periods = i).mean()

def rhmax(data,datac,i):
    return data['H'].rolling(window = i,center = False).max()

def rmmin(data,datac,i):
    return data['L'].rolling(window = i,center = False).min()


def op_mean(data,datac,i):
    return datac['O'].rolling(window = i,center = False).mean()

def cl_mean(data,datac,i):
    return datac['C'].rolling(window = i,center = False).mean()

def hi_max(data,datac,i):
    return datac['H'].rolling(window = i,center = False).max()

def lo_min(data,datac,i):
    return datac['L'].rolling(window = i,center = False).min()

def vl_mean(data,datac,i):
    return datac['V'].rolling(window = i,center = False).mean()

def kd(data,datac,i):
    rsv = (data['C'] - rmmin(data,datac,i+9))/(rhmax(data,datac,i+9) - rmmin(data,datac,i+9))
    k = rsv.ewm(alpha = 3/float(i+3),min_periods = (i+3)//3).mean()
    d = k.ewm(alpha = 3/float(i+3),min_periods = (i+3)//3).mean()
    return k,d

def k(data,datac,i):
    return kd(data,datac,i)[0]
def d(data,datac,i):
    return kd(data,datac,i)[1]

def dma(data,datac,i):
    return (rsma(data,datac,i)-data['C'])/data['C']

def wr(data,datac,i):
    return (rhmax(data,datac,i)-data['C'])/(rhmax(data,datac,i)-rmmin(data,datac,i))

def rsi(data,datac,i):
    U = (data['C']>data['C'].shift(1))*(data['C']-data['C'].shift(1))
    D = (data['C']<data['C'].shift(1))*(data['C']-data['C'].shift(1))*(-1)
    ###
    smau = U.ewm(alpha = 1.0/float(i),min_periods = i).mean()
    smad = D.ewm(alpha = 1.0/float(i),min_periods = i).mean()
    return 1-1/(1+smau/smad)

def vortex(data,datac,i):
    TR = pd.DataFrame({'hl':abs(data['H']-data['L']),'lc':abs(data['L']-data['C'].shift(1)),'hc':abs(data['H']-data['C'].shift(1))}).max(axis = 1)
    VMP = abs(data['H'] - data['L'].shift(1))
    VMN = abs(data['L'] - data['H'].shift(1))
    ###
    STR = TR.rolling(window = i,center = False).sum()
    SVMP = VMP.rolling(window = i,center = False).sum()
    SVMN = VMN.rolling(window = i,center = False).sum()
    ### VIP/VIN
    return SVMP/STR,SVMN/STR

def vip(data,datac,i):
    return vortex(data,datac,i)[0]
def vin(data,datac,i):
    return vortex(data,datac,i)[1]

def boll(data,datac,i):
    ubb = rsma(data,datac,i+1) + 1.5*rstd(data,datac,i+1)
    lbb = rsma(data,datac,i+1) - 1.5*rstd(data,datac,i+1)
    return (data['C']-lbb)/(ubb-lbb)

def variance(data,datac,i):
    return datac['C'].rolling(window = i+1,center = False).std().apply(lambda x:min(5,max(0,x)))

def macd(data,datac,FI=12,SI=26,XI=9):
    DIF = data.C.ewm(alpha = 1.0/float(FI),min_periods = FI).mean()-data.C.ewm(alpha = 1.0/float(SI),min_periods = SI).mean()
    DEM = DIF.ewm(alpha = 1.0/float(XI),min_periods = XI).mean()
    OSC = DIF - DEM
    return DIF,DEM,OSC

__idc = [k,d,dma,wr,rsi,vip,vin,boll,variance]
__idn = ['k','d','dma','wr','rsi','vip','vin','boll','variance']
indices = dict(zip(__idn,__idc))
