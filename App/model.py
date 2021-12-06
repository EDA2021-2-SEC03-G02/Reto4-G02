"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

import math
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT.graph import gr
from DISClib.Utils import error as error
assert cf
from DISClib.ADT import orderedmap as om        
from math import radians, cos, sin, asin, sqrt
"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

def newAnalyzer():
    analyzer = {"Di-aeropuertos": None, "No-aeropuertos": None, "aeropuertos": None, "ciudad-iata": None, "ciudades_id": None, "ciudades_nombre": None}
    
    analyzer['Di-aeropuertos'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareStopIds)
    analyzer['NO-aeropuertos'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=14000,
                                              comparefunction=compareStopIds)
    analyzer['aeropuertos'] = mp.newMap(10000,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=compareartistMAP) 
    analyzer['ciudad-iata'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=14000,
                                              comparefunction=compareStopIds)
    analyzer['ciudades_id'] = mp.newMap(10000,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=compareartistMAP)
    analyzer["ciudades_nombre"] = mp.newMap(10000,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=compareartistMAP)
    analyzer["air"] = lt.newList()     
    analyzer["cit"] = lt.newList(datastructure="ARRAY_LIST")
    analyzer["air_iata"] = lt.newList()
    return analyzer                                   

def addAirport(analyzer, airport):
    mapa = analyzer["aeropuertos"]
    mp.put(mapa, airport["IATA"], airport)
    lista = analyzer["air"]
    lt.addLast(lista, airport)
    addRoutesGraphCities(analyzer, airport)
    addAirportVertex(analyzer, airport["IATA"])

def addRoutesGraph(analyzer, route):
    airport1 = route["Departure"]
    airport2 = route["Destination"]
    distance = route["distance_km"]
    addAirportVertex(analyzer, airport1)
    addAirportVertex(analyzer, airport2)
    addConnection(analyzer, airport1, airport2, distance)

def addRoutesGraphCities(analyzer, airport):
    iata = airport["IATA"]
    addGraphCitiesVertexIata(analyzer, iata)
    #lt.addLast(analyzer["air_iata"], iata)

def addConnection2(analyzer, iata, ciudad, distance):
    edge = gr.getEdge(analyzer['ciudad-iata'], iata, ciudad)
    if edge is None:
        gr.addEdge(analyzer['ciudad-iata'], iata, ciudad, distance)


def addGraphCitiesVertexIata(analyzer, info):
    try:
        if not gr.containsVertex(analyzer['ciudad-iata'], info):
            gr.insertVertex(analyzer['ciudad-iata'], info)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addstop')




def addAirportVertex(analyzer, airport):
    try:
        if not gr.containsVertex(analyzer['Di-aeropuertos'], airport):
            gr.insertVertex(analyzer['Di-aeropuertos'], airport)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addstop')

def addAirportVertexNO(analyzer, airport):
    try:
        if not gr.containsVertex(analyzer['NO-aeropuertos'], airport):
            gr.insertVertex(analyzer['NO-aeropuertos'], airport)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addstop')
    
def addConnectionNO(analyzer, airport1, airport2, distance):
    edge = gr.getEdge(analyzer['NO-aeropuertos'], airport1, airport2)
    if edge is None:
        gr.addEdge(analyzer['NO-aeropuertos'], airport1, airport2, distance)

def addConnection(analyzer, airport1, airport2, distance):
    edge = gr.getEdge(analyzer['Di-aeropuertos'], airport1, airport2)
    edge2 = gr.getEdge(analyzer['Di-aeropuertos'], airport2, airport1)
    #hacer todo aca para no dirijido, hacer edge 2 y revisar y todo eso
    #if edge is None:
    gr.addEdge(analyzer['Di-aeropuertos'], airport1, airport2, distance)
    if edge is not None and edge2 is not None:
        addAirportVertexNO(analyzer, airport1)
        addAirportVertexNO(analyzer, airport2)
        addConnectionNO(analyzer, airport1, airport2, distance)

    return analyzer




def addCiudad(analyzer, ciudad):
    mapa = analyzer["ciudades_id"]
    mp.put(mapa, ciudad["id"], ciudad)
    mapa1 = analyzer["ciudades_nombre"]
    updateCiudadesNombre(mapa1, ciudad)
    lt.addLast(analyzer["cit"], ciudad["id"])
    #addCiudadGrafoIATA_ciudad(analyzer, ciudad)

def addCiudadGrafoIATA_ciudad(analyzer, ciudad):
    addGraphCitiesVertexIata(analyzer, ciudad["id"])
    for airport in lt.iterator(analyzer["air"]):
        lat1 = airport["Latitude"]
        lon1 = airport["Longitude"]
        lat2 = ciudad["lat"]
        lon2 = ciudad["lng"]
        distancia = haversine(float(lon1), float(lat1), float(lon2), float(lat2))
        iata = airport["IATA"]
        city = ciudad["id"]
        addConnection2(analyzer, iata, city, distancia)
        print("OK")


def updateCiudadesNombre(mapa1, ciudad):
    nombre = ciudad['city']
    entry = mp.get(mapa1, nombre)
    if entry is None:
        cityentry = newCityEntry(ciudad)
        mp.put(mapa1, nombre, cityentry)
    else:
        cityentry = me.getValue(entry)
        addCityIndex(cityentry, ciudad)
    return mapa1

def newCityEntry(ciudad):
    entry = {'FirstCity': None}
    entry['FirstCity'] = lt.newList('ARRAY_LIST')
    First = entry['FirstCity']
    lt.addLast(First, ciudad)
    return entry

def addCityIndex(cityentry, ciudad):
    first= cityentry['FirstCity']
    lt.addLast(first,ciudad)
    return cityentry

def compareStopIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1

def totalAirports(grafo):
    return gr.numVertices(grafo)

def totalRoutes(grafo):
    return gr.numEdges(grafo)

def FirstAirport(analyzer):
    lista = analyzer["air"]
    primera = lt.firstElement(lista)
    return primera

def sizeLista(lista):
    return lt.size(lista), lt.lastElement(lista)

def infoUltimo(analyzer, ultimo):
    print(ultimo)
    mapa = analyzer["ciudades_id"]
    pareja = mp.get(mapa, ultimo)
    info = me.getValue(pareja)
    return info
def sizeMapa(analyzer):
    mapa = analyzer["ciudades_id"]
    return mp.size(mapa)



# Construccion de modelos

# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
def compareartistMAP(keyname, artist):
    artistEntry = me.getKey(artist)
    if (keyname == artistEntry):
        return 0
    elif (keyname > artistEntry):
        return 1
    else:
        return -1



#Req 3

def findCityName(analyzer, ciudad):
    mapa = analyzer["ciudades_nombre"]
    pareja = mp.get(mapa, ciudad)
    info = me.getValue(pareja)
    lista = info["FirstCity"]
    return lista

def getInfo(analyzer, id):
    mapa = analyzer["ciudades_id"]
    pareja = mp.get(mapa, id)
    info = me.getValue(pareja)
    return info



#Función para calcular la distancia en km de dos puntos con longitud y latitud. Retribuido del link disponible en la guía del laboratorio
#https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points creada por Michale Dunn para Stack Overflow
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r










