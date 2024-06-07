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
            self.cargar_imagenes()
            self.crear_grafo()
            self.pygame_running = True
            
            self.render_thread = RenderThread(self)
            self.render_thread.start()

    def cargar_imagenes(self):
        self.background = pygame.image.load('./data/image/ciudad.jpeg')

        rutas_vehiculos = {
            "blindado": "./data/image/Blindado.png",
            "camioneta": "./data/image/Camioneta.png",
        }
        for nombre_vehiculo, ruta in rutas_vehiculos.items():
            try:
                self.imagenes_vehiculos[nombre_vehiculo] = pygame.image.load(ruta)
                print(f"Imagen del vehículo {nombre_vehiculo} cargada correctamente.")
            except pygame.error as e:
                print(f"No se pudo cargar la imagen del vehículo {nombre_vehiculo}: {e}")
                self.imagenes_vehiculos[nombre_vehiculo] = None

        rutas_personajes = {
            "escolta": "./data/image/Moto.png",
            "banda": "./data/image/Banda.png",
            "banda2": "./data/image/Banda2.png",
            "banda3": "./data/image/Banda3.png",
            "ladron": "./data/image/Ladron.png",
            "ladron2": "./data/image/Ladron2.png",
            "ladron3": "./data/image/Ladron3.png",
        }
        for nombre_personaje, ruta in rutas_personajes.items():
            try:
                self.imagenes_personajes[nombre_personaje] = pygame.image.load(ruta)
                print(f"Imagen del personaje {nombre_personaje} cargada correctamente.")
            except pygame.error as e:
                print(f"No se pudo cargar la imagen del personaje {nombre_personaje}: {e}")
                self.imagenes_personajes[nombre_personaje] = None

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
            ('D', 'H'): [(52, 509), (34, 622), (247, 619)],
            ('E', 'I'): [(330, 510), (365, 510), (366, 708), (475, 708)],
            ('E', 'F'): [(330, 510), (365, 474), (663, 474)],
            ('F', 'E'): [(663, 474), (364, 474), (365, 510), (330, 510)],
            ('F', 'G'): [(663, 474), (965, 512)],
            ('F', 'J'): [(663, 474), (671, 665)],
            ('G', 'K'): [(965, 512), (965, 740)],
            ('B', 'C'): [(663, 374), (965, 372)],
            ('B', 'F'): [(663, 374), (663, 474)],
            ('C', 'G'): [(965, 372), (965, 512)],
            ('H', 'I'): [(247, 619), (249, 711), (478, 724)],
            ('I', 'L'): [(478, 724), (479, 824), (663, 824), (663, 824)],
            ('I', 'J'): [(478, 724), (791, 670), (653, 670)],
            ('J', 'I'): [(653, 670), (791, 670), (478, 724)],
            ('L', 'K'): [(663, 824), (663, 852), (712, 856), (715, 902), (956, 902), (965, 740)],
        }

        for nodo, (x, y) in self.posiciones_nodos.items():
            puente = puentes.get(nodo, None)  # Obtener el puente correspondiente al nodo
            self.ciudad.add_node(nodo, pos=(x, y), puente=puente)
            print(f"Nodo agregado: {nodo} con posición {(x, y)} y puente {puente}")

        for (nodo1, nodo2), camino in self.caminos_detallados.items():
            if nodo1 in self.ciudad.nodes and nodo2 in self.ciudad.nodes:
                peso_max = min(puentes[nodo1].peso_maximo, puentes[nodo2].peso_maximo)
                peso_arista = max(1, peso_max // capacidad_camioneta)  # Aquí debes usar la capacidad del vehículo adecuado
                puente = puentes.get(nodo1)  # Suponiendo que usas el puente del nodo inicial
                self.ciudad.add_edge(nodo1, nodo2, weight=peso_arista, puente=puente)
                print(f"Arista agregada entre {nodo1} y {nodo2} con peso {peso_arista} y puente {puente}")
            else:
                print(f"Error: Nodo {nodo1} o Nodo {nodo2} no está presente en el grafo.")

    def procesar_solicitudes(self, nombre,dinero_a_enviar,destino,tiempo_estimado):
        # Llamar a planificar_ruta para obtener los resultados
        mejor_ruta, mensaje = self.planificar_ruta(self, nombre,dinero_a_enviar,destino,tiempo_estimado)
        
        if mejor_ruta:
            vehiculo = mejor_ruta[0]
            costo = mejor_ruta[1][0]
            print(f"Vehículo seleccionado: {vehiculo.id}")
            print(f"Mejor ruta: {mejor_ruta[1][1]}")
            print(f"Costo de la ruta: {costo}")
            print(mensaje)
        else:
            print(mensaje)

    def dibujar(self, screen):
        screen.blit(self.background, (0, 0))

        for nodo, (x, y) in self.posiciones_nodos.items():
            pygame.draw.circle(screen, (255, 0, 0), (x, y), 10)

        if self.vehiculos:
            for vehiculo in self.vehiculos.values():
                x, y = vehiculo.posicion
                screen.blit(self.imagenes_vehiculos[vehiculo.tipo], (x, y))

    def stop_pygame(self):
        if self.render_thread:
            self.render_thread.stop()
            self.pygame_running = False
