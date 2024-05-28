#/view/Ciudad.py
import pygame
import networkx as nx
from src.Botin import Puente
from PySide6.QtCore import Signal, QThread

class RenderThread(QThread):
    finished_signal = Signal()

    def __init__(self, ciudad, parent=None):
        super().__init__(parent)
        self.ciudad = ciudad
        self.running = False
        

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((1100, 1000))
        pygame.display.set_caption("SImulacion")

        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    print(f"Click en la posición ({x}, {y})")
                    
            # Dibujar el fondo de la ciudad en la ventana de Pygame
            screen.blit(self.ciudad.background, (0, 0))
            
            # Aquí puedes agregar más lógica de dibujo de objetos, personajes, etc.
            self.ciudad.dibujar(screen)
            
            pygame.display.flip()
            pygame.time.delay(10)

        pygame.quit()
        self.finished_signal.emit()

    def stop(self):
        self.running = False
        pygame.quit()
        self.wait()

class Ciudad:
    def __init__(self):
        self.background = None
        self.vehiculos = {}
        self.imagenes_vehiculos = {}
        self.imagenes_personajes = {}
        self.ciudad = nx.DiGraph()
        self.pygame_running = False
        

    def iniciar_pygame(self):
        pygame.init()
        self.cargar_imagenes()
        self.pygame_running = True

        # Iniciar el hilo de renderizado de Pygame
        self.render_thread = RenderThread(self)
        self.render_thread.start()

    def cargar_imagenes(self):
        # Cargar la imagen de fondo
        self.background = pygame.image.load('./data/image/ciudad.jpeg')

        # Cargar imágenes de vehículos
        rutas_vehiculos = {
            "blindado": "./data/image/Blindado.png",
            "camioneta": "./data/image/Camioneta.png",
        }
        for nombre_vehiculo, ruta in rutas_vehiculos.items():
            self.imagenes_vehiculos[nombre_vehiculo] = pygame.image.load(ruta)

        # Cargar imágenes de personajes
        rutas_personajes = {
            "escolta": "./data/image/Moto.png",
            "banda": "./data/image/Banda.png",
            "banda2": "./data/image/Banda2.png",
            "banda3": "./data/image/Banda3.png",
            "ladron": "./data/image/Ladron.png",
            "ladron2": "./data/image/Ladron2.png",
            "ladron3": "./data/image/Ladron3.png",
            # Agrega más personajes según sea necesario
        }
        for nombre_personaje, ruta in rutas_personajes.items():
            self.imagenes_personajes[nombre_personaje] = pygame.image.load(ruta)
 # Definir posiciones de nodos
        self.posiciones_nodos = {
            'A': (139, 374), 'B': (663, 374), 'C': (965, 372),
            'D': (52, 509),  'E': (330, 510), 'F': (663, 474),
            'G': (965, 512), 'H': (247, 619), 'I': (478, 724),
            'J': (653, 670), 'K': (965, 740), 'L': (663, 824)
        }

        # Definir caminos detallados entre nodos
        self.caminos_detallados = {
            ('A', 'D'): [(139, 374), (142, 509), (36, 512), (52, 509)],
            ('A', 'E'): [(139, 374), (265, 378), (271, 508), (330, 510)],
            ('A', 'B'): [(139, 374), (663, 374)],
            ('D', 'H'): [(52, 509), (34, 622), (247, 619)],
            ('E', 'I'): [(330, 510), (365, 510), (366, 708), (475, 708)],
            ('E', 'F'): [(330, 510), (365,474), (663, 474)],
            ('F', 'E'): [(663, 474), (364, 474), (365, 510), (330, 510)],
            ('F', 'G'): [(663, 474), (965, 512)],
            ('F', 'J'): [(663, 474), (671, 665)],
            ('G', 'K'): [(965, 512), (965, 740)],
            ('B', 'C'): [(663, 374), (965, 372)],
            ('B', 'F'): [(663, 374), (663, 474)],
            ('C', 'G'): [(965, 372), (965, 512)],
            ('H', 'I'): [(247, 619),(249,711),(478, 724)],
            ('I', 'L'): [(478, 724), (479,824), (663,824), (663, 824)],
            ('I', 'J'): [(478, 724), (791,670), (653, 670)],
            ('J', 'I'): [(653, 670), (791,670), (478, 724)],
            ('L', 'K'): [(663, 824), (663, 852), (712, 856), (715,902),(956,902),(965, 740)],
        }
        
    
    def crear_grafo(self):
        # Añadir nodos al grafo
        self.ciudad.add_nodes_from(self.posiciones_nodos.keys())

        # Añadir conexiones al grafo
        for (nodo1, nodo2), camino in self.caminos_detallados.items():
            self.ciudad.add_edge(nodo1, nodo2, weight=len(camino))

        # Crear instancias de la clase Puente para representar los puentes
        puentes = {
            'A': Puente(id='A', peso_maximo=500),
            'B': Puente(id='B', peso_maximo=2500),
            'C': Puente(id='C', peso_maximo=500),
            'D': Puente(id='D', peso_maximo=2500),
            'E': Puente(id='E', peso_maximo=2500),
            'F': Puente(id='F', peso_maximo=2500),
            'G': Puente(id='G', peso_maximo=2500),
            'H': Puente(id='H', peso_maximo=500),
            'I': Puente(id='I', peso_maximo=2500),
            'J': Puente(id='J', peso_maximo=2500),
            'L': Puente(id='L', peso_maximo=2500)
        }

        for (nodo1, nodo2) in self.ciudad.edges:
            puente = puentes.get(nodo1) or puentes.get(nodo2)
            if puente:
                self.ciudad[nodo1][nodo2]['puente'] = puente

    def dibujar(self, screen):
        # Dibujar líneas entre nodos
        for (nodo1, nodo2) in self.ciudad.edges:
            camino = self.caminos_detallados.get((nodo1, nodo2), [])
            if not camino:
                camino = self.caminos_detallados.get((nodo2, nodo1), [])
                camino = camino[::-1]

            if camino:
                pygame.draw.lines(screen, (0, 0, 0), False, camino, 5)

        # Dibujar los nodos
        for nodo, (x, y) in self.posiciones_nodos.items():
            pygame.draw.circle(screen, (255, 0, 0), (x, y), 10)

        # Dibujar los vehículos
        if self.vehiculos:  # Verifica si self.vehiculos no está vacío
          for vehiculo in self.vehiculos.values():
            x, y = vehiculo.posicion
            screen.blit(self.imagenes_vehiculos[vehiculo.tipo], (x, y))

    def mover_vehiculo(self, vehiculo, ruta):
        for i in range(len(ruta) - 1):
            nodo_actual = ruta[i]
            siguiente_nodo = ruta[i + 1]

            if (nodo_actual, siguiente_nodo) in self.caminos_detallados:
                camino = self.caminos_detallados[(nodo_actual, siguiente_nodo)]
            else:
                camino = self.caminos_detallados[(siguiente_nodo, nodo_actual)][::-1]

            for x, y in camino:
                if not self.pygame_running:
                    return
                vehiculo.actualizar_posicion((x, y))
                pygame.time.delay(50)

    def stop_pygame(self):
        self.render_thread.stop()
        self.pygame_running = False

