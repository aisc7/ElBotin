#src/Botin.py
import networkx as nx
from heapq import heappop, heappush

# Definición de Clases

class CentroDeOperacion:
    def __init__(self, id, capacidad_dinero, capacidad_vehiculos, capacidad_escoltas):
        self.id = id
        self.capacidad_dinero = capacidad_dinero
        self.capacidad_vehiculos = capacidad_vehiculos
        self.capacidad_escoltas = capacidad_escoltas
        self.dinero = 0
        self.vehiculos = []
        self.escoltas = []

    def agregar_vehiculo(self, vehiculo):
        if len(self.vehiculos) < self.capacidad_vehiculos:
            self.vehiculos.append(vehiculo)

    def agregar_escolta(self, escolta):
        if len(self.escoltas) < self.capacidad_escoltas:
            self.escoltas.append(escolta)

    def almacenar_dinero(self, cantidad):
        if self.dinero + cantidad <= self.capacidad_dinero:
            self.dinero += cantidad
        else:
            raise ValueError("Capacidad de dinero excedida en el centro de operación")

class Cliente:
    def __init__(self, id, demanda_dinero, tiempo_entrega, capacidad_contenedores):
        self.id = id
        self.demanda_dinero = demanda_dinero
        self.tiempo_entrega = tiempo_entrega
        self.capacidad_contenedores = capacidad_contenedores

class Vehiculo:
    def __init__(self, id, tipo, capacidad, escudo, ataque, escoltas_necesarias):
        self.id = id
        self.tipo = tipo
        self.capacidad = capacidad
        self.escudo = escudo
        self.ataque = ataque
        self.escoltas_necesarias = escoltas_necesarias

class Escolta:
    def __init__(self, id, escudo, ataque):
        self.id = id
        self.escudo = escudo
        self.ataque = ataque

class Contenedor:
    def __init__(self, id, capacidad_peso):
        self.id = id
        self.capacidad_peso = capacidad_peso

class Puente:
     def __init__(self, id, peso_maximo):
        self.id = id
        self.tipo = 'puente' 
        self.peso_maximo = peso_maximo  # Peso máximo permitido en el puente

class BandaLadrones:
    def __init__(self, id, vehiculos):
        self.id = id
        self.vehiculos = vehiculos

