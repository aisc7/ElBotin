from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from src.Botin import Vehiculo, Escolta, Ladron

class CiudadModel(Model):
    def __init__(self, width, height, num_vehiculos, num_escoltas, num_ladrones):
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        # Crear vehículos
        for i in range(num_vehiculos):
            capacidad = 1000
            escudo = 20
            ataque = 15
            escoltas_necesarias = 2
            vehiculo = Vehiculo(i, self, capacidad, escudo, ataque, escoltas_necesarias)
            self.schedule.add(vehiculo)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(vehiculo, (x, y))

        # Crear escoltas
        for i in range(num_escoltas):
            escudo = 5
            ataque = 5
            escolta = Escolta(i + num_vehiculos, self, escudo, ataque)
            self.schedule.add(escolta)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(escolta, (x, y))

        # Crear ladrones
        for i in range(num_ladrones):
            ataque = 10
            escudo = 5
            ladron = Ladron(i + num_vehiculos + num_escoltas, self, ataque, escudo)
            self.schedule.add(ladron)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(ladron, (x, y))

        self.datacollector = DataCollector(
            agent_reporters={"Escudo": "escudo", "Ataque": "ataque"}
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
