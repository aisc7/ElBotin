# src/Botin.py

class CentroDeOperacion:
    def __init__(self, id, capacidad_dinero, capacidad_vehiculos, capacidad_escoltas):
        self.id = id
        self.capacidad_dinero = 10.000
        self.capacidad_vehiculos = 7
        self.capacidad_escoltas = 10
        self.dinero = 0
        self.vehiculos = []
        self.escoltas = []

    def agregar_vehiculo(self, vehiculo):
        if len(self.vehiculos) < self.capacidad_vehiculos:
            self.vehiculos.append(vehiculo)

    def agregar_escolta(self, escolta):
        if len(self.escoltas) < self.capacidad_escoltas:
            self.escoltas.append(escolta)

    def almacenar_dinero(self, cantidad):
        if self.dinero + cantidad <= self.capacidad_dinero:
            self.dinero += cantidad
        else:
            raise ValueError("Capacidad de dinero excedida en el centro de operación")

class Cliente:
    def __init__(self, id):
        self.id = id
        self.dinero = 0

class Vehiculo:
    def __init__(self, id, tipo, velocidad, capacidad, escudo, ataque, escoltas_necesarias):
        self.id = id
        self.tipo = tipo
        self.velocidad = velocidad
        self.capacidad = capacidad
        self.escudo = escudo
        self.ataque = ataque
        self.escoltas_necesarias = escoltas_necesarias
        self.contenedores_permitidos = self.establecer_contenedores_permitidos()
        self.posicion = (139, 374) 
    def establecer_contenedores_permitidos(self):
        if self.tipo == "camioneta":
            return ["Tipo1", "Tipo2"]  # Ejemplo de contenedores permitidos para camioneta
        elif self.tipo == "blindado":
            return ["Tipo3", "Tipo4"]  # Ejemplo de contenedores permitidos para vehículo blindado
        else:
            raise ValueError("Tipo de vehículo no válido")
        
    def puede_llevar_contenedor(self, tipo_contenedor):
        return tipo_contenedor in self.contenedores_permitidos

    def actualizar_posicion(self, nueva_posicion):
            self.posicion = nueva_posicion

class Escolta:
    def __init__(self, id, escudo, ataque):
        self.id = id
        self.escudo = escudo
        self.ataque = ataque

class Contenedor:
    def __init__(self, id, tipo_contenedor):
        self.id = id
        self.tipo_contenedor = tipo_contenedor
        self.capacidad_peso = self.establecer_capacidad_peso()

    def establecer_capacidad_peso(self):
        if self.tipo_contenedor == "pequeno":
            return 200   # Capacidad máxima de peso para contenedor pequeño
        elif self.tipo_contenedor == "mediano":
            return 500  # Capacidad máxima de peso para contenedor mediano
        elif self.tipo_contenedor == "grande":
            return 2000  # Capacidad máxima de peso para contenedor grande
        elif self.tipo_contenedor == "doble":
            return 2500 or 2200
        else:
            raise ValueError("Tipo de contenedor no válido")

class Puente:
    def __init__(self, id, peso_maximo):
        self.id = id
        self.peso_maximo = peso_maximo
        self.colapsado = False

    def puede_cruzar(self, peso_vehiculo):
        return peso_vehiculo <= self.peso_maximo

    def colapsar(self):
        self.colapsado = True

class BandaLadrones:
    def __init__(self, id):
        self.id = id
