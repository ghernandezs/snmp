import threading
import time
import os
import rrdtool

from getSNMP import consultaSNMP

from Agente import Agente
from AgenteDAO import AgenteDAO
from Agente import Agente

oidsarr = {"os":"1.3.6.1.2.1.1.1.0",
"upTime":"1.3.6.1.2.1.1.3.0","interfacesNumber":"1.3.6.1.2.1.2.1.0","interfaceIndex":"1.3.6.1.2.1.2.2.1.","ipIn":"1.3.6.1.2.1.4.3.0","ipOut":"1.3.6.1.2.1.4.10.0"}

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
			print "opcion 4"
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

def ipStats(agente):
	pkgIn = int(consultaSNMP(agente.getComunity(),agente.getHost(), oidsarr['ipIn'],agente.getPort()))
	pkgOut = int(consultaSNMP(agente.getComunity(),agente.getHost(), oidsarr['ipOut'],agente.getPort()))
    	
def monitorear(agente):

	total_input_traffic = 0
	total_output_traffic = 0

	t = threading.currentThread()

	while getattr(t, "do_run", True):
		ipStats(agente)
		#total_input_traffic = int(consultaSNMP('comunidadSNMP',agente.getHost(),'1.3.6.1.2.1.2.2.1.10.3'))
    	#total_output_traffic = int(consultaSNMP('comunidadSNMP',agente.getHost(),'1.3.6.1.2.1.2.2.1.16.3'))
	    #total_input_traffic = int(consultaSNMP(agente.getComunity(),agente.getHost(),'1.3.6.1.2.1.2.2.1.10.3'))
	    #total_output_traffic = int(consultaSNMP(agente.getComunity(),agente.getHost(),'1.3.6.1.2.1.2.2.1.16.3'))

	    #valor = agente.getHost()+":" + str(total_input_traffic) + ':' + str(total_output_traffic)
	    #print valor
	    #rrdtool.update('net3.rrd', valor)
	    #rrdtool.dump('net3.rrd','net3.xml')
	    #time.sleep(1)

	#if ret:
   	#	print rrdtool.error()
    #	time.sleep(300)
	

def createThread(agente):
	t = threading.Thread(target=monitorear, args=[agente])
	return t			

#if __name__ == "__main__":
agenteDAO = AgenteDAO()
l = agenteDAO.findAll()
try:
	for agente in l:
		print "***************************************************************************"
		response = os.system("ping -c 1 " + agente.getHost())
		if(response == 0):
			t = createThread(agente)
			t.setName(agente.getHost())
			t.start()
			intNum = getInterfacesNumber(agente)
			print agente.getHost() +"  sistema operativo: " +getOS(agente) +" status: activo"+ "  interfaces: " + str(intNum) 
			for i in range(0,int(intNum)):
				getInterfaceStatus(agente,i) 

		else:
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


