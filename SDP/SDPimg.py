from .SDP import SDP
from .indices_lib import *
import os
import numpy as np

class SDPIMG(SDP):
    def __init__(self,**args):
        SDP.__init__(self,**args)
        self.wsize = args['wsize']

        self.get_raw_data()
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
    def cook(self):

        self.rawdata['K'] = k(self.rawdata,self.rawdata_c,self.kd_p)
        self.rawdata['D'] = d(self.rawdata,self.rawdata_c,self.kd_p)
        self.rawdata['R'] = wr(self.rawdata,self.rawdata_c,self.wr_p)
        self.rawdata['VIP'] = vip(self.rawdata,self.rawdata_c,self.vot_p)
        self.rawdata['VIN'] = vin(self.rawdata,self.rawdata_c,self.vot_p)
