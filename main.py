from Agente import Agente
from AgenteDAO import AgenteDAO

#agente =Agente("localHost","v1","comunidadSNMP",161)
#print agente.getHost()
#print agente.getVersion()
#print agente.getComunity()
#print agente.getPort()

agenteDAO = AgenteDAO();
#agenteDAO.save(agente);
agenteDAO.deleteByHost("localHost2")
#print agente.getHost()