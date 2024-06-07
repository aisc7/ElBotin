import heapq
from collections import deque
from src.Botin import Vehiculo
from view.Ciudad import Ciudad

class Rutas:
    def __init__(self):
        self.ciudad = Ciudad()
        self.ciudad.iniciar_pygame()  # Asegúrate de que `iniciar_pygame` se llama para cargar imágenes y crear el grafo
   
    def planificar_ruta_bfs(self, origen, destino, vehiculo_seleccionado, tiempo_estimado):
        visitados = set()
        padre = {}
        distancias = {nodo: float('inf') for nodo in self.ciudad.ciudad.nodes}
        distancias[origen] = 0
        cola = deque([origen])

        while cola:
            nodo_actual = cola.popleft()
            visitados.add(nodo_actual)

            if nodo_actual == destino:
                camino = self.construir_camino(padre, origen, destino)
                costo_ruta = self.calcular_costo(camino)
                if costo_ruta <= tiempo_estimado:
                    return costo_ruta, camino
                else:
                    return float('inf'), []

            for vecino in self.ciudad.ciudad.neighbors(nodo_actual):
                if self.puente_dispo(nodo_actual, vecino, vehiculo_seleccionado) and vecino not in visitados:
                    if distancias[vecino] > distancias[nodo_actual] + 1:
                        distancias[vecino] = distancias[nodo_actual] + 1
                        padre[vecino] = nodo_actual
                        cola.append(vecino)

        return float('inf'), []

    def planificar_ruta_dfs(self, origen, destino, vehiculo_seleccionado, tiempo_estimado):
        visitados = set()
        padre = {}
        stack = [origen]

        while stack:
            nodo_actual = stack.pop()

            if nodo_actual == destino:
                camino = self.construir_camino(padre, origen, destino)
                costo_ruta = self.calcular_costo(camino)
                if costo_ruta <= tiempo_estimado:
                    return costo_ruta, camino
                else:
                    return float('inf'), []

            if nodo_actual not in visitados:
                visitados.add(nodo_actual)
                for vecino in self.ciudad.ciudad.neighbors(nodo_actual):
                    if self.puente_dispo(nodo_actual, vecino, vehiculo_seleccionado) and vecino not in visitados:
                        padre[vecino] = nodo_actual
                        stack.append(vecino)

        return float('inf'), []

    def planificar_ruta_dijkstra(self, origen, destino, vehiculo_seleccionado, tiempo_estimado):
        distancias = {nodo: float('inf') for nodo in self.ciudad.ciudad.nodes}
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

            for vecino in self.ciudad.ciudad.neighbors(nodo_actual):
                if self.puente_dispo(nodo_actual, vecino, vehiculo_seleccionado):
                    nueva_distancia = distancia_actual + self.ciudad.ciudad[nodo_actual][vecino]['weight']
                    if nueva_distancia < distancias[vecino]:
                        distancias[vecino] = nueva_distancia
                        padre[vecino] = nodo_actual
                        heapq.heappush(pq, (nueva_distancia, vecino))

        return float('inf'), []

    def planificar_ruta_bellman_ford(self, origen, destino, vehiculo_seleccionado, tiempo_estimado):
        distancias = {nodo: float('inf') for nodo in self.ciudad.ciudad.nodes}
        distancias[origen] = 0
        padre = {}

        for _ in range(len(self.ciudad.ciudad.nodes) - 1):
            for nodo in self.ciudad.ciudad.nodes:
                for vecino in self.ciudad.ciudad.neighbors(nodo):
                    if self.puente_dispo(nodo, vecino, vehiculo_seleccionado):
                        if distancias[nodo] + self.ciudad.ciudad[nodo][vecino]['weight'] < distancias[vecino]:
                            distancias[vecino] = distancias[nodo] + self.ciudad.ciudad[nodo][vecino]['weight']
                            padre[vecino] = nodo

        if distancias[destino] == float('inf'):
            return float('inf'), []

        camino = self.construir_camino(padre, origen, destino)
        if distancias[destino] <= tiempo_estimado:
            return distancias[destino], camino
        else:
            return float('inf'), []

    def puente_dispo(self, nodo_actual, vecino, vehiculo_seleccionado):
        nodo_actual_data = self.ciudad.ciudad.nodes[nodo_actual]
        nodo_vecino_data = self.ciudad.ciudad.nodes[vecino]

        puente_actual = nodo_actual_data.get('puente', None)
        puente_vecino = nodo_vecino_data.get('puente', None)

        if puente_actual and puente_vecino:
            peso_max = min(puente_actual.peso_maximo, puente_vecino.peso_maximo)
            if peso_max >= vehiculo_seleccionado.capacidad:
                return True
        return False
    
    def planificar_ruta(self, nombre, destino, dinero_a_enviar, tiempo_estimado):
        vehiculo_seleccionado = self.asignar_vehiculo(dinero_a_enviar)
        print(f"Planificando ruta para el cliente {nombre} con {dinero_a_enviar} dinero")

        # Verificar si el destino es una lista y unirla en una cadena si es necesario
        if isinstance(destino, list):
            destino = ','.join(destino)

        # Obtener el origen y el destino
        destino_limpio = destino.replace(" ", "").split(",")
        origen = destino_limpio[0]
        destino_final = destino_limpio[1]

        rutas = {
            'BFS': self.planificar_ruta_bfs(origen.strip(), destino_final.strip(), vehiculo_seleccionado, tiempo_estimado),
            'DFS': self.planificar_ruta_dfs(origen.strip(), destino_final.strip(), vehiculo_seleccionado, tiempo_estimado),
            'Dijkstra': self.planificar_ruta_dijkstra(origen.strip(), destino_final.strip(), vehiculo_seleccionado, tiempo_estimado),
            'Bellman-Ford': self.planificar_ruta_bellman_ford(origen.strip(), destino_final.strip(), vehiculo_seleccionado, tiempo_estimado)
        }

        # Encontrar la mejor ruta basada en el tiempo estimado
        mejor_ruta = min(rutas.items(), key=lambda x: x[1][0])

        if mejor_ruta[1][0] != float('inf'):
            return mejor_ruta, f"La mejor ruta es para el destino {destino_final.strip()}"
        else:
            return None, "No se puede llegar al destino en el tiempo estimado con ninguna ruta."

    def asignar_vehiculo(self, dinero_a_enviar):
        if isinstance(dinero_a_enviar, int):
            if dinero_a_enviar <= 500:
                vehiculo = Vehiculo(id='Camioneta', tipo='camioneta', velocidad=3, capacidad=500, escudo=5, ataque=10, escoltas_necesarias=1)
            else:
                vehiculo = Vehiculo(id='Blindado', tipo='blindado', velocidad=1, capacidad=2000, escudo=20, ataque=15, escoltas_necesarias=2)
            
            # Imprimir los detalles del vehículo seleccionado
            print(f"Vehículo seleccionado para enviar {dinero_a_enviar} dinero: {vehiculo.id}, Tipo: {vehiculo.tipo}, Velocidad: {vehiculo.velocidad}, Capacidad: {vehiculo.capacidad}")

            return vehiculo

    def calcular_costo(self, camino):
        costo_total = 0
        for i in range(len(camino) - 1):
            nodo_actual = camino[i]
            nodo_siguiente = camino[i + 1]
            peso_arista = self.ciudad.ciudad[nodo_actual][nodo_siguiente]['weight']
            costo_total += peso_arista
        return costo_total
        
    def construir_camino(self, padre, origen, destino):
        camino = [destino]
        while camino[-1] != origen:
            camino.append(padre[camino[-1]])
        camino.reverse()
        return camino
