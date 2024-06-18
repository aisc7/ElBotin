#src/Rutas.py
import heapq
from collections import deque
from src.Botin import Vehiculo, Ladrones
from view.Ciudad import Ciudad

class Rutas:
    def __init__(self):
        self.vehiculos = {} 
        self.ciudad = Ciudad()
        self.ciudad.iniciar_pygame(self.vehiculos)
         

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
        
        # Verificar si el destino es una lista y unirla en una cadena si es necesario
        if isinstance(destino, list):
            destino = ','.join(destino)

        # Obtener la lista de paradas
        destinos = destino.replace(" ", "").split(",")

        rutas = {
            'BFS': self.planificar_ruta_con_paradas(self.planificar_ruta_bfs, destinos, vehiculo_seleccionado, tiempo_estimado),
            'DFS': self.planificar_ruta_con_paradas(self.planificar_ruta_dfs, destinos, vehiculo_seleccionado, tiempo_estimado),
            'Dijkstra': self.planificar_ruta_con_paradas(self.planificar_ruta_dijkstra, destinos, vehiculo_seleccionado, tiempo_estimado),
            'Bellman-Ford': self.planificar_ruta_con_paradas(self.planificar_ruta_bellman_ford, destinos, vehiculo_seleccionado, tiempo_estimado)
        }

        # Encontrar la mejor ruta basada en el tiempo estimado
        mejor_ruta = min(rutas.items(), key=lambda x: x[1][0])

        if mejor_ruta[1][0] != float('inf'):
            costo_ruta, camino_ruta = mejor_ruta[1]
            if costo_ruta <= tiempo_estimado:
               
                ruta_detallada = self.construir_ruta_detallada(camino_ruta)
                vehiculo_seleccionado.ruta_detallada = ruta_detallada
                self.vehiculos[vehiculo_seleccionado.id] = vehiculo_seleccionado

                return mejor_ruta, f"La mejor ruta es para el destino {destinos[-1]}"
            else:
                return None, f"No se puede llegar al destino {destinos[-1]} en el tiempo estimado de {tiempo_estimado} minutos. El costo de la mejor ruta es {costo_ruta} minutos."
        else:
            return None, "No se puede llegar al destino en el tiempo estimado con ninguna ruta."
    
    def planificar_ruta_con_paradas(self, metodo_planificacion, destinos, vehiculo_seleccionado, tiempo_estimado):
        origen = destinos[0]
        paradas = destinos[1:-1]
        destino_final = destinos[-1]

        tiempo_total = 0
        camino_completo = []

        nodo_actual = origen
        for parada in paradas + [destino_final]:
            costo, camino = metodo_planificacion(nodo_actual, parada, vehiculo_seleccionado, tiempo_estimado)
            if costo == float('inf'):
                return float('inf'), []

            tiempo_total += costo
            if camino_completo:
                camino_completo.extend(camino[1:])
            else:
                camino_completo.extend(camino)

            nodo_actual = parada

        if tiempo_total <= tiempo_estimado:
            return tiempo_total, camino_completo
        else:
            return float('inf'), []
            
    def construir_ruta_detallada(self, camino_ruta):
        ruta_detallada = []
        for i in range(len(camino_ruta) - 1):
            nodo_origen = camino_ruta[i]
            nodo_destino = camino_ruta[i + 1]
            par_de_nodos = (nodo_origen, nodo_destino)
            if par_de_nodos in self.ciudad.caminos_detallados:
                ruta_detallada.extend(self.ciudad.caminos_detallados[par_de_nodos])
            else:
                print(f"No se encontró una ruta detallada para el camino: {par_de_nodos}")
        print(f"Ruta detallada construida: {ruta_detallada}")
        return ruta_detallada

            
    def asignar_vehiculo(self, dinero_a_enviar):
        if isinstance(dinero_a_enviar, int):
            if dinero_a_enviar <= 500:
                vehiculo = Vehiculo(id='camioneta', tipo='camioneta', velocidad=850, capacidad=500, escudo=5, ataque=10, escoltas_necesarias=1)
            else:
                vehiculo = Vehiculo(id='blindado', tipo='blindado', velocidad=500, capacidad=2500, escudo=20, ataque=15, escoltas_necesarias=2)
            
            self.vehiculos[vehiculo.id] = vehiculo  # Almacenar el vehículo en el diccionario
            print(f"Vehículo asignado y almacenado: {vehiculo.id}")
            return vehiculo
        return None

        
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
        actual = destino
        
        while actual != origen:
            actual = padre[actual]
            camino.append(actual)
        
        camino.reverse()
        return camino

        
    def ladrones(self, cliente, vehiculo_asignado, mejor_ruta_cliente, dinero_a_enviar, tiempo_estimado, ataque_ladrones, escudo_ladrones):
        # Verificar que el vehículo asignado sea un blindado
        if vehiculo_asignado.tipo != "blindado":
            return False, "El vehículo no es un blindado. No hay ataque posible."

        # Obtener el destino del cliente
        destino_cliente = cliente if isinstance(cliente, str) else cliente.destino

        # Obtener la ruta del cliente
        distancia_cliente, ruta_cliente = mejor_ruta_cliente[1]
        print(f"Camino de la mejor ruta para el cliente {destino_cliente}: ({distancia_cliente}, {ruta_cliente})")

        # Buscar un punto de interceptación en la ruta del cliente
        punto_intercepcion = ruta_cliente[len(ruta_cliente) // 2]

        # Planificar la ruta de los ladrones al punto de interceptación
        origen_ladrones = "Inicio de los ladrones"
        vehiculo_ladrones = Vehiculo(id='camioneta', tipo='camioneta', velocidad=3, capacidad=500, escudo=5, ataque=10, escoltas_necesarias=1)
        mejor_ruta_ladrones, mensaje_ladrones = self.planificar_ruta(origen_ladrones, punto_intercepcion, 2400, tiempo_estimado)
        if not mejor_ruta_ladrones:
            return False, "No se encontró una ruta válida para los ladrones. " + mensaje_ladrones

        distancia_ladrones, ruta_ladrones = mejor_ruta_ladrones[1]
        print(f"Camino de los ladrones hacia el punto de interceptación: ({distancia_ladrones}, {ruta_ladrones})")

        # Calcular el poder de ataque y escudo del vehículo asignado
        poder_ataque_total = vehiculo_asignado.ataque + (5 * vehiculo_asignado.escoltas_necesarias)
        poder_escudo_total = vehiculo_asignado.escudo + (5 * vehiculo_asignado.escoltas_necesarias)

        if ataque_ladrones > poder_escudo_total:
            return True, f"La banda de ladrones ha tenido éxito en atacar a {destino_cliente} con un ataque de {ataque_ladrones} y un escudo de {escudo_ladrones}. El poder de escudo del vehículo asignado era {poder_escudo_total}."
        else:
            return False, f"La banda de ladrones no pudo atacar a {destino_cliente}. El poder de escudo del vehículo asignado era {poder_escudo_total}, que es suficiente para defenderse del ataque de {ataque_ladrones}."
    def obtener_informacion_banda(self, ataque, escudo):
        return f"Ataque de la banda: {ataque}, Escudo de la banda: {escudo}"