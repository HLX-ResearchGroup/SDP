from .SDP import SDP
from .indices_lib import *
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

