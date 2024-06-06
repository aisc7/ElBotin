#view/View.py
import os
import csv
import pygame
from src.Rutas import Rutas
from src.Botin import Vehiculo
from PySide6.QtCore import Signal
from view.Ciudad import Ciudad, RenderThread
from PySide6.QtWidgets import QApplication,QDialog,QInputDialog,QMessageBox,QAbstractItemView, QListWidget, QMainWindow, QTabWidget, QComboBox, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton



class RegistroWidget(QWidget):
    def __init__(self, ciudad, parent=None):
        super(RegistroWidget, self).__init__(parent)
        self.ciudad = ciudad
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Planificar Ruta")
        layout = QVBoxLayout()

        self.origen_label = QLabel("Nombre")
        self.origen_input = QLineEdit(self)
        layout.addWidget(self.origen_label)
        layout.addWidget(self.origen_input)
        
        self.cantidad_dinero_label = QLabel("Dinero a enviar")
        self.cantidad_dinero_input = QComboBox(self)
        dinero_opciones = [str(i) for i in range(100, 2600, 100)]  # Genera opciones desde 100 hasta 2500 en incrementos de 100
        self.cantidad_dinero_input.addItems(dinero_opciones)
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

        self.tiempo_estimado_label = QLabel("Tiempo estimado de entrega")
        self.tiempo_estimado_input = QComboBox(self)
        self.tiempo_estimado_input.addItems(["10 minutos", "15 minutos", "30 minutos", "1 hora"])
        layout.addWidget(self.tiempo_estimado_label)
        layout.addWidget(self.tiempo_estimado_input)
        
        self.guardar_button = QPushButton("Guardar", self)
        self.guardar_button.clicked.connect(self.on_guardar)
        layout.addWidget(self.guardar_button)

        self.destino_input.currentIndexChanged.connect(self.toggle_lista_destinos)
        self.setLayout(layout)

    def toggle_lista_destinos(self, index):
        if self.destino_input.currentText() == "Entre varios clientes":
            self.lista_destinos.setVisible(True)
            self.lista_destinos_label.setVisible(True)
        else:
            self.lista_destinos.setVisible(False)
            self.lista_destinos_label.setVisible(False)

    def on_guardar(self):
        nombre = self.origen_input.text()
        destino = self.destino_input.currentText()
        cantidad_dinero = int(self.cantidad_dinero_input.currentText())
        tiempo_estimado = self.tiempo_estimado_input.currentText()

        if destino == "Entre varios clientes":
            destinos = [item.text() for item in self.lista_destinos.selectedItems()]
            destino = ", ".join(destinos)

      # Guardar en CSV
        file_path = './data/registro.csv'
        file_exists = os.path.isfile(file_path)

        try:
            with open(file_path, 'a', newline='') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(["Nombre", "Dinero_a_enviar", "Destino", "Tiempo_estimado"])
                writer.writerow([nombre, cantidad_dinero, destino, tiempo_estimado])
        except Exception as e:
            QMessageBox.critical(self, "Error al guardar", f"No se pudo guardar en el archivo CSV: {str(e)}")
            return

    # Mostrar alerta de guardado exitoso
        QMessageBox.information(self, "Guardado Exitoso", "Los datos han sido guardados correctamente en el archivo CSV.")

        
        # costo_ruta, camino, vehiculo_seleccionado = Rutas.planificar_ruta(self.ciudad, origen, destino, cantidad_dinero, capacidad_puente_maxima)
        # if camino:
        #     if vehiculo_seleccionado.capacidad >= cantidad_dinero:
        #         QMessageBox.information(self, "Ruta Planificada", f"Ruta: {camino}, Costo: {costo_ruta}, Vehículo: {vehiculo_seleccionado.id}")
        #     else:
        #         QMessageBox.warning(self, "Capacidad Insuficiente", "El vehículo seleccionado no tiene suficiente capacidad.")
        # else:
        #     QMessageBox.critical(self, "Error", "No se encontró una ruta válida o no se puede hacer a tiempo")
    # Limpiar campos después de guardar
        self.origen_input.clear()
        self.cantidad_dinero_input.setCurrentIndex(0)
        self.destino_input.setCurrentIndex(0)
        self.tiempo_estimado_input.setCurrentIndex(0)
        self.lista_destinos.clearSelection()


class BandaDialog(QDialog):
    def __init__(self, parent=None):
        super(BandaDialog, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Configuración de la Banda")
        self.resize(400, 300)
        layout = QVBoxLayout()
        clientes = self.obtener_clientes_del_csv()
        if not clientes:
            QMessageBox.warning(self, "Advertencia", "No hay clientes registrados.")
            return

        self.cliente_input = QComboBox(self)
        self.cliente_input.addItems(clientes)
        layout.addWidget(QLabel("Seleccionar Cliente"))
        layout.addWidget(self.cliente_input)

        self.ataque_label = QLabel("Ataque")
        self.ataque_input = QComboBox(self)
        ataque_opciones = [str(i) for i in range(5, 35, 5)]  # Opciones de ataque: 5, 10, 15, 20, 25, 30
        self.ataque_input.addItems(ataque_opciones)
        layout.addWidget(self.ataque_label)
        layout.addWidget(self.ataque_input)

        self.escudo_label = QLabel("Escudo")
        self.escudo_input = QComboBox(self)
        escudo_opciones = [str(i) for i in range(5, 45, 5)]  # Opciones de escudo: 5, 10, 15, 20, 25, 30, 35, 40
        self.escudo_input.addItems(escudo_opciones)
        layout.addWidget(self.escudo_label)
        layout.addWidget(self.escudo_input)

        self.guardar_button = QPushButton("Guardar", self)
        self.guardar_button.clicked.connect(self.accept)
        layout.addWidget(self.guardar_button)

        self.setLayout(layout)

    def get_values(self):
        ataque = int(self.ataque_input.currentText())
        escudo = int(self.escudo_input.currentText())
        cliente = self.cliente_input.currentText()
        return ataque, escudo, cliente

    def obtener_clientes_del_csv(self):
        try:
            with open('./data/registro.csv', 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Saltar el encabezado si lo hay
                clientes = [row[0] for row in reader]  # Suponiendo que el nombre del cliente está en la primera columna
            return clientes
        except Exception as e:
            QMessageBox.critical(self, "Error al leer CSV", f"No se pudo leer el archivo CSV: {str(e)}")
            return []

class SimulacionDialogoWidget(QWidget):
    def __init__(self, parent=None):
        super(SimulacionDialogoWidget, self).__init__(parent)
        self.clientes_datos = {}  # Inicializar el diccionario aquí
        self.init_ui()
        self.cargar_datos_clientes() 
        
    def init_ui(self):
        layout = QVBoxLayout()

        self.boton_generar_ruta = QPushButton("Generar Ruta")
        self.boton_generar_ruta.clicked.connect(self.generar_ruta)
        layout.addWidget(self.boton_generar_ruta)

        self.boton_banda = QPushButton("Banda")
        self.boton_banda.clicked.connect(self.mostrar_banda)
        layout.addWidget(self.boton_banda)
        
        self.boton_simular = QPushButton("Simular")
        self.boton_simular.clicked.connect(self.simular_pygame)
        layout.addWidget(self.boton_simular)

        self.setLayout(layout)

    def simular_pygame(self):
        self.ciudad = Ciudad()
        self.ciudad.iniciar_pygame()
        # llamar la funcion procesar_solicitudes de la clase ciudad
    
    def mostrar_banda(self):
        dialog = BandaDialog(self)
        if dialog.exec():
            ataque, escudo, cliente = dialog.get_values()
            QMessageBox.information(self, "Valores Seleccionados", f"Ataque: {ataque}, Escudo: {escudo}, Cliente: {cliente}")

    def generar_ruta(self):
        clientes = self.obtener_clientes_del_csv()
        if not clientes:
            QMessageBox.warning(self, "Advertencia", "No hay clientes registrados.")
            return

        cliente, simular = QInputDialog.getItem(self, "Seleccionar Cliente", "Elige un cliente:", clientes, 0, False)
        if simular and cliente:
            QMessageBox.information(self, "Cliente a simular", f"Simularás a: {cliente}")

            # Obtener los datos del cliente seleccionado
            cantidad_dinero, destino, tiempo_estimado = self.obtener_datos_cliente(cliente)

            # Crear una instancia de la clase Rutas
            rutas = Rutas()

            # Llamar al método planificar_ruta de la instancia rutas
            mejor_ruta, mensaje = rutas.planificar_ruta(cliente, destino, cantidad_dinero, tiempo_estimado)

            # Procesar el resultado obtenido
            if mejor_ruta:
                costo, camino = mejor_ruta
                # Realizar las operaciones necesarias con el camino y el costo
                print(f"Costo de la mejor ruta para el cliente {cliente}: {costo}")
                print(f"Camino de la mejor ruta para el cliente {cliente}: {camino}")
            else:
                print(mensaje)

    def cargar_datos_clientes(self):
        try:
            with open('./data/registro.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    nombre = row['Nombre']
                    dinero_a_enviar = int(row['Dinero_a_enviar'])
                    destino = row['Destino'].strip()  # Obtener destino como texto y quitar espacios innecesarios
                    tiempo_estimado_texto = row['Tiempo_estimado'].strip()  # Obtener tiempo estimado como texto
                    tiempo_estimado = self.convertir_tiempo_a_minutos(tiempo_estimado_texto)

                    # Guardar los datos en el diccionario de clientes
                    self.clientes_datos[nombre] = (dinero_a_enviar, destino, tiempo_estimado)

        except Exception as e:
            QMessageBox.critical(self, "Error al leer CSV", f"No se pudo leer el archivo CSV: {str(e)}")

    def convertir_tiempo_a_minutos(self, tiempo_texto):
        tiempo_texto = tiempo_texto.lower()  # Convertir texto a minúsculas para manejar diferentes casos
        if tiempo_texto == "10 minutos":
            return 10
        elif tiempo_texto == "15 minutos":
            return 15
        elif tiempo_texto == "30 minutos":
            return 30
        elif tiempo_texto == "1 hora":
            return 60
        return 0  # Retornar 0 si el formato no coincide
    
    def obtener_clientes_del_csv(self):
        return list(self.clientes_datos.keys())

    def obtener_datos_cliente(self, cliente):
        datos_cliente = self.clientes_datos.get(cliente)
        if datos_cliente:
            return datos_cliente
        else:
            QMessageBox.warning(self, "Cliente no encontrado", f"No se encontraron datos para el cliente '{cliente}'")
            return 0, '', 0

class MainWindow(QMainWindow):
    show_form_signal = Signal()
    show_simulation_dialog_signal = Signal()

    def __init__(self):
        super().__init__()
        self.ciudad = Ciudad()
        self.ciudad.background = pygame.image.load('./data/image/ciudad.jpeg')

        self.Camioneta = Vehiculo(id=1, tipo="camioneta", velocidad=3, capacidad=500, escudo=5, ataque=10, escoltas_necesarias=1)
        self.Blindado = Vehiculo(id=2, tipo="blindado", velocidad=1, capacidad=2500, escudo=20, ataque=15, escoltas_necesarias=2)
        self.render_thread = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Simulación de Rutas")

        # Establecer tamaño de la ventana
        self.resize(800, 800)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Crear las pestañas
        self.registro_tab = RegistroWidget(self.ciudad)
        self.simulacion_dialogo_tab = SimulacionDialogoWidget()
      
        # Añadir las pestañas al widget de pestañas
        self.tabs.addTab(self.registro_tab, "Registro")
        self.tabs.addTab(self.simulacion_dialogo_tab, "Ajustes de Simulación")
        
        # Conectar señales a métodos
        self.show_form_signal.connect(self.mostrar_formulario)
        self.show_simulation_dialog_signal.connect(self.mostrar_dialogo_simulaciones)
        
        self.apply_styles()    
    def apply_styles(self):
     self.setStyleSheet("""
        QTabWidget::pane {
            border: 1px solid #50623A;
        }
        QTabBar::tab {
            background: #50623A;
            border: 1px solid #C4C4C3;
            padding: 10px; /* Aumenta el padding para espaciar más los tabs */
            margin: 1px;
            font-size: 17px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }
        QTabBar::tab:selected {
            background: #294B29;
            margin-bottom: 2px;
        }
        QLabel {
            font-size: 15px; /* Aumenta el tamaño de la fuente de las etiquetas */
        }
        QLineEdit, QComboBox, QListWidget {
            font-size: 15px; /* Aumenta el tamaño de la fuente de los campos de entrada, combo boxes y listas */
            padding: 10px; /* Aumenta el padding para hacer los campos más grandes */
            border: 2px solid #C4C4C3; /* Aumenta el grosor del borde */
            border-radius: 8px; /* Aumenta el radio de borde para hacerlos más redondeados */
        }
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 15px 30px; /* Aumenta el padding horizontal y vertical del botón */
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 15px; /* Aumenta el tamaño de la fuente del botón */
            margin: 20px 0; /* Aumenta el margen vertical del botón */
            border-radius: 12px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }

    """)
        
    def closeEvent(self, event):
    # Método que se llama cuando se intenta cerrar la ventana principal
        if self.render_thread:
            self.render_thread.quit()
            self.render_thread.wait()
        event.accept()
        
        # Aplicar estilos
        self.apply_styles()
    
    def mostrar_dialogo_simulaciones(self):
        self.tabs.setCurrentIndex(1)
        
    def mostrar_formulario(self):
        self.tabs.setCurrentIndex(0)

  # Cerrar Pygame al cerrar la aplicación
        app = QApplication.instance()
        if app:
            app.aboutToQuit.connect(self.ciudad.stop_pygame)
        