# src/Rutas.py
import heapq
import csv
from collections import deque
import networkx as nx

from src.Botin import Vehiculo, Puente


class Rutas:

    def planificar_ruta_bfs(self, ciudad, origen, destino, vehiculo_seleccionado, tiempo_estimado):
        visitados = set()
        padre = {}
        distancias = {nodo: float('inf') for nodo in ciudad.ciudad.nodes}
        distancias[origen] = 0
        cola = deque([origen])

        while cola:
            nodo_actual = cola.popleft()
            visitados.add(nodo_actual)

            if nodo_actual == destino:
                camino = self.construir_camino(padre, origen, destino)
                costo_ruta = self.calcular_costo(ciudad, camino)
                if costo_ruta <= tiempo_estimado:
                    return costo_ruta, camino
                else:
                    return float('inf'), []

            for vecino in ciudad.ciudad.neighbors(nodo_actual):
                peso_max = ciudad.ciudad[nodo_actual][vecino]['peso_max']
                if peso_max >= vehiculo_seleccionado.capacidad and vecino not in visitados:
                    if distancias[vecino] > distancias[nodo_actual] + 1:
                        distancias[vecino] = distancias[nodo_actual] + 1
                        padre[vecino] = nodo_actual
                        cola.append(vecino)

        return float('inf'), []

    def planificar_ruta_dfs(self, ciudad, origen, destino, vehiculo_seleccionado, tiempo_estimado):
        visitados = set()
        padre = {}
        stack = [origen]

        while stack:
            nodo_actual = stack.pop()

            if nodo_actual == destino:
                camino = self.construir_camino(padre, origen, destino)
                costo_ruta = self.calcular_costo(ciudad, camino)
                if costo_ruta <= tiempo_estimado:
                    return costo_ruta, camino
                else:
                    return float('inf'), []

            if nodo_actual not in visitados:
                visitados.add(nodo_actual)
                for vecino in ciudad.ciudad.neighbors(nodo_actual):
                    peso_max = ciudad.ciudad[nodo_actual][vecino]['peso_max']
                    if peso_max >= vehiculo_seleccionado.capacidad and vecino not in visitados:
                        padre[vecino] = nodo_actual
                        stack.append(vecino)

        return float('inf'), []

    def planificar_ruta_dijkstra(self, ciudad, origen, destino, vehiculo_seleccionado, tiempo_estimado):
        distancias = {nodo: float('inf') for nodo in ciudad.ciudad.nodes}
        distancias[origen] = 0
        padre = {}
        pq = [(0, origen)]

        while pq:
            distancia_actual, nodo_actual = heapq.heappop(pq)

            if nodo_actual == destino:
                camino = self.construir_camino(padre, origen, destino)
                if distancia_actual <= tiempo_estimado:
                    return distancia_actual, camino
                else:
                    return float('inf'), []

            if distancia_actual > distancias[nodo_actual]:
                continue

            for vecino in ciudad.ciudad.neighbors(nodo_actual):
                peso_max = ciudad.ciudad[nodo_actual][vecino]['peso_max']
                if peso_max >= vehiculo_seleccionado.capacidad:
                    nueva_distancia = distancia_actual + 1
                    if nueva_distancia < distancias[vecino]:
                        distancias[vecino] = nueva_distancia
                        padre[vecino] = nodo_actual
                        heapq.heappush(pq, (nueva_distancia, vecino))

        return float('inf'), []

    def planificar_ruta_bellman_ford(self, ciudad, origen, destino, vehiculo_seleccionado, tiempo_estimado):
        distancias = {nodo: float('inf') for nodo in ciudad.ciudad.nodes}
        distancias[origen] = 0
        padre = {}

        for _ in range(len(ciudad.ciudad.nodes) - 1):
            for nodo in ciudad.ciudad.nodes:
                for vecino in ciudad.ciudad.neighbors(nodo):
                    peso_max = ciudad.ciudad[nodo][vecino]['peso_max']
                    if peso_max >= vehiculo_seleccionado.capacidad:
                        if distancias[nodo] + 1 < distancias[vecino]:
                            distancias[vecino] = distancias[nodo] + 1
                            padre[vecino] = nodo

        if distancias[destino] == float('inf'):
            return float('inf'), []

        camino = self.construir_camino(padre, origen, destino)
        if distancias[destino] <= tiempo_estimado:
            return distancias[destino], camino
        else:
            return float('inf'), []

    def planificar_ruta(self, ciudad, origen, destino, cantidad_dinero, capacidad_puente_maxima, tiempo_estimado):
        vehiculo_seleccionado = self.seleccionar_vehiculo(cantidad_dinero)

        rutas = {
            'BFS': self.planificar_ruta_bfs(ciudad, origen, destino, vehiculo_seleccionado, tiempo_estimado),
            'DFS': self.planificar_ruta_dfs(ciudad, origen, destino, vehiculo_seleccionado, tiempo_estimado),
            'Dijkstra': self.planificar_ruta_dijkstra(ciudad, origen, destino, vehiculo_seleccionado, tiempo_estimado),
            'Bellman-Ford': self.planificar_ruta_bellman_ford(ciudad, origen, destino, vehiculo_seleccionado, tiempo_estimado)
        }

        mejor_ruta = min(rutas.items(), key=lambda x: x[1][0])

        if mejor_ruta[1][0] == float('inf'):
            return None, "No se puede llegar al destino en el tiempo estimado con ninguna ruta."

        return mejor_ruta

    def seleccionar_vehiculo(self, cantidad_dinero):
        if cantidad_dinero <= 500:
            return Vehiculo(id='Camioneta', tipo='camioneta', velocidad=3, capacidad=500, escudo=5, ataque=10, escoltas_necesarias=1)
        else:
            return Vehiculo(id='Blindado', tipo='blindado', velocidad=1, capacidad=2000, escudo=20, ataque=15, escoltas_necesarias=2)

    def calcular_costo(self, ciudad, camino):
        return len(camino) - 1

    def construir_camino(self, padre, origen, destino):
        camino = []
        nodo_actual = destino
        while nodo_actual in padre:
            camino.append(nodo_actual)
            nodo_actual = padre[nodo_actual]
        camino.append(origen)
        camino.reverse()
        return camino

    def procesar_solicitudes(self, archivo_entrada, archivo_salida, ciudad, opcion_ruta=None):
        with open(archivo_entrada, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            resultados = []
            for row in reader:
                nombre_cliente = row['nombre_cliente']
                origen = row['origen']
                destino = row['destino']
                cantidad_dinero = int(row['cantidad_dinero'])
                capacidad_puente_maxima = int(row['capacidad_puente_maxima'])
                tiempo_estimado = int(row['tiempo_estimado'])

                resultado = self.planificar_ruta(ciudad, origen, destino, cantidad_dinero, capacidad_puente_maxima, tiempo_estimado)

                if resultado[0] is None:
                    resultados.append({
                        'nombre_cliente': nombre_cliente,
                        'origen': origen,
                        'destino': destino,
                        'cantidad_dinero': cantidad_dinero,
                        'vehiculo': 'N/A',
                        'ruta': 'No es posible llegar en el tiempo estimado',
                        'costo': 'N/A'
                    })
                else:
                    nombre_algoritmo, (costo, ruta) = resultado
                    resultados.append({
                        'nombre_cliente': nombre_cliente,
                        'origen': origen,
                        'destino': destino,
                        'cantidad_dinero': cantidad_dinero,
                        'vehiculo': self.seleccionar_vehiculo(cantidad_dinero).id,
                        'ruta': ' -> '.join(ruta),
                        'costo': costo
                    })

        with open(archivo_salida, 'w', newline='') as csvfile:
            fieldnames = ['nombre_cliente', 'origen', 'destino', 'cantidad_dinero', 'vehiculo', 'ruta', 'costo']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for resultado in resultados:
                writer.writerow(resultado)