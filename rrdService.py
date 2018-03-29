import threading

import rrdtool
import time
from Agente import Agente


def crearBD(nombre):
	ret = rrdtool.create(nombre,
			"--start",'N',
			"--step",'20',
			"DS:paquetesIPEntrada:COUNTER:600:U:U",
			"DS:paquetesIPSalida:COUNTER:600:U:U",
			"DS:paquetesICMPEntrada:COUNTER:60:U:U",
			"DS:paquetesICMPSalida:COUNTER:600:U:U",
			"DS:conexionesTCP:COUNTER:600:U:U",
			"DS:paquetesTCPEntrada:COUNTER:600:U:U",
			"DS:paquetesTCPSalida:COUNTER:600:U:U",
			"DS:PaquetesSNMPEntrada:COUNTER:600:U:U",
			"DS:PaquetesSNMPSalida:COUNTER:600:U:U",		
			"RRA:AVERAGE:0.5:6:15",
			"RRA:AVERAGE:0.5:6:15",
			"RRA:AVERAGE:0.5:6:15",
			"RRA:AVERAGE:0.5:6:15",
			"RRA:AVERAGE:0.5:6:15",
			"RRA:AVERAGE:0.5:6:15",
			"RRA:AVERAGE:0.5:6:15",
			"RRA:AVERAGE:0.5:6:15",
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
	t = threading.currentThread()
	while getattr(t, "do_run", True):
		print "Reporting"
		rrdtool.graph( "paquetesIPEntrada_" + agente.getHost() + ".png",
	             		"--start",str(tiempo_actual),
			#"--end","N",
	             		"--vertical-label=Bytes/s",
	             		"DEF:tcpcon=dbPractica1.rrd:paquetesIPEntrada:AVERAGE",
	             		"AREA:tcpcon#00FF00:paquetesIPEntrada\r")
		rrdtool.graph( "paquetesIPSalida_" + agente.getHost() + ".png",
	             		"--start",str(tiempo_actual),
			#"--end","N",
	             		"--vertical-label=Bytes/s",
	             		"DEF:tcpcon=dbPractica1.rrd:paquetesIPSalida:AVERAGE",
	             		"AREA:tcpcon#00FF00:paquetesIPSalida\r")
		rrdtool.graph( "paquetesICMPEntrada_" + agente.getHost() + ".png",
	             		"--start",str(tiempo_actual),
			#"--end","N",
	             		"--vertical-label=Bytes/s",
	             		"DEF:tcpcon=dbPractica1.rrd:paquetesICMPEntrada:AVERAGE",
	             		"AREA:tcpcon#00FF00:paquetesICMPEntrada\r")
		rrdtool.graph( "paquetesICMPSalida_" + agente.getHost() + ".png",
	             		"--start",str(tiempo_actual),
			#"--end","N",
	             		"--vertical-label=Bytes/s",
	             		"DEF:tcpcon=dbPractica1.rrd:paquetesICMPSalida:AVERAGE",
	             		"AREA:tcpcon#00FF00:paquetesICMPSalida\r")
		rrdtool.graph( "Reporte1_" + agente.getHost() + ".png",
	             		"--start",str(tiempo_actual),
			#"--end","N",
	             		"--vertical-label=Bytes/s",
	             		"DEF:tcpcon=dbPractica1.rrd:conexionesTCP:AVERAGE",
	             		"AREA:tcpcon#00FF00:conexionesTCP\r")
		rrdtool.graph( "paquetesTCPEntrada_" + agente.getHost() + ".png",
	             		"--start",str(tiempo_actual),
			#"--end","N",
	             		"--vertical-label=Bytes/s",
	             		"DEF:tcpcon=dbPractica1.rrd:paquetesTCPEntrada:AVERAGE",
	             		"AREA:tcpcon#00FF00:paquetesTCPEntrada\r")
		rrdtool.graph( "paquetesTCPSalida_" + agente.getHost() + ".png",
	             		"--start",str(tiempo_actual),
			#"--end","N",
	             		"--vertical-label=Bytes/s",
	             		"DEF:tcpcon=dbPractica1.rrd:paquetesTCPSalida:AVERAGE",
	             		"AREA:tcpcon#00FF00:paquetesTCPSalida\r")
		rrdtool.graph( "PaquetesSNMPEntrada_" + agente.getHost() + ".png",
	             		"--start",str(tiempo_actual),
			#"--end","N",
	             		"--vertical-label=Bytes/s",
	             		"DEF:tcpcon=dbPractica1.rrd:PaquetesSNMPEntrada:AVERAGE",
	             		"AREA:tcpcon#00FF00:PaquetesSNMPEntrada\r")
		rrdtool.graph( "PaquetesSNMPSalida_" + agente.getHost() + ".png",
	             		"--start",str(tiempo_actual),
			#"--end","N",
	             		"--vertical-label=Bytes/s",
	             		"DEF:tcpcon=dbPractica1.rrd:PaquetesSNMPSalida:AVERAGE",
	             		"AREA:tcpcon#00FF00:PaquetesSNMPSalida\r")	             			             			             			             				
		time.sleep(30)
	return

