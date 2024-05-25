#/view/Cuidad.py
import pygame
import networkx as nx
import pathlib
from src.Botin import Puente

class Ciudad:
    def __init__(self):
        self.background = None
        self.imagenes_vehiculos = {}
        self.imagenes_personajes = {}
        self.ciudad = nx.DiGraph()

    def cargar_imagenes(self):
        # Cargar la imagen de fondo
        self.background = pygame.image.load('./data/image/cuidad.jpeg')

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

    def crear_grafo(self):
        nodos = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
        conexiones = [
            ('A', 'B'), ('A', 'D'), ('A', 'E'),
            ('B', 'C'), ('B', 'F'),
            ('C', 'G'),
            ('D', 'H'),
            ('E', 'F'), ('E', 'I'),
            ('F', 'G'), ('F', 'J'),
            ('G', 'K'),
            ('H', 'I'),
            ('I', 'J'), ('I', 'L'),
            ('J', 'K'),
            ('L', 'K')
        ]

        # Crear el grafo dirigido
        self.ciudad.add_nodes_from(nodos)
        self.ciudad.add_edges_from(conexiones)

        # Crear instancias de la clase Puente para representar los puentes
        puentes = {
            'A': Puente(id='A', peso_maximo=500),
            'D': Puente(id='D', peso_maximo=2500),
            'H': Puente(id='H', peso_maximo=500),
            'C': Puente(id='C', peso_maximo=2500),
            'I': Puente(id='I', peso_maximo=2500),
            'L': Puente(id='L', peso_maximo=2500)
        }

        # Agregar los puentes al grafo
        for nodo, puente in puentes.items():
            self.ciudad.nodes[nodo]['puente'] = puente

    def dividir_imagen(self):
        ancho_imagen, alto_imagen = self.background.get_size()
        ancho_parte = 256
        alto_parte = 128

        num_filas = alto_imagen // alto_parte
        num_columnas = ancho_imagen // ancho_parte

        for f in range(num_filas):
            for c in range(num_columnas):
                nombre_parte = f'parte_{f}_{c}.png'
                x_parte = ancho_parte * c
                y_parte = alto_parte * f
                self.guardar_parte(nombre_parte, x_parte, y_parte, ancho_parte, alto_parte)

        if f < num_filas:
            alto_ultima_fila = alto_imagen % alto_parte
            nombre_parte = f'parte_{num_filas}_{c}.png'
            self.guardar_parte(nombre_parte, x_parte, y_parte, ancho_parte, alto_ultima_fila)

        if c < num_columnas:
            ancho_ultima_columna = ancho_imagen % ancho_parte
            nombre_parte = f'parte_{f}_{num_columnas}.png'
            self.guardar_parte(nombre_parte, x_parte, y_parte, ancho_ultima_columna, alto_parte)

    def guardar_parte(self, nombre_archivo, x, y, ancho, alto):
        parte = self.background.subsurface((x, y, ancho, alto))
        ruta_archivo = pathlib.Path(nombre_archivo)
        pygame.image.save(parte, ruta_archivo)

    