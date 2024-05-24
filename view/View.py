import pygame
import networkx as nx
from view.Ciudad import Ciudad
from src.Botin import CentroDeOperacion, Cliente, Vehiculo, Escolta, Contenedor, Puente, BandaLadrones
from src.Rutas import Rutas
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import csv
import sys
import threading

class Button:
    def __init__(self, x, y, w, h, text, action=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (0, 0, 0)
        self.text = text
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(self.text, True, (255, 255, 255))
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def click(self):
        if self.action:
            self.action()

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((1100, 1000))
    pygame.display.set_caption("Modelo de Ciudad")

    ciudad = Ciudad()
    ciudad.background = pygame.image.load('./src/image/cuidad.jpeg')

    # Definir botón
    planificar_button = Button(10, 10, 150, 50, 'Registro', lambda: threading.Thread(target=mostrar_formulario, args=(ciudad,)).start())

    corriendo = True
    while corriendo:
        pantalla.fill((255, 255, 255))
        if ciudad.background:
            pantalla.blit(ciudad.background, (0, 0))

        planificar_button.draw(pantalla)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if planificar_button.is_clicked(evento.pos):
                    planificar_button.click()

        pygame.display.flip()

    pygame.quit()

def mostrar_formulario(ciudad):
    app = QApplication(sys.argv)

    class Formulario(QWidget):
        def __init__(self):
            super().__init__()
            self.init_ui()

        def init_ui(self):
            self.setWindowTitle("Planificar Ruta")
            layout = QVBoxLayout()

            self.origen_label = QLabel("Nombre")
            self.origen_input = QLineEdit(self)
            layout.addWidget(self.origen_label)
            layout.addWidget(self.origen_input)
            
            self.cantidad_dinero_label = QLabel("Cantidad de Dinero")
            self.cantidad_dinero_input = QLineEdit(self)
            layout.addWidget(self.cantidad_dinero_label)
            layout.addWidget(self.cantidad_dinero_input)

            self.destino_label = QLabel("Destino")
            self.destino_input = QLineEdit(self)
            layout.addWidget(self.destino_label)
            layout.addWidget(self.destino_input)

            self.capacidad_puente_maxima_label = QLabel("Tiempo estimado de entrega")
            self.capacidad_puente_maxima_input = QLineEdit(self)
            layout.addWidget(self.capacidad_puente_maxima_label)
            layout.addWidget(self.capacidad_puente_maxima_input)

            self.submit_button = QPushButton("Submit", self)
            self.submit_button.clicked.connect(self.on_submit)
            layout.addWidget(self.submit_button)

            self.setLayout(layout)

        def on_submit(self):
            origen = self.origen_input.text()
            destino = self.destino_input.text()
            cantidad_dinero = int(self.cantidad_dinero_input.text())
            capacidad_puente_maxima = int(self.capacidad_puente_maxima_input.text())

            # Guardar en CSV
            with open('registro.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([origen, destino, cantidad_dinero, capacidad_puente_maxima])

            costo_ruta, camino, vehiculo_seleccionado = Rutas.planificar_ruta(ciudad, origen, destino, cantidad_dinero, capacidad_puente_maxima)
            if camino:
                QMessageBox.information(self, "Ruta Planificada", f"Ruta: {camino}, Costo: {costo_ruta}, Vehículo: {vehiculo_seleccionado.id}")
            else:
                QMessageBox.warning(self, "Error", "No se encontró una ruta válida")

            self.close()

    formulario = Formulario()
    formulario.show()
    app.exec_()

