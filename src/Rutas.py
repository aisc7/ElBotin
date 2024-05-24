# src/Rutas.py
from src.Botin import CentroDeOperacion, Cliente, Vehiculo, Escolta, Contenedor, Puente, BandaLadrones
from collections import deque

class Rutas:
    
    @staticmethod
    def planificar_ruta(ciudad, origen, destino, cantidad_dinero, capacidad_puente_maxima):
        # Definir vehículos disponibles
        camioneta = Vehiculo(id='Camioneta', tipo='pequeno', capacidad=500, escudo=5, ataque=10, escoltas_necesarias=1)
        blindado = Vehiculo(id='Blindado', tipo='grande', capacidad=2000, escudo=20, ataque=15, escoltas_necesarias=2)
        
        # Seleccionar el vehículo adecuado
        if cantidad_dinero <= 500:
            vehiculo_seleccionado = camioneta
        else:
            vehiculo_seleccionado = blindado

        # Inicializar variables para BFS
        visitados = set()
        padre = {}
        distancias = {nodo: float('inf') for nodo in ciudad.ciudad.nodes}
        distancias[origen] = 0

        # Cola para BFS
        cola = deque([origen])

        # Búsqueda en anchura (BFS) modificada
        while cola:
            nodo_actual = cola.popleft()
            visitados.add(nodo_actual)

            # Si se llega al destino, reconstruir el camino
            if nodo_actual == destino:
                camino = []
                while nodo_actual in padre:
                    camino.append(nodo_actual)
                    nodo_actual = padre[nodo_actual]
                camino.append(origen)
                camino.reverse()

                # Calcular costo total de la ruta
                costo_ruta, costo_peajes = Rutas.calcular_costo(ciudad, camino, vehiculo_seleccionado, capacidad_puente_maxima)

                return costo_ruta, camino, vehiculo_seleccionado

            # Explorar vecinos
            for vecino in ciudad.ciudad.neighbors(nodo_actual):
                peso = ciudad.ciudad[nodo_actual][vecino]['peso']
                if peso <= capacidad_puente_maxima and vecino not in visitados:
                    if distancias[vecino] > distancias[nodo_actual] + peso:
                        distancias[vecino] = distancias[nodo_actual] + peso
                        padre[vecino] = nodo_actual
                        cola.append(vecino)

        # Si no se encuentra camino, devolver un valor indicando esto
        return float('inf'), [], None

    @staticmethod
    def calcular_costo(ciudad, camino, vehiculo, capacidad_puente_maxima):
        costo_ruta = 0
        costo_peajes = 0

        for i in range(len(camino) - 1):
            origen = camino[i]
            destino = camino[i + 1]
            peso = ciudad.ciudad[origen][destino]['peso']
            costo_ruta += peso  # Suponiendo que el peso también representa el costo de la ruta
            if peso > capacidad_puente_maxima:
                costo_peajes += peso  # Agregar el costo del peaje si el peso excede la capacidad del puente

        return costo_ruta, costo_peajes
