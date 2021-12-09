"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 """


import config as cf
import sys
import controller
import threading
from DISClib.ADT import list as lt
assert cf
sys.setrecursionlimit(2 ** 21)

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
airports = "airports-utf8-small.csv"
routes = "routes-utf8-small.csv"
cities = "worldcities.csv"

def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de los vuelos del mundo")
    print("3- Encontrar puntos de interconexión aérea")
    print("4- Encont1rar clústeres de tráfico aéreo y saber si dos aeropuertos pertenecen a esta")
    print("5- Encontrar la ruta más corta entre dos ciudades")
    print("6- Utilizar millas de viajero para conocer la mayor cantidad de ciudades")
    print("7- Cuantificar el efecto de un aeropuerto cerrado")
    print("0- Salir")
    print("*******************************************")

catalog = None

def printPrimero(primero):
    print("Nombre: " +primero["Name"]+", Ciudad: "+primero["City"]+", País: "+primero["Country"]+", Latitud: "+primero["Latitude"]+", Longitud: "+primero["Longitude"])

def printInfoUltimo(ultimo):
    print("Nombre: " +ultimo["city"]+ ", Poblacion: " +ultimo["population"]+", Latitud: "+ultimo["lat"] +", Longitud: "+ultimo["lng"])

def printListaCiudades(lista):
    for ciudad in lt.iterator(lista):
        print("**"*56)
        print("Nombre: " +ciudad["city"]+", País: "+ciudad["country"]+", Latitud: "+ciudad["lat"]+", Longitud: "+ciudad["lng"]+", ID: "+ciudad["id"])

def printMasConectados(lista,cont):
    for tupla in lt.iterator(lista):
        iata = tupla[0]
        total = tupla[1]
        inbound = tupla[2]
        outbound = tupla[3]
        info_iata = controller.infoIata(iata, cont)
        nombre = info_iata[0]
        ciudad = info_iata[1]
        pais = info_iata[2]
        print("**"*56)
        print("Nombre: " + nombre+", Ciudad: "+ciudad+", País: "+pais+", Total de Conexiones: "+str(total)+", Conexiones Entrantes: "+str(inbound)+", Conexiones Salientes: "+str(outbound))

def print3airports(lista):
    tamanio = lt.size(lista)
    if tamanio<6:
        print("A continuación todos lo aeropuertos afectados:")
        for x in lt.iterator(lista):
            primero = controller.infoAirport(cont, x)
            print("IATA: "+primero["IATA"]+", Nombre: " +primero["Name"]+", Ciudad: "+primero["City"]+", País: "+primero["Country"])
    else:
            primeros3 = lt.subList(lista, 1, 3)
            ultimos3 = lt.subList(lista, lt.size(lista)-2, 3)
            print("A continuación los primeros 3 aeropuertos afectados:")
            for x in lt.iterator(primeros3):
                primero = controller.infoAirport(cont, x)
                print("IATA: "+primero["IATA"]+", Nombre: " +primero["Name"]+", Ciudad: "+primero["City"]+", País: "+primero["Country"])
            print("A continuación los últimos 3 aeropuertos afectados")
            for x in lt.iterator(ultimos3):
                primero = controller.infoAirport(cont, x)
                print("IATA: "+primero["IATA"]+", Nombre: " +primero["Name"]+", Ciudad: "+primero["City"]+", País: "+primero["Country"])
    
def printRecorridos(lista):
    for element in lt.iterator(lista):
        print("Origen: "+element["vertexA"]+", Destino: "+element["vertexB"]+", Distancia en Km: "+str(element["weight"]))
        print("**"*56)

def printMST(lista):
    for element in lt.iterator(lista):
        print("Aeropuerto Origen: "+element["vertexA"]+", Aeropuerto Destino: "+element["vertexB"]+", Distancia (km): "+str(element["weight"]))

def option2(cont):
    print("Cargando la información de vuelos, rutas, aeropuertos y ciudades")
    controller.loadTodo(cont, airports, routes, cities)
    primero = controller.FirstAirport(cont)
    print("Informacion del primer aeropuerto en ser cargado:")
    print("El primer aeropuerto cargado fue: ")
    printPrimero(primero)
    grafo1 = cont["Di-aeropuertos"]
    numedges1 = controller.totalRoutes(grafo1)
    numvertex1 = controller.totalAirports(grafo1)
    grafo2 = cont["NO-aeropuertos"]
    numedges2 = controller.totalRoutes(grafo2)
    numvertex2 = controller.totalAirports(grafo2)
    grafo3 = cont["ciudad-iata"]
    numedges3 = controller.totalRoutes(grafo3)
    numvertex3 = controller.totalAirports(grafo3)
    lista = cont["cit"]
    tamanio = controller.sizeLista(lista)[0]
    ultimo = controller.sizeLista(lista)[1]
    info_utlimo = controller.infoUltimo(cont, ultimo)
    tamanio1 = controller.sizeMapa(cont)
    print("**"*56)
    print("Información del Digrafo de aeropuertos conectados por vuelos entre sí")
    print("Numero de vertices (aeropuertos): " +str(numvertex1))
    print("Numero de arcos: " +str(numedges1))
    print("**"*56)
    print("Informacion del grafo NO dirigido de aeropuertos con vuelos disponibles en ambas direcciones")
    print("Numero de vertices (aeropuertos): " +str(numvertex2))
    print("Numero de arcos: " +str(numedges2))
    print("**"*56)
    """print("Información del grafo no direccionado que representa las ciudades y sus aeropuertos")
    print("Numero de vertices (aeropuertos y ciudades): " +str(numvertex3))
    print("Numero de arcos: " +str(numedges3))
    print("Total de ciudades en el grafo: "+str(tamanio))"""
    print("Información de la última ciudad cargada en el grafo: ")
    printInfoUltimo(info_utlimo)
    print("**"*56)
    
    

    

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Inicializando")
        cont = controller.init()
    elif int(inputs[0]) == 2:
        option2(cont)
    elif int(inputs[0]) == 3:
        tupla = controller.Top5Conectados(cont)
        lista = tupla[0]
        tamanio = tupla[1]
        print("El número de aeropuertos conectados en el grafo es: "+str(tamanio))
        print("A continuación se muestran los 5 aeropuertos más interconectados")
        printMasConectados(lista, cont)
        
    elif int(inputs[0]) == 4:
        iata1 = input("Por favor escriba el nombre del código IATA del aeropuerto 1: ")
        iata2 = input("Por favor escriba el nombre del código IATA del aeropuerto 2: ")
        info = controller.FindSCC(cont, iata1, iata2)
        airport1 = controller.infoAirport(cont, iata1)
        airport2 = controller.infoAirport(cont, iata2)
        print("Existen "+str(info[0])+" elementos fuertemente conectados (SCC) en el grafo de aeropuertos rutas")
        existe = info[1]
        print("En este caso, los aeropuertos "+airport1["Name"]+ " y "+airport2["Name"]+" "+existe+" hacen parte del mismo clúster")
    elif int(inputs[0]) == 5:
        ciudad1 = input("Por favor escriba el nombre de la ciudad de origen: ")
        opciones1 = controller.findCityName(cont, ciudad1)
        print("A continuación se muestran todas las posibles opciones de ciudades con el nombre "+ciudad1)
        printListaCiudades(opciones1)
        id1 = input("Por favor digite el código de la ciudad que desea seleccionar como origen del recorrido: ")
        print("Ciudad de origen guardada")
        ciudad2 = input("Por favor escriba el nombre de la ciudad de destino: ")
        print("A continuación se muestran todas las posibles opciones de ciudades con el nombre "+ciudad1)
        opciones2 = controller.findCityName(cont, ciudad2)
        printListaCiudades(opciones2)
        id2 = input("Por favor digite el código de la ciudad que desea seleccionar como destino: ")
        print("Ciudad de destino guardada")
        print("Inciando búsqueda de la ruta más corta entre las ciudades con ID "+id1+" y "+id2)
        origen = controller.getAirportCity(cont, id1)
        partida = origen[0]
        d1 = origen[1]
        d1 = round(d1, 3)
        partida1 = controller.infoAirport(cont, partida)
        destino = controller.getAirportCity(cont, id2)
        llegada = destino[0]
        llegada1 = controller.infoAirport(cont,llegada)
        d2 = destino[1]
        d2 = round(d2,3)
        print("")
        print("El aeropuerto que se usará como punto de partida está a una distancia de "+str(d1)+" Km de la ciudad elegida como origen")
        print("Ahora, la información de dicho aeropuerto:")
        printPrimero(partida1)
        print("")
        print("El aeropuerto que se usará como punto de llegada está a una distancia de "+str(d2)+" Km de la ciudad elegida como destino")
        print("Ahora, la información de dicho aeropuerto:")
        printPrimero(llegada1)
        cortos = controller.RutaMenorCosto(cont, partida, llegada)
        print("")
        print("A continuación la ruta más corta (en distancia) para poder llegar desde el aeropuerto de origen hasta el aeropuerto de destino: ")
        print("**"*56)
        printRecorridos(cortos[1])
        distancia_total = d1+d2+cortos[0]
        print("")
        print("La distancia total para hacer este recorrido en Km (incluyendo la distancia necesaria para llegar de la ciudad origen al aeropuerto origen\ny la necesaria para llegar del aeropuerto destino a la ciudad destino) es de: "+str(distancia_total))        
    elif int(inputs[0]) == 6:
        millas = float(input("Por favor escriba su cantidad de millas de viajero: "))
        km = round(millas*1.60,3)
        info = controller.RutaMasParadas(cont)
        lista = info[0]
        peso = round(info[1],3)
        num_vertices = info[2]
        print("Existe un total de "+str(num_vertices)+ " posibles aeropuertos en el MST\n")
        print("El distancia total (weight o peso del MST) es de "+str(peso)+" Km.")
        print("En este caso, el usuario cuenta con "+str(millas)+" millas. Es decir, "+str(km)+" kilómetros.")
        if km>=peso:
            d = km-peso
            print("Por ende, el usuario puede cumplir con el recorrido del MST, y le sobran "+str(d)+" kilómetros")
        else:
            d = peso-km
            print("Por ende, el usuario no puede cumplir con el recorrido del MST, ya que le faltan "+str(d)+" kilómetros")
        print("A continuación, se muestran los recorridos posibles en el MST, con sus respectivas distancias")
        printMST(lista)
    elif int(inputs[0]) == 7:
        airport = input("Por favor escriba el código IATA del aeropuerto que está fuera de funcionamiento: ")
        datos = controller.ChaoAirport(cont, airport)
        print("Al eliminar el aeropuerto "+airport+", se ven afectados un total de "+str(datos[1])+" aeropuertos.")
        print3airports(datos[0])
    else:
        sys.exit(0)
sys.exit(0)


if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()
