from .SDP import SDP
class SDP2DCOV(SDP):
	def __init__(self,**args):
		SDP.__init__(self,args)
		assert 'indices' in args
		assert 'iwindow_size' in args
		assert 'jwindow_size' in args
		self.indices = args['indices']
		self.iwindow_size = args['iwindow_size']
		self.jwindow_size = args['jwindow_size']
		try:
			self.istride = args['istride']
		except:
			self.istride = 1
		try:
			self.jstride = args['jstride']
		except:
			self.jstride = 1
		self.get_raw_data()

	def 