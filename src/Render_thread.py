import pygame
from PySide6.QtCore import QThread, Signal

class RenderThread(QThread):
    finished_signal = Signal()

    def __init__(self, ciudad, parent=None):
        super().__init__(parent)
        self.ciudad = ciudad
        self.nodos_ruta_actual = []
        self.running = False


    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((1100, 1000))
        pygame.display.set_caption("Rutas")

        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            background = pygame.image.load('./data/image/ciudad.jpeg')       
            escolta = pygame.image.load('./data/image/Moto.png')
            banda = pygame.image.load('./data/image/Banda.png')
            banda2 = pygame.image.load('./data/image/Banda2.png')
            banda3 = pygame.image.load('./data/image/Banda3.png')
            ladron = pygame.image.load('./data/image/Ladron.png')
            ladron2 = pygame.image.load('./data/image/Ladron2.png')
            ladron3 = pygame.image.load('./data/image/Ladron3.png')
            
            # Dibujar el fondo de la ciudad en la ventana de Pygame
            screen.blit(background, (0, 0))

            # Aquí puedes agregar más lógica de dibujo de objetos, personajes, etc.
            self.ciudad.dibujar(screen, self.nodos_ruta_actual)
            
            pygame.display.flip()
            pygame.time.delay(10)

        pygame.quit()
        self.finished_signal.emit()

    def stop(self):
        self.running = False
        pygame.quit()
        self.wait()