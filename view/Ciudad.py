import pygame
import networkx as nx
from src.Botin import Puente
from src.Render_thread import RenderThread

class Ciudad:
    def __init__(self):
        self.background = None
        self.vehiculos = {}
        self.imagenes_vehiculos = {}
        self.imagenes_personajes = {}
        self.ciudad = nx.DiGraph()
        self.pygame_running = False
        self.render_thread = None
        self.posiciones_nodos = {}
        self.caminos_detallados = {}

    def iniciar_pygame(self):
        if not self.pygame_running:
            pygame.init()
            self.crear_grafo()
            self.pygame_running = True
            
            self.render_thread = RenderThread(self)
            self.render_thread.start()

    def crear_grafo(self):
        capacidad_camioneta = 500
        capacidad_blindado = 2500
        
        # Definir los puentes (esto puede estar definido en otro lugar, asegúrate de tener acceso)
        puentes = {
            'A': Puente(id='A', peso_maximo=2500),
            'B': Puente(id='B', peso_maximo=2500),
            'C': Puente(id='C', peso_maximo=500),
            'D': Puente(id='D', peso_maximo=2500),
            'E': Puente(id='E', peso_maximo=2500),
            'F': Puente(id='F', peso_maximo=2500),
            'G': Puente(id='G', peso_maximo=2500),
            'H': Puente(id='H', peso_maximo=500),
            'I': Puente(id='I', peso_maximo=2500),
            'J': Puente(id='J', peso_maximo=2500),
            'K': Puente(id='K', peso_maximo=2500),
            'L': Puente(id='L', peso_maximo=2500)
        }

        self.posiciones_nodos = {
            'A': (139, 374), 'B': (663, 374), 'C': (965, 372),
            'D': (52, 509),  'E': (330, 510), 'F': (663, 474),
            'G': (965, 512), 'H': (247, 619), 'I': (478, 724),
            'J': (653, 670), 'K': (965, 740), 'L': (663, 824)
        }

        self.caminos_detallados = {
            ('A', 'D'): [(139, 374), (142, 509), (36, 512), (52, 509)],
            ('A', 'E'): [(139, 374), (265, 378), (271, 508), (330, 510)],
            ('A', 'B'): [(139, 374), (663, 374)],
            ('D', 'H'): [(52, 509),(34, 510), (34, 622), (247, 619)],
            ('E', 'I'): [(330, 510), (365, 510), (368, 712), (478, 724)],
            ('E', 'F'): [(330, 510), (365, 474), (663, 474)],
            ('F', 'E'): [(663, 474), (364, 474), (365, 510), (330, 510)],
            ('F', 'G'): [(663, 474), (965, 512)],
            ('F', 'J'): [(663, 474), (671, 665)],
            ('G', 'K'): [(965, 512), (965, 740)],
            ('B', 'C'): [(663, 374), (965, 372)],
            ('B', 'F'): [(663, 374), (663, 474)],
            ('C', 'G'): [(965, 372), (965, 512)],
            ('H', 'I'): [(247, 619), (249, 711),(368, 712),(478, 724)],
            ('I', 'L'): [(478, 724), (479, 824), (663, 824), (663, 824)],
            ('I', 'J'): [(478, 724),(540, 721),(540, 673),(653, 670)],
            ('J', 'I'): [(653, 670),(540, 673), (540, 721), (478, 724)],
            ('J', 'K'): [(653, 670), (963, 674),(965, 740)],
            ('L', 'K'): [(663, 824), (663, 852), (712, 856), (715, 902), (956, 902), (965, 740)],
        }

        for nodo, (x, y) in self.posiciones_nodos.items():
            puente = puentes.get(nodo, None)  # Obtener el puente correspondiente al nodo
            self.ciudad.add_node(nodo, pos=(x, y), puente=puente)
            
        for (nodo1, nodo2), camino in self.caminos_detallados.items():
            if nodo1 in self.ciudad.nodes and nodo2 in self.ciudad.nodes:
                peso_max = min(puentes[nodo1].peso_maximo, puentes[nodo2].peso_maximo)
                peso_arista = max(1, peso_max // capacidad_camioneta)  # Aquí debes usar la capacidad del vehículo adecuado
                puente = puentes.get(nodo1)  # Suponiendo que usas el puente del nodo inicial
                self.ciudad.add_edge(nodo1, nodo2, weight=peso_arista, puente=puente)
            else:
                print(f"Error: Nodo {nodo1} o Nodo {nodo2} no está presente en el grafo.")
    
    def procesar_solicitudes(self, nombre, dinero_a_enviar, destino, tiempo_estimado):
        print(f"Vehículo seleccionado para enviar {dinero_a_enviar} dinero: {destino}, Tipo: {destino.tipo}, Velocidad: {destino.velocidad}, Capacidad: {destino.capacidad}")

        print(f"Planificando ruta para el cliente {nombre} con {dinero_a_enviar} dinero")
        mejor_ruta, mensaje = self.planificar_ruta(nombre, dinero_a_enviar, destino, tiempo_estimado)
        print("planificar_ruta completado.")

        if mejor_ruta:
            vehiculo = mejor_ruta[0]
            costo = mejor_ruta[1][0]
            nodos_ruta = mejor_ruta[1][1]
            camino_detallado = []

            # Verificar y agregar el vehículo a la ciudad si no está registrado
            self.ciudad.verificar_y_agregar_vehiculo(vehiculo)

            # Obtener la imagen del vehículo si no está cargada
            self.ciudad.cargar_imagen_vehiculo(vehiculo)

            # Asignar posición inicial del vehículo
            vehiculo.x, vehiculo.y = self.posiciones_nodos[nodos_ruta[0]]

            # Construir el camino detallado a partir de la lista de nodos
            for i in range(len(nodos_ruta) - 1):
                nodo_actual = nodos_ruta[i]
                nodo_siguiente = nodos_ruta[i + 1]
                if (nodo_actual, nodo_siguiente) in self.caminos_detallados:
                    camino_detallado.extend(self.caminos_detallados[(nodo_actual, nodo_siguiente)])
                else:
                    print(f"Advertencia: No se encontró camino detallado entre {nodo_actual} y {nodo_siguiente}")

            print(f"Vehículo seleccionado: {vehiculo.id}")
            print(f"Mejor ruta: {nodos_ruta}")
            print(f"Camino detallado (coordenadas): {camino_detallado}")
            print(f"Costo de la ruta: {costo}")
            print(mensaje)

            # Actualizar la pantalla después de procesar la solicitud
            self.actualizar_pantalla()

        else:
            print(mensaje)

    def dibujar(self, screen, nodos_ruta):
        # Dibujar la ciudad y los nodos
        screen.blit(self.background, (0, 0))

        for nodo, (x, y) in self.posiciones_nodos.items():
            pygame.draw.circle(screen, (255, 0, 0), (x, y), 10)


        # Actualizar la pantalla después de dibujar todos los vehículos en la ruta
        pygame.display.flip()

    def stop_pygame(self):
        if self.render_thread:
            self.render_thread.stop()
            self.pygame_running = False