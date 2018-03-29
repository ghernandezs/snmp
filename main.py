import threading
import time
import os
import rrdtool

from getSNMP import consultaSNMP

from Agente import Agente
from AgenteDAO import AgenteDAO
import rrdService

oidsarr = {"os":"1.3.6.1.2.1.1.1.0",
"upTime":"1.3.6.1.2.1.1.3.0","interfacesNumber":"1.3.6.1.2.1.2.1.0","interfaceIndex":"1.3.6.1.2.1.2.2.1.","ipIn":"1.3.6.1.2.1.4.3.0","ipOut":"1.3.6.1.2.1.4.10.0","icmpIn":"1.3.6.1.2.1.5.1.0","icmpOut":"1.3.6.1.2.1.5.14.0","tcpCon":"1.3.6.1.2.1.6.5.0","tcpIn":"1.3.6.1.2.1.6.10.0","tcpOut":"1.3.6.1.2.1.6.11.0","snmpIn":"1.3.6.1.2.1.11.1.0","snmpOut":"1.3.6.1.2.1.11.2.0"}

def  addAgente():
	agenteDAO = AgenteDAO()
	host = str(raw_input("Agregar host o ip :\n"))
	version = str(raw_input("Agregar version de snmp:\n"))
	comunity = str(raw_input("Agregar comunidad:\n"))
	port = str(raw_input("Agregar Puerto:\n"))

	agente = Agente(host,version,comunity,port)
 	agenteDAO.save(agente)

def showAgents():
	agenteDAO = AgenteDAO()
	l = agenteDAO.findAll()
	if(len(l)>0):
		for obj in l:
			print obj.getHost() + " " +obj.getIsActive()

	else:
		print "No hay agentes Agregados"
	print "\n"					
def deleteDevice():
	agenteDAO = AgenteDAO()
	host=str(raw_input("ingresar host o ip  a eliminar :\n"))
	try:
		agenteDAO.deleteByHost(host)
	except Exception, e:
		print e

def startStopDevice():
	print "Iniciar/Detener Aente"	
	showAgents()

def main():
	while 1:
		print "seleccionar Opcion"
		print "1.Agregar Dispositivos"
		print "2.Mostrar Dispoditivo"
		print "3.Eliminar dispoditivo"
		print "4.Iniciar/Detener agente"
		print "5.mostrar reporte agente"
		opcion = int(raw_input("\n"))

		if(opcion == 1):
			addAgente()
		elif(opcion == 2):
			showAgents()
		elif(opcion == 3):
			deleteDevice()
		elif(opcion == 4):
			startStopDevice()
		elif(opcion == 5):
			print "opcion 5"	
		else:
			print "opcion no valida" 

def getOS(agente):
	return consultaSNMP(agente.getComunity(),agente.getHost(),oidsarr['os'],agente.getPort())

def getInterfacesNumber(agente):
	return consultaSNMP(agente.getComunity(),agente.getHost(),oidsarr['interfacesNumber'],agente.getPort())

def getInterfaceStatus(agente,i):
		status = "up " if consultaSNMP(agente.getComunity(),agente.getHost(),oidsarr['interfaceIndex']+str(i)+".8",agente.getPort()) == 1 else "down"	
		print  consultaSNMP(agente.getComunity(),agente.getHost(),oidsarr['interfaceIndex']+str(i)+".2",agente.getPort())+ "  "+ status	    	
def monitorear(agente):
 
  	print "monitoreando a " + agente.getHost()

	total_input_traffic = 0
	total_output_traffic = 0

	t = threading.currentThread()
	while getattr(t, "do_run", True):
		
		ipIn = int(consultaSNMP(agente.getComunity(),agente.getHost(), oidsarr['ipIn'],agente.getPort()))
		ipOut = int(consultaSNMP(agente.getComunity(),agente.getHost(), oidsarr['ipOut'],agente.getPort()))
		icmpIn = int(consultaSNMP(agente.getComunity(),agente.getHost(), oidsarr['icmpIn'],agente.getPort()))
		icmpOut = int(consultaSNMP(agente.getComunity(),agente.getHost(), oidsarr['icmpOut'],agente.getPort()))
		tcpCon =int(consultaSNMP(agente.getComunity(),agente.getHost(), oidsarr['tcpCon'],agente.getPort()))
		tcpIn =int(consultaSNMP(agente.getComunity(),agente.getHost(), oidsarr['tcpIn'],agente.getPort()))
		tcpOut = int(consultaSNMP(agente.getComunity(),agente.getHost(), oidsarr['tcpOut'],agente.getPort()))
		snmpIn = int(consultaSNMP(agente.getComunity(),agente.getHost(), oidsarr['snmpIn'],agente.getPort()))
		snmpOut = int(consultaSNMP(agente.getComunity(),agente.getHost(), oidsarr['snmpOut'],agente.getPort()))
		valor ='N:'+str(ipIn) + ':' + str(ipOut)+':'+str(icmpIn)+':'+str(icmpOut)+':'+ str(tcpCon)+':'+str(tcpIn)+':'+str(tcpOut)+':'+str(snmpIn)+':'+str(snmpOut) 
		#print valor
		rrdtool.update('dbPractica1.rrd', valor)
    	rrdtool.dump('dbPractica1.rrd','dbPractica1.xml')
    	time.sleep(1)
	if ret:
   		print rrdtool.error()
    	time.sleep(300)
	
def createReportThread(agente):
	r = threading.Thread(target=rrdService.report, args=[agente])
	return r
def createThread(agente):
	t = threading.Thread(target=monitorear, args=[agente])
	return t			


agenteDAO = AgenteDAO()
l = agenteDAO.findAll()
try:
	for agente in l:
		print "***************************************************************************"
		response = os.system("ping -c 1 " + agente.getHost())
		if(response == 0):
			agente.setIsActive(True)
			agenteDAO.update(agente)
			t = createThread(agente)
			t.setName(agente.getHost())
			t.start()
			r = createReportThread(agente)
			r.start()
			intNum = getInterfacesNumber(agente)
			print agente.getHost() +"  sistema operativo: " +getOS(agente) +" status: activo"+ "  interfaces: " + str(intNum) 
			for i in range(0,int(intNum)):
				getInterfaceStatus(agente,i) 

		else:
			agente.setIsActive(False)
			agenteDAO.update(agente)	
			print agente.getHost() +"  status: inactivo" 
		print "***************************************************************************"	
except Exception, e:
	raise

mainThread = threading.Thread(target=main())
#t1 = createThread("thread1")
#t2 = createThread("treaded2")
 
#t1.start()
#t2.start()
#mainThread.start()
#time.sleep(5)
#t1.do_run = False
#t2.do_run = False
