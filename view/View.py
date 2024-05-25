import pygame
import networkx as nx
from view.Cuidad import Ciudad
from src.Botin import Vehiculo
from src.Rutas import Rutas
from PySide6.QtWidgets import QDialog, QListWidget, QAbstractItemView, QComboBox, QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import QObject, Signal, Qt
import csv
import sys


class MainWindow(QObject):
    show_form_signal = Signal()
    show_simulation_dialog_signal = Signal()

    def __init__(self):
        super().__init__()
        self.ciudad = Ciudad()
        self.ciudad.background = pygame.image.load('./data/image/cuidad.jpeg')

        # Inicializar botones en Pygame
        self.boton_registro = pygame.Rect(10, 10, 120, 40)
        self.boton_simulaciones = pygame.Rect(170, 10, 150, 40)
        self.corriendo = True

        pygame.init()
        self.pantalla = pygame.display.set_mode((1100, 1000))
        pygame.display.set_caption("Modelo de Ciudad")

        # Definir vehículos con parámetros personalizados
        self.Camioneta = Vehiculo(id=1, tipo="camioneta", velocidad=3, capacidad=500, escudo=5, ataque=10, escoltas_necesarias=1)
        self.Blindado = Vehiculo(id=2, tipo="blindado", velocidad=1, capacidad=2500, escudo=20, ataque=15, escoltas_necesarias=2)

        self.show_form_signal.connect(self.mostrar_formulario)
        self.show_simulation_dialog_signal.connect(self.mostrar_dialogo_simulaciones)

    def handle_events(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.corriendo = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if self.boton_registro.collidepoint(evento.pos):
                    self.show_form_signal.emit()
                elif self.boton_simulaciones.collidepoint(evento.pos):
                    self.show_simulation_dialog_signal.emit()

    def mostrar_dialogo_simulaciones(self):
        dialogo = DialogoSimulaciones()
        dialogo.exec_()

    def mostrar_formulario(self):
        formulario = Formulario()
        formulario.show()

    def main(self):
        while self.corriendo:
            self.handle_events()

            self.pantalla.fill((255, 255, 255))
            if self.ciudad.background:
                self.pantalla.blit(self.ciudad.background, (0, 0))

            # Dibujar botones
            pygame.draw.rect(self.pantalla, (0, 103, 105), self.boton_registro)
            pygame.draw.rect(self.pantalla, (0, 103, 105), self.boton_simulaciones)
            font = pygame.font.SysFont(None, 28)  # Usa la fuente predeterminada
            text_surface_registro = font.render("Registro", True, (255, 255, 255))
            text_surface_simulaciones = font.render("Simulaciones", True, (255, 255, 255))
            self.pantalla.blit(text_surface_registro, (self.boton_registro.x + 10, self.boton_registro.y + 10))
            self.pantalla.blit(text_surface_simulaciones, (self.boton_simulaciones.x + 10, self.boton_simulaciones.y + 10))

            pygame.display.flip()

        pygame.quit()


class DialogoSimulaciones(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulaciones")
        self.resize(400, 200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.boton_generar_ruta = QPushButton("Generar Ruta")
        self.boton_generar_ruta.clicked.connect(self.generar_ruta)
        layout.addWidget(self.boton_generar_ruta)

        self.boton_banda = QPushButton("Banda")
        self.boton_banda.clicked.connect(self.mostrar_banda)
        layout.addWidget(self.boton_banda)

        self.setLayout(layout)
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 10px 0;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

    def mostrar_banda(self):
        QMessageBox.information(self, "Información de la Banda", "Detalles de la banda de ladrones...")

    def generar_ruta(self):
        pass  # Aquí iría la lógica para generar la ruta


class Formulario(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Planificar Ruta")
        self.resize(400, 400)
        layout = QVBoxLayout()

        self.origen_label = QLabel("Nombre")
        self.origen_input = QLineEdit(self)
        layout.addWidget(self.origen_label)
        layout.addWidget(self.origen_input)

        self.cantidad_dinero_label = QLabel("Dinero a enviar")
        self.cantidad_dinero_input = QLineEdit(self)
        layout.addWidget(self.cantidad_dinero_label)
        layout.addWidget(self.cantidad_dinero_input)

        self.destino_label = QLabel("Destino")
        self.destino_input = QComboBox(self)
        self.destino_input.addItem("Dirección del Cliente")
        self.destino_input.addItem("Entre varios clientes")
        layout.addWidget(self.destino_label)
        layout.addWidget(self.destino_input)

        self.lista_destinos_label = QLabel("Seleccione los destinos")
        self.lista_destinos = QListWidget(self)
        self.lista_destinos.addItems(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"])
        self.lista_destinos.setSelectionMode(QAbstractItemView.MultiSelection)
        self.lista_destinos.setVisible(False)
        self.lista_destinos_label.setVisible(False)
        layout.addWidget(self.lista_destinos_label)
        layout.addWidget(self.lista_destinos)

        self.capacidad_puente_maxima_label = QLabel("Tiempo estimado de entrega")
        self.capacidad_puente_maxima_input = QLineEdit(self)
        layout.addWidget(self.capacidad_puente_maxima_label)
        layout.addWidget(self.capacidad_puente_maxima_input)

        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.on_submit)
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        layout.addWidget(self.submit_button)

        self.destino_input.currentIndexChanged.connect(self.toggle_lista_destinos)
        self.setLayout(layout)

    def toggle_lista_destinos(self, index):
        if self.destino_input.currentText() == "Entre varios clientes":
            self.lista_destinos.setVisible(True)
            self.lista_destinos_label.setVisible(True)
        else:
            self.lista_destinos.setVisible(False)
            self.lista_destinos_label.setVisible(False)

    def on_submit(self):
        origen = self.origen_input.text()
        destino = self.destino_input.currentText()
        cantidad_dinero = int(self.cantidad_dinero_input.text())
        capacidad_puente_maxima = int(self.capacidad_puente_maxima_input.text())

        if destino == "Entre varios clientes":
            destinos = [item.text() for item in self.lista_destinos.selectedItems()]
            destino = ", ".join(destinos)

        # Guardar en CSV
        with open('./data/registro.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([origen, destino, cantidad_dinero, capacidad_puente_maxima])

        costo_ruta, camino, vehiculo_seleccionado = Rutas.planificar_ruta(self.ciudad, origen, destino, cantidad_dinero, capacidad_puente_maxima)
        if camino:
            if vehiculo_seleccionado.capacidad >= cantidad_dinero:
                QMessageBox.information(self, "Ruta Planificada", f"Ruta: {camino}, Costo: {costo_ruta}, Vehículo: {vehiculo_seleccionado.id}")
            else:
                QMessageBox.warning(self, "Capacidad Insuficiente", "El vehículo seleccionado no tiene suficiente capacidad.")
        else:
            QMessageBox.critical(self, "Error", "No se encontró una ruta válida o no se puede hacer a tiempo")

        self.close()
