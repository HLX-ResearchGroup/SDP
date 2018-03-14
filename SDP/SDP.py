try:
    from quandl_set import *
except:
    import quandl
import numpy as np
import pandas as pd

class SDP:
    def __init__(self,**args):
        assert 'scode' in args
        self.scode = args['scode']
        self.rawdata = None
        self.rawdata_c = None
    def get_raw_data(self):
        """
        download raw data with quandl and store it into rawdata and rawdata_c
        """
        data = quandl.get("EOD/"+self.scode)[['Adj_Open','Adj_High','Adj_Low','Adj_Close','Adj_Volume']]
        data.columns = ['O','H','L','C','V']
        cl = data['C']
        c1 = cl.shift(1)
        lv = (data['V']+1).apply(np.log)
        self.rawdata = data
        self.rawdata_c = pd.DataFrame()
        self.rawdata_c['O'] = (self.rawdata['O']-c1)/c1
        self.rawdata_c['H'] = (self.rawdata['H']-c1)/c1
        self.rawdata_c['L'] = (self.rawdata['L']-c1)/c1
        self.rawdata_c['C'] = (cl-c1)/c1
        self.rawdata_c['V'] = lv - lv.shift(1)


    def __call__(self,on = None,shuffle = False,split_ratio = 1):
        """
        process raw data and return traning/test data

        ptype(str): what kind of Y data to be returned, regression:float, classification: one hot matrix, unsupervised: no Y data
        on(str): which attribute to be predicted
        shuffle(bool): shuffle the training data or not
        split_ratio(float): precentage of data to be used as training data 
        """

        assert on in ['H','L','C','all',None]
        assert split_ratio <= 1
        assert split_ratio >= 0
        return None

    def save(self,path):
        """
        save processed data from local
        """
        raise NotImplementedError

    def load(self,path):
        """
        load processed data from local
        """
        raise NotImplementedError

    def update(self,n):
        """
        update raw data and process
        n(int): add records of the least n days from quandl
        """
        raise NotImplementedError


    def last_updated(self):
        return self.rawdata.index[-1]