from .SDP import SDP
from .indices_lib import *
import os
import numpy as np

from mpl_finance import plot_day_summary2_ohlc
import matplotlib.pyplot as plt
import PIL.Image as Image


def default_cla_func(D):
    c = D.C

    d_change = (D.C - D.C.shift(1))/D.C.shift(1)
    if d_change.max()>0.05 and d_change.mean()>0.025 and D.L.iloc[-1] > D.H.iloc[0] and d_change.iloc[1]>-0.001:
        return np.ones(1)
    return np.zeros(1)

def optional_cla_func(D):
	if D.L.iloc[-1]>D.H.iloc[0]:
		return np.ones(1)
	return np.zeros(1)


class SDPIMG(SDP):
    def __init__(self,**args):
        SDP.__init__(self,**args)
        try:
            self.wsize = args['wsize']
        except:
            self.wsize = 20
        try:
            self.kd_p = args['kd_p']
        except:
            self.kd_p = 1
        try:
            self.wr_p = args['wr_p']
        except:
            self.wr_p = 14
        try:
            self.vot_p = args['vot_p']
        except:
            self.vot_p = 21
        self.get_raw_data()
        try:
            self.cla_func = args['cla_func']
        except:
            self.cla_func = optional_cla_func
        try:
            self.cla_days = args['cla_days']
        except:
            self.cla_days = 30
        try:
            self.w = args['w']
        except:
            self.w = 110
        try:
            self.h = args['h']
        except:
            self.h = 65

    def cook(self):
        s1,s2,dd = macd(self.rawdata,None)
        self.rawdata['K'] = k(self.rawdata,self.rawdata_c,self.kd_p)
        self.rawdata['D'] = d(self.rawdata,self.rawdata_c,self.kd_p)
        self.rawdata['R'] = wr(self.rawdata,self.rawdata_c,self.wr_p)
        self.rawdata['VIP'] = vip(self.rawdata,self.rawdata_c,self.vot_p)
        self.rawdata['VIN'] = vin(self.rawdata,self.rawdata_c,self.vot_p)
        self.rawdata['DIF'] = s1
        self.rawdata['DEM'] = s2
        self.rawdata['OSC'] = dd
        self.rawdata = self.rawdata.dropna()

    def __call__(self):
        X = []
        Y = []

        for i in range(0,len(self.rawdata)-self.wsize-self.cla_days-1):
            xD = self.rawdata.iloc[i:i+self.wsize]
            yD = self.rawdata.iloc[i+self.wsize:i+self.wsize+self.cla_days]
            y = self.cla_func(yD)
            x = []

            _,ax = plt.subplots(1,1,figsize = (4,2))
            plot_day_summary2_ohlc(
                colordown='black',
                colorup='yellow',
                closes=xD.C,
                highs=xD.H,
                lows=xD.L,
                opens=xD.O,
                ax=ax
            )
            ax.axes.get_xaxis().set_visible(False)
            ax.axes.get_yaxis().set_visible(False)
            ax.margins(0,0)
            plt.savefig('x.png', bbox_inches='tight')
            x_x = Image.open('x.png').convert('L')
            x.append(np.asarray(x_x))
            plt.clf()



            axx = plt.subplot(111,sharex = ax)
            axx.plot(xD.VIN.reset_index(drop=True),color = 'yellow')
            axx.plot(xD.VIP.reset_index(drop=True),color = 'black')
            axx.axes.get_xaxis().set_visible(False)
            axx.axes.get_yaxis().set_visible(False)
            axx.margins(0,0)
            plt.savefig('x.png', bbox_inches='tight')
            x_x = Image.open('x.png').convert('L')
            x.append(np.asarray(x_x))
            plt.clf()


            axxx = plt.subplot(111,sharex = ax)
            axxx.plot(xD.K.reset_index(drop = True),color = 'yellow')
            axxx.plot(xD.D.reset_index(drop = True),color = 'black')
            axxx.axes.get_xaxis().set_visible(False)
            axxx.axes.get_yaxis().set_visible(False)
            axxx.margins(0,0)
            plt.savefig('x.png', bbox_inches='tight')
            x_x = Image.open('x.png').convert('L')
            x.append(np.asarray(x_x))
            plt.clf()

            

            axx = plt.subplot(111,sharex = ax)
            axx.plot(xD.DIF.reset_index(drop = True),color = 'yellow')
            axx.plot(xD.DEM.reset_index(drop = True),color = 'black')
            axx.axes.get_xaxis().set_visible(False)
            axx.axes.get_yaxis().set_visible(False)
            axx.margins(0,0)
            plt.savefig('x.png', bbox_inches='tight')
            x_x = Image.open('x.png').convert('L')
            x.append(np.asarray(x_x))
            plt.clf()

            axxx = plt.subplot(111,sharex = ax)
            axxx.bar(range(self.wsize),xD.V)
            axxx.axes.get_xaxis().set_visible(False)
            axxx.axes.get_yaxis().set_visible(False)
            axxx.margins(0,0)
            plt.savefig('x.png', bbox_inches='tight')
            x_x = Image.open('x.png').convert('L')
            x.append(np.asarray(x_x))
            plt.clf()

            axx = plt.subplot(111,sharex = ax)
            axx.bar(range(self.wsize),xD.OSC)
            axx.axes.get_xaxis().set_visible(False)
            axx.axes.get_yaxis().set_visible(False)
            axx.margins(0,0)
            plt.savefig('x.png', bbox_inches='tight')
            x_x = Image.open('x.png').convert('L')
            x.append(np.asarray(x_x))
            plt.clf()

            plt.close()
            X.append(np.stack(x))
            Y.append(y)
#            print(X)
        try:
            return np.stack(X).transpose(0,2,3,1),np.stack(Y)
        except:
            print(X)
            print(Y)





