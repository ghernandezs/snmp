import time
import rrdtool
from getSNMP import consultaSNMP

total_input_traffic = 0
total_output_traffic = 0


while 1:
    total_input_traffic = int(consultaSNMP('comunidadSNMP','192.168.1.69','1.3.6.1.2.1.2.2.1.10.3'))
    total_output_traffic = int(consultaSNMP('comunidadSNMP','192.168.1.69','1.3.6.1.2.1.2.2.1.16.3'))

    valor = "N:" + str(total_input_traffic) + ':' + str(total_output_traffic)
    print valor
    rrdtool.update('net3.rrd', valor)
    rrdtool.dump('net3.rrd','net3.xml')
    time.sleep(1)

if ret:
    print rrdtool.error()
    time.sleep(300)
