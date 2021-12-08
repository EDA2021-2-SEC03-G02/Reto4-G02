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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
def init():
    analyzer = model.newAnalyzer()
    return analyzer

def loadTodo(analyzer, airports, routes, cities):
    loadAirports(analyzer, airports)
    loadRoutes(analyzer, routes)
    loadCities(analyzer, cities)

def loadAirports(analyzer, airports):
    servicesfile = cf.data_dir + airports
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=",")
    for airport in input_file:
        model.addAirport(analyzer, airport)


def loadRoutes(analyzer, routes):
    servicesfile = cf.data_dir + routes
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=",")
    for route in input_file:
        model.addRoutesGraph(analyzer, route)

def loadCities(analyzer, cities):
    servicesfile = cf.data_dir + cities
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=",")
    for city in input_file:
        model.addCiudad(analyzer, city)

def totalRoutes(grafo):
    return model.totalRoutes(grafo)

def totalAirports(grafo):
    return model.totalAirports(grafo)

def FirstAirport(analyzer):
    return model.FirstAirport(analyzer)

def sizeLista(lista):
    return model.sizeLista(lista)
def infoUltimo(analyzer, ultimo):
    return model.infoUltimo(analyzer, ultimo)
def sizeMapa(analyzer):
    return model.sizeMapa(analyzer)

#Req 1
def Top5Conectados(analyzer):
    return model.Top5Conectados(analyzer)
def infoIata(iata, cont):
    return model.infoIata(iata, cont)


#Req3
def findCityName(analyzer, ciudad):
    return model.findCityName(analyzer, ciudad)

def getInfo(analyzer, id):
    return model.getInfo(analyzer, id)

def getAirportCity(cont, id):
    return model.getAirportCity(cont, id)

def infoAirport(analyzer, iata):
    return model.infoAirport(analyzer, iata)

def RutaMenorCosto(analyzer, inicio, final):
    return model.RutaMenorCosto(analyzer, inicio, final)

#Req 4
def RutaMasParadas(analyzer, km, ciudad):
    return model.RutaMasParadas(analyzer, km, ciudad)
    
#Req 5
def ChaoAirport(analyzer, iata):
    return model.ChaoAirport(analyzer, iata)