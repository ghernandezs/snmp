import rrdtool
import time
from Agente import Agente


def crearBD(nombre):
	ret = rrdtool.create(nombre,
			"--start",'N',
			"--step",'20',
			"DS:ConexionesTcp:COUNTER:600:U:U",
			"RRA:AVERAGE:0.5:6:15"
			)
	if ret:
		print( rrdtool.error() )

def saveTorrd(valor):
	rrdtool.update('dbPractica1.rrd', valor)
	rrdtool.dump('dbPractica1.rrd','dbPractica1.xml')
	time.sleep(1)

def report(agente):
	tiempo_actual = int(time.time())
	tiempo_final = tiempo_actual - 86400
	tiempo_inicial = tiempo_final -25920000
	#while agente.getIsActive():
	rrdtool.graph( "Reporte1_" + agente.getHost() + ".png",
             		"--start",str(tiempo_actual),
		#"--end","N",
             		"--vertical-label=Bytes/s",
             		"DEF:tcpcon=dbPractica1.rrd:ConexionesTcp:AVERAGE",
             		"AREA:tcpcon#00FF00:ConexionesTCP\r")
	time.sleep(30)
	return

