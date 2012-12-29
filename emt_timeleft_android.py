#import library to do http requests:
import urllib2
 
#import easy to use xml parser called minidom:
from xml.dom.minidom import *

import android
droid = android.Android()

passkey = '0810DDE4-02FC-4C0E-A440-1BD171B397C8'
idClient = "WEB.PORTALMOVIL.OTROS"

parada = str(droid.dialogGetInput('EMT Timeleft','Inserte Numero de Parada').result)

linea_query = str(droid.dialogGetInput('EMT Timeleft','Inserte Numero de Linea').result)

print("")

#download the file:
file = urllib2.urlopen('https://servicios.emtmadrid.es:8443/geo/servicegeo.asmx/getArriveStop?idClient='+idClient+'&passKey='+passkey+'&idStop='+parada+'&statistics=&cultureInfo=')
#convert to string:
data = file.read()
#close file because we dont need it anymore:
file.close()
#parse the xml you downloaded
dom = parseString(data)
nodos = dom.childNodes
lista = nodos[0].getElementsByTagName("Arrive")

#each nodo represents a bus
for nodo in lista:
	linea = nodo.getElementsByTagName("idLine")[0].toxml().replace('<idLine>','').replace('</idLine>','')
	destino = nodo.getElementsByTagName("Destination")[0].toxml().replace('<Destination>','').replace('</Destination>','')
	tiempo = int(nodo.getElementsByTagName("TimeLeftBus")[0].toxml().replace('<TimeLeftBus>','').replace('</TimeLeftBus>',''))/60
	if tiempo==16666:
		tiempo = "mas de 20"
	distancia = nodo.getElementsByTagName("DistanceBus")[0].toxml().replace('<DistanceBus>','').replace('</DistanceBus>','')

	texto = "Bus de la Linea "+ str(linea) +" con destino "+ destino+ " a " +str(tiempo)+" minutos, "+str(distancia)+ " metros."

	if int(linea_query) == int(linea) or int(linea_query)==0:
		print texto
		droid.notify('Parada: '+str(parada)+'  Linea: '+ str(linea) , 'Tiempo: '+str(tiempo)+' minutos.  ('+str(distancia)+ " m)")
		droid.ttsSpeak(texto)