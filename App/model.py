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

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

def newAnalyzer():
    analyzer = {"Di-aeropuertos": None, "No-aeropuertos": None, "aeropuertos": None, "ciudad-iata": None, "ciudades": None}
    
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
    analyzer['ciudades'] = mp.newMap(10000,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=compareartistMAP)
    analyzer["air"] = lt.newList()     
    analyzer["cit"] = lt.newList(datastructure="ARRAY_LIST")
    return analyzer                                   

def addAirport(analyzer, airport):
    mapa = analyzer["aeropuertos"]
    mp.put(mapa, airport["IATA"], airport)
    lista = analyzer["air"]
    lt.addLast(lista, airport)
    addRoutesGraphCities(analyzer, airport)

def addRoutesGraph(analyzer, route):
    airport1 = route["Departure"]
    airport2 = route["Destination"]
    distance = route["distance_km"]
    addAirportVertex(analyzer, airport1)
    addAirportVertex(analyzer, airport2)
    addConnection(analyzer, airport1, airport2, distance)

def addRoutesGraphCities(analyzer, airport):
    iata = airport["IATA"]
    ciudad = airport["City"]
    distance = distanciaCoordenadas(iata, ciudad)
    addGraphCitiesVertexIata(analyzer, iata)
    addGraphCitiesVertexCit(analyzer, ciudad)
    addConnection2(analyzer, iata, ciudad, distance)

def addConnection2(analyzer, iata, ciudad, distance):
    edge = gr.getEdge(analyzer['ciudad-iata'], iata, ciudad)
    if edge is None:
        gr.addEdge(analyzer['ciudad-iata'], iata, ciudad, distance)

def distanciaCoordenadas(iata, ciudad):
    return 1

def addGraphCitiesVertexIata(analyzer, info):
    try:
        if not gr.containsVertex(analyzer['ciudad-iata'], info):
            gr.insertVertex(analyzer['ciudad-iata'], info)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addstop')

def addGraphCitiesVertexCit(analyzer, info):
    try:
        if not gr.containsVertex(analyzer['ciudad-iata'], info):
            gr.insertVertex(analyzer['ciudad-iata'], info)
            lt.addLast(analyzer["cit"], info)
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
    if edge is None:
        gr.addEdge(analyzer['Di-aeropuertos'], airport1, airport2, distance)
    if edge is not None and edge2 is not None:
        addAirportVertexNO(analyzer, airport1)
        addAirportVertexNO(analyzer, airport2)
        addConnectionNO(analyzer, airport1, airport2, distance)

    return analyzer




def addCiudad(analyzer, ciudad):
    mapa = analyzer["ciudades"]
    mp.put(mapa, ciudad["city"], ciudad)

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
    ultimo = ultimo.replace(" City", "")
    mapa = analyzer["ciudades"]
    pareja = mp.get(mapa, ultimo)
    print(pareja)
    info = me.getValue(pareja)
    return info




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


#Código para calcular la distancia entre dos coordenadas, basado en el código publicado en: http://www.codecodex.com/wiki/Calculate_Distance_Between_Two_Points_on_a_Globe#Python

def decdeg2dms(dd):
    mnt,sec = divmod(dd*3600,60)
    deg,mnt = divmod(mnt,60)
    return deg,mnt,sec

def recalculate_coordinate(val,  _as=None):

  deg,  min,  sec = val
  # pass outstanding values from right to left
  min = (min or 0) + int(sec) / 60
  sec = sec % 60
  deg = (deg or 0) + int(min) / 60
  min = min % 60
  # pass decimal part from left to right
  dfrac,  dint = math.modf(deg)
  min = min + dfrac * 60
  deg = dint
  mfrac,  mint = math.modf(min)
  sec = sec + mfrac * 60
  min = mint
  if _as:
    sec = sec + min * 60 + deg * 3600
    if _as == 'sec': return sec
    if _as == 'min': return sec / 60
    if _as == 'deg': return sec / 3600
  return deg,  min,  sec
      
def points2distance(start,  end):
    longitudciudad=decdeg2dms(start[1])
    longitudAirport=decdeg2dms(end[1])
    latitudciudad=decdeg2dms(start[0])
    latitudAirport=decdeg2dms(end[0])

    start_long = math.radians(recalculate_coordinate(longitudciudad,  'deg'))
    start_latt = math.radians(recalculate_coordinate(latitudciudad,  'deg'))
    end_long = math.radians(recalculate_coordinate(longitudAirport,  'deg'))
    end_latt = math.radians(recalculate_coordinate(latitudAirport,  'deg'))
    d_latt = end_latt - start_latt
    d_long = end_long - start_long
    a = math.sin(d_latt/2)**2 + math.cos(start_latt) * math.cos(end_latt) * math.sin(d_long/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return 6371 * c

