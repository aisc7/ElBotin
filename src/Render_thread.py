import pygame
from PySide6.QtCore import QThread, Signal

class RenderThread(QThread):
    finished_signal = Signal()

    def __init__(self, ciudad, parent=None):
        super().__init__(parent)
        self.ciudad = ciudad
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
