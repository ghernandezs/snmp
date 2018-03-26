# -*- coding: utf-8 -*-	
from Agente import Agente

class AgenteDAO:

	
	def __init__(self):
		self.source = "agentes.txt"
	def save(self,agente):
		file = open(self.source,'a')
		l = self.findAll()
		if(len(l)>0):	
			objStr="\nhost="+agente.getHost()+",version="+agente.getVersion()+",comunidad="+agente.getComunity()+",puerto="+str(agente.getPort())+",isActive="+str(agente.getIsActive()) 
		else:
			objStr="host="+agente.getHost()+",version="+agente.getVersion()+",comunidad="+agente.getComunity()+",puerto="+str(agente.getPort())+",isActive="+str(agente.getIsActive()) 	
		file.write(objStr)
		file.close()

	def findAll(self):
		l = []
		file = open(self.source,'r')
		line=(file.read()).split('\n')
		if(len(line)>0 and line[0] != ''):
			for i in line:
				agente= Agente()
				arr=i.split(',')
				agente.setHost(arr[0].split('=')[1])
				agente.setVersion(arr[1].split('=')[1])
				agente.setComunity(arr[2].split('=')[1])
				agente.setPort(arr[3].split('=')[1])
				agente.setIsActive(arr[4].split('=')[1])
				l.append(agente)
		file.close()
		return l	

	def findByHost(self,host):
		l = self.findAll()
		for obj in l: 
			if(obj.getHost() == host):
				return obj

	def deleteByHost(self,host):
		l = self.findAll()
		file = open(self.source,'w')		
		for agente in l:
			if(agente.getHost() != host):
				if(len(l)-2>0):	
					objStr="\nhost="+agente.getHost()+",version="+agente.getVersion()+",comunidad="+agente.getComunity()+",puerto="+str(agente.getPort())+",isActive="+str(agente.getIsActive())  
				else:
					objStr="host="+agente.getHost()+",version="+agente.getVersion()+",comunidad="+agente.getComunity()+",puerto="+str(agente.getPort())+",isActive="+str(agente.getIsActive()) 
				file.write(objStr)			
		file.close()

	def update(self,agente):
		self.deleteByHost(agente.getHost())
		self.save(agente)			