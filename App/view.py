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
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
airports = "airports_full.csv"
routes = "routes_full.csv"
cities = "worldcities.csv"

def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de los vuelos del mundo")
    print("3- Encontrar puntos de interconexión aérea")
    print("4- Encontrar clústeres de tráfico aéreo y saber si dos aeropuertos pertenecen a esta")
    print("5- Encontrar la ruta más corta entre dos ciudades")
    print("6- Utilizar millas de viajero para conocer la mayor cantidad de ciudades")
    print("7- Cuantificar el efecto de un aeropuerto cerrado")
    print("0- Salir")
    print("*******************************************")

catalog = None

def option2(cont):
    print("Cargarndo la información de vuelos, rutas, aeropuertos y ciuades")
    controller.loadTodo(cont, airports, routes, cities)

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
        pass
    elif int(inputs[0]) == 4:
        airport1 = input("Por favor escriba el nombre del código IATA del aeropuerto 1")
        airport2 = input("Por favor escriba el nombre del código IATA del aeropuerto 2")
    elif int(inputs[0]) == 5:
        ciudad1 = input("Por favor escriba el nombre de la ciudad de origen")
        ciudad2 = input("Por favor escriba el nombre de la ciudad de destino")
    elif int(inputs[0]) == 6:
        ciudad = input("Por favor escriba su ciudad de origen")
        millas = input("Por favor escriba su cantidad de millas de viajero")
    elif int(inputs[0]) == 7:
        airport = input("Por favor escriba el código IATA del aeropuerto que está fuera de funcionamiento")

    else:
        sys.exit(0)
sys.exit(0)


if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()
