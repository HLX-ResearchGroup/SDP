try:
    from quandl_set import *
except:
    import quandl
import numpy as np
import pandas as pd

class SDP:
    def __init__(self,**args):
        assert scodes in args
        self.rawdata = {}
    def get_raw_data(self):
        """
        download raw data with quandl and store it into self.rawdata
        """
        raise NotImplementedError

    def __call__(self,ptype = None,on = None,shuffle = False,split_ratio = 1):
        """
        process raw data and return traning/test data

        ptype(str): what kind of Y data to be returned, regression:float, classification: one hot matrix, unsupervised: no Y data
        on(str): which attribute to be predicted
        shuffle(bool): shuffle the training data or not
        split_ratio(float): precentage of data to be used as training data 
        """
        assert ptype in ['regression','classification','unsupervised']
        assert on in ['high','low','close','all',None]
        if ptype == 'unsupervised':
            on = None
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
        return self.raw_data.index[-1]
