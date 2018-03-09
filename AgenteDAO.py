# -*- coding: utf-8 -*-
from Agente import Agente

class AgenteDAO:

	
	def __init__(self):
		self.source = "agentes.txt"
	def save(self,agente):
		file = open(self.source,'a')
		objStr="host="+agente.getHost()+",version="+agente.getVersion()+",comunidad="+agente.getComunity()+",puerto="+str(agente.getPort()) +"\n" 
		file.write(objStr)
		file.close()

	def findAll(self):
		file = open(self.source,'r')
		line=(file.read()).split('\n')
		l = []
		for i in line:
			agente= Agente()
			arr=i.split(',')
			agente.setHost(arr[0].split('=')[1])
			agente.setVersion(arr[1].split('=')[1])
			agente.setComunity(arr[2].split('=')[1])
			agente.setPort(arr[3].split('=')[1])
			l.append(agente)
		file.close()
		return l	

	def findByHost(self,host):
		l = self.findAll()
		for obj in l: 
			if(obj.getHost() == host):
				return obj

	def deleteByHost(self,host):
		#file = open(self.source,'w')		
		l = self.findAll()
		print len(l)
		for agente in l:
			print agente.getHost()
		#	if(agente.getHost() != host):
		#		objStr="host="+agente.getHost()+",version="+agente.getVersion()+",comunidad="+agente.getComunity()+",puerto="+str(agente.getPort()) +"\n" 
		#		file.write(objStr)
		#file.close()		