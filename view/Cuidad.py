import pygame
import numpy as np
import pathlib
import networkx as nx

class Ciudad:
    def __init__(self):
        self.background = None
        self.partes_imagen = []  # Lista para almacenar las partes divididas
        self.ciudad = nx.Graph()  # Grafo que representa la ciudad

    def dividir_imagen(self):
        ancho_imagen, alto_imagen = self.background.get_size()
        ancho_parte = 256  # Ancho deseado para cada parte
        alto_parte = 128  # Alto deseado para cada parte

        num_filas = alto_imagen // alto_parte
        num_columnas = ancho_imagen // ancho_parte

        for f in range(num_filas):
            for c in range(num_columnas):
                nombre_parte = f'parte_{f}_{c}.png'
                x_parte = ancho_parte * c
                y_parte = alto_parte * f
                self.guardar_parte(nombre_parte, x_parte, y_parte, ancho_parte, alto_parte)

        # Manejar la última fila si es necesario
        if f < num_filas:
            alto_ultima_fila = alto_imagen % alto_parte
            nombre_parte = f'parte_{num_filas}_{c}.png'
            self.guardar_parte(nombre_parte, x_parte, y_parte, ancho_parte, alto_ultima_fila)

        # Manejar la última columna si es necesario
        if c < num_columnas:
            ancho_ultima_columna = ancho_imagen % ancho_parte
            nombre_parte = f'parte_{f}_{num_columnas}.png'
            self.guardar_parte(nombre_parte, x_parte, y_parte, ancho_ultima_columna, alto_parte)

    def guardar_parte(self, nombre_archivo, x, y, ancho, alto):
        parte = self.background.subsurface((x, y, ancho, alto))
        ruta_archivo = pathlib.Path(nombre_archivo)
        pygame.image.save(parte, ruta_archivo)

    def agregar_centro(self, id, capacidad_dinero, capacidad_vehiculos, capacidad_escoltas):
        self.ciudad.add_node(id, tipo='centro', capacidad_dinero=capacidad_dinero,
                             capacidad_vehiculos=capacidad_vehiculos, capacidad_escoltas=capacidad_escoltas)

    def agregar_cliente(self, id, demanda_dinero, tiempo_entrega, capacidad_contenedores):
        self.ciudad.add_node(id, tipo='cliente', demanda_dinero=demanda_dinero,
                             tiempo_entrega=tiempo_entrega, capacidad_contenedores=capacidad_contenedores)

    def agregar_ruta(self, origen, destino, peso):
        self.ciudad.add_edge(origen, destino, peso=peso)
