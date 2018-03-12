class Agente:
	def __init__(self, host = "",version ="",comunity= "",port=0):
		self.host = host
		self.version = version
		self.comunity = comunity
		self.port = port
		self.isActive= False

	def getHost(self):
		return self.host
	def setHost(self,host):
		self.host = host
	
	def getVersion(self):
		return 	self.version
	def setVersion(self,version):
		self.version = version

	def getComunity(self):	
		return self.comunity

	def setComunity(self,comunity):
		self.comunity = comunity

	def getPort(self):
		return self.port
	def setPort(self,port):
		self.port = port

	def setIsActive(self,isActive):
		self.isActive=isActive

	def getIsActive(self):
		return self.isActive		 							