import pygame
from PySide6.QtCore import QThread, Signal

class RenderThread(QThread):
    finished_signal = Signal()

    def __init__(self, ciudad, vehiculos, parent=None):
        super().__init__(parent)
        self.ciudad = ciudad
        self.vehiculos = vehiculos  # Almacenar el diccionario vehiculos
        self.nodos_ruta_actual = []
        self.running = False
        
    def run(self):
        pygame.init()
        print("Pygame inicializado")

        screen = pygame.display.set_mode((1100, 1000))
        pygame.display.set_caption("Rutas")

        print(f"Ruta de la imagen de fondo: {self.ciudad.rutas_imagenes['ciudad']}")
        background = pygame.image.load(self.ciudad.rutas_imagenes['ciudad']).convert()
        
        self.running = True
        while self.running:
            print("Dentro del bucle principal")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Dibujar el fondo de la ciudad en la ventana de Pygame
            screen.blit(background, (0, 0))
           
            for vehiculo in self.vehiculos.values():
                 vehiculo.actualizar_posicion()
           
            # Dibujar la ciudad (nodos, caminos, vehículos, etc.)
            self.ciudad.dibujar(screen)
      
            pygame.display.flip()
            pygame.time.delay(1500)

        pygame.quit()
        self.finished_signal.emit()

    def stop(self):
        self.running = False
        pygame.quit()
        self.wait()
