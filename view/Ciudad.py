#view/Ciudad.py
import os
import pygame
import networkx as nx
from src.Botin import Puente, Vehiculo
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

        # Diccionario con las rutas de las imágenes
        self.rutas_imagenes = {
            'ciudad': './data/image/ciudad.jpeg',
            'Banda': './data/image/Banda.png',
            'Camioneta': './data/image/Camioneta.png',
            'Blindado': './data/image/Blindado.png'
        }

        # Cargar las imágenes al iniciar la ciudad
        self.cargar_imagenes()

    def cargar_imagenes(self):
        for clave, ruta in self.rutas_imagenes.items():
            if os.path.exists(ruta):
                try:
                    print(f"Intentando cargar la imagen {ruta} para {clave}")
                    imagen = pygame.image.load(ruta)
                    self.imagenes_vehiculos[clave] = imagen
                    if clave == 'ciudad':
                        self.background = imagen
                    print(f"Imagen {ruta} cargada correctamente para {clave}")
                except pygame.error as e:
                    print(f"Error cargando la imagen {ruta}: {e}")
                except Exception as e:
                    print(f"Error inesperado cargando la imagen {ruta}: {e}")
            else:
                print(f"La ruta de la imagen {ruta} no existe.")

    def iniciar_pygame(self, vehiculos):
        self.crear_grafo()
        self.pygame_running = True
        self.vehiculos = vehiculos  # Asignar el diccionario vehiculos al atributo
        self.render_thread = RenderThread(self, vehiculos)  # Pasar vehiculos al hilo de renderizado
        self.render_thread.start()

    def crear_grafo(self):
        capacidad_camioneta = 500
        capacidad_blindado = 2500

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
            'D': (52, 509), 'E': (330, 510), 'F': (663, 474),
            'G': (965, 512), 'H': (247, 619), 'I': (478, 724),
            'J': (653, 670), 'K': (965, 740), 'L': (663, 824)
        }

        self.caminos_detallados = {
            ('A', 'D'): [(139, 374), (142, 509), (36, 512), (52, 509)],
            ('A', 'E'): [(139, 374), (265, 378), (271, 508), (330, 510)],
            ('A', 'B'): [(139, 374), (663, 374)],
            ('D', 'H'): [(52, 509), (34, 510), (34, 622), (247, 619)],
            ('E', 'I'): [(330, 510), (365, 510), (368, 712), (478, 724)],
            ('E', 'F'): [(330, 510), (365, 474), (663, 474)],
            ('F', 'E'): [(663, 474), (364, 474), (365, 510), (330, 510)],
            ('F', 'G'): [(663, 474), (965, 512)],
            ('F', 'J'): [(663, 474), (671, 665)],
            ('G', 'K'): [(965, 512), (965, 740)],
            ('B', 'C'): [(663, 374), (965, 372)],
            ('B', 'F'): [(663, 374), (663, 474)],
            ('C', 'G'): [(965, 372), (965, 512)],
            ('H', 'I'): [(247, 619), (249, 711), (368, 712), (478, 724)],
            ('I', 'L'): [(478, 724), (479, 824), (663, 824), (663, 824)],
            ('I', 'J'): [(478, 724), (540, 721), (540, 673), (653, 670)],
            ('J', 'I'): [(653, 670), (540, 673), (540, 721), (478, 724)],
            ('J', 'K'): [(653, 670), (963, 674), (965, 740)],
            ('L', 'K'): [(663, 824), (663, 852), (712, 856), (715, 902), (956, 902), (965, 740)],
        }

        for nodo, (x, y) in self.posiciones_nodos.items():
            puente = puentes.get(nodo, None)  # Obtener el puente correspondiente al nodo
            self.ciudad.add_node(nodo, pos=(x, y), puente=puente)

        for (nodo1, nodo2), camino in self.caminos_detallados.items():
            if nodo1 in self.ciudad.nodes and nodo2 in self.ciudad.nodes:
                peso_max = min(puentes[nodo1].peso_maximo, puentes[nodo2].peso_maximo)
                peso_arista = max(1, peso_max // capacidad_camioneta)  # Usar la capacidad de la camioneta
                puente = puentes.get(nodo1)  # Suponiendo que usas el puente del nodo inicial
                self.ciudad.add_edge(nodo1, nodo2, weight=peso_arista, puente=puente, camino=camino)
            else:
                print(f"Error: Nodo {nodo1} o Nodo {nodo2} no está presente en el grafo.")

    def simular_ruta_en_pygame(self, rutas, camino, dinero_a_enviar):
        vehiculo_asignado = rutas.asignar_vehiculo(dinero_a_enviar)
        if vehiculo_asignado:
            print(f"Vehículo asignado: {vehiculo_asignado.id}")
            ruta_detallada = rutas.construir_ruta_detallada(camino)
            vehiculo_asignado.ruta_detallada = ruta_detallada
            
            # Actualizar posición actual si la ruta detallada tiene al menos un punto
            if ruta_detallada:
                vehiculo_asignado.posicion_actual = ruta_detallada[0]
                vehiculo_asignado.indice_destino = 1  # Inicializar indice_destino a 1
            
            print(f"Ruta detallada asignada al vehículo {vehiculo_asignado.id}: {ruta_detallada}")
            self.vehiculos[vehiculo_asignado.id] = vehiculo_asignado
            self.render_thread.update_vehiculos(self.vehiculos)
        else:
            print("No se pudo asignar un vehículo.")
    def actualizar_ciudad(self, rutas):
        self.vehiculos = rutas.vehiculos.copy()
        print(f"Vehículos actualizados en la ciudad: {self.vehiculos}")

    
    def dibujar(self, screen):
        print("Dibujando ciudad")
    
        for nodo, (x, y) in self.posiciones_nodos.items():
            pygame.draw.circle(screen, (255, 0, 0), (x, y), 10)
        # Dibujar vehículos y rutas detalladas
        for vehiculo in self.vehiculos.values():
            print(f"Dibujando vehículo {vehiculo.id}")

            if vehiculo.tipo == 'camioneta':
                imagen_vehiculo = self.imagenes_vehiculos['Camioneta']
            elif vehiculo.tipo == 'blindado':
                imagen_vehiculo = self.imagenes_vehiculos['Blindado']
            else:
                imagen_vehiculo = self.imagenes_vehiculos['Ladron']

            # Verificar si el vehículo tiene una ruta detallada asignada
            if vehiculo.ruta_detallada:
                camino_detallado = vehiculo.ruta_detallada
                print(f"Camino detallado para el vehículo {vehiculo.id}: {camino_detallado}")

                # Dibujar el camino detallado en la pantalla
                pygame.draw.lines(screen, (0, 255, 0), False, camino_detallado, 5)

                # Verificar si el vehículo tiene una posición actual definida
                if vehiculo.posicion_actual:
                    x, y = vehiculo.posicion_actual
                    screen.blit(imagen_vehiculo, (x - imagen_vehiculo.get_width() // 2, y - imagen_vehiculo.get_height() // 2))
                else:
                    print(f"El vehículo {vehiculo.id} no tiene posición actual definida.")
            else:
                print(f"El vehículo {vehiculo.id} no tiene ruta detallada asignada.")

                # Dibujar el vehículo en su posición actual si no tiene ruta detallada
                if hasattr(vehiculo, 'posicion_actual') and vehiculo.posicion_actual in self.posiciones_nodos:
                    x, y = self.posiciones_nodos[vehiculo.posicion_actual]
                    screen.blit(imagen_vehiculo, (x - imagen_vehiculo.get_width() // 2, y - imagen_vehiculo.get_height() // 2))

    def stop_pygame(self):
        if self.render_thread:
            self.render_thread.stop()
            self.pygame_running = False
