# Botin.py
from mesa import Agent

class Vehiculo(Agent):
    def __init__(self, unique_id, model, capacidad, escudo, ataque, escoltas_necesarias):
        super().__init__(unique_id, model)
        self.capacidad = capacidad
        self.escudo = escudo
        self.ataque = ataque
        self.escoltas_necesarias = escoltas_necesarias

    def step(self):
        # Lógica del comportamiento del vehículo en cada paso de la simulación
        pass

class Escolta(Agent):
    def __init__(self, unique_id, model, escudo, ataque):
        super().__init__(unique_id, model)
        self.escudo = escudo
        self.ataque = ataque

    def step(self):
        # Lógica del comportamiento del escolta en cada paso de la simulación
        pass

class Ladron(Agent):
    def __init__(self, unique_id, model, ataque, escudo):
        super().__init__(unique_id, model)
        self.ataque = ataque
        self.escudo = escudo

    def step(self):
        # Lógica del comportamiento del ladrón en cada paso de la simulación
        pass
