from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from src.Cuidad import CiudadModel
from src.Botin import Vehiculo, Escolta, Ladron

def agent_portrayal(agent):
    if type(agent) is Vehiculo:
        portrayal = {"Shape": "circle", "Color": "blue", "Filled": "true", "Layer": 0, "r": 0.5}
    elif type(agent) is Escolta:
        portrayal = {"Shape": "circle", "Color": "green", "Filled": "true", "Layer": 0, "r": 0.5}
    elif type(agent) is Ladron:
        portrayal = {"Shape": "circle", "Color": "red", "Filled": "true", "Layer": 0, "r": 0.5}
    return portrayal

# CanvasGrid is used to visualize the agents on a grid
grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

# ChartModule is used to visualize the collected data
chart = ChartModule(
    [
        {"Label": "Escudo", "Color": "Black"},
        {"Label": "Ataque", "Color": "Red"}
    ]
)

# ModularServer is used to set up and launch the server
server = ModularServer(CiudadModel,
                       [grid, chart],
                       "Modelo de Ciudad",
                       {"width": 10, "height": 10, "num_vehiculos": 10, "num_escoltas": 5, "num_ladrones": 3})

server.port = 8521  # The default port to run the server
def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Color": "blue",
        "Filled": "true",
        "Layer": 0,
        "r": 0.5
    }
    if isinstance(agent, Vehiculo):
        portrayal["Shape"] = "./src/image/carro.png"
    elif isinstance(agent, Escolta):
        portrayal["Shape"] = "./src/image/Moto.png"
    elif isinstance(agent, Ladron):
        portrayal["Shape"] = "./src/image/Ladron.png"
    
    return portrayal

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

chart = ChartModule([
    {"Label": "Escudo", "Color": "Black"},
    {"Label": "Ataque", "Color": "Red"}
])

server = ModularServer(
    CiudadModel,
    [grid, chart],
    "Modelo de Ciudad",
    {"width": 10, "height": 10, "num_vehiculos": 10, "num_escoltas": 5, "num_ladrones": 3}
)

server.port = 8521

server.launch()
