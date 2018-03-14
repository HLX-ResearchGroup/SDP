from .SDP import SDP
from .indices_lib import *
import os
import numpy as np
class SDP2DCONV(SDP):
    def __init__(self,**args):
        SDP.__init__(self,**args)
        assert 'indices' in args
        assert 'istop' in args
        self.indices = args['indices']
        self.istop = args['istop']

        try:
            self.istride = args['istride']
        except:
            self.istride = 1

        self.get_raw_data()

    def cook(self):
        self.channels = {}
        for index in self.indices:
            self.channels[index] = pd.DataFrame()
            for i in range(1,self.istop,self.istride):
                self.channels[index][i] = indices[index](self.rawdata,self.rawdata_c,i)
            self.channels[index] = self.channels[index].fillna(0).replace(np.inf,0)
    def save(self,pth = None):
        if pth is None:
            pth = "{}_{}_{}/".format(self.scode,self.istop,self.istride)
        if not os.path.exists(pth):
            os.mkdir(pth)
        for c in self.channels:
            self.channels[c].to_csv(pth+c+'.csv')
    def __call__(self,on = 'C',shuffle = False, split_ratio = 0,evi_days = 60):
        X_Tr = None
        X_Te = None
        Y_Tr = None
        Y_Te = None
        X = []
        Y = []
        for i in range(evi_days+1,len(self.rawdata)):
            x = []
            for c in sorted(self.channels.keys()):
                x.append(self.channels[c].iloc[i-evi_days:i].values)
            X.append(np.stack(x,axis = -1))
            Y.append(self.rawdata_c[on].iloc[i:i+1].values)

        X_Tr = np.stack(X)
        Y_Tr = np.stack(Y)
        L = len(X_Tr)*split_ratio
        X_Te = X_Tr[:L,:,:,:]
        Y_Te = Y_Tr[:L,:]
        X_Tr = X_Tr[L:,:,:,:]
        Y_Tr = Y_Tr[L:,:]
        return {'XTR':X_Tr,'XTE':X_Te,'YTR':Y_Tr,'YTE':Y_Te}
