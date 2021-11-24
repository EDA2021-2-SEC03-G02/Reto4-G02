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
    analyzer['aeropuertos'] = mp.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)
    analyzer['ciudad-iata'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=14000,
                                              comparefunction=compareStopIds)
    analyzer['ciudades'] = mp.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)       
    return analyzer                                   

def addAirport(analyzer, airport):
    mapa = analyzer["aeropuertos"]
    mp.put(mapa, airport["IATA"], airport)

def addRoutesGraph(analyzer, route):
    airport1 = route["Departure"]
    airport2 = route["Destination"]
    distance = route["distance_km"]
    addAirportVertex(analyzer, airport1)
    addAirportVertex(analyzer, airport2)
    addConnection(analyzer, airport1, airport2, distance)

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
# Construccion de modelos

# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
