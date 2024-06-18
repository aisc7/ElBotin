# src/Botin.py

class CentroDeOperacion:
    def __init__(self, id, capacidad_dinero, capacidad_vehiculos, capacidad_escoltas):
        self.id = id
        self.capacidad_dinero = 10000
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
    def __init__(self, id, tipo, velocidad, capacidad, escudo, ataque, escoltas_necesarias, ruta_imagen=None):
        self.id = id
        self.tipo = tipo
        self.escudo = escudo
        self.ataque = ataque
        self.ruta_imagen = ruta_imagen
        self.velocidad = velocidad
        self.capacidad = capacidad
        self.escoltas_necesarias = escoltas_necesarias
        self.contenedores_permitidos = self.establecer_contenedores_permitidos()
        self.ruta_detallada = [] 
        self.posicion_actual = None  
        self.indice_destino = 1  

    def asignar_ruta_detallada(self, ruta_detallada):
        self.ruta_detallada = ruta_detallada
        self.posicion_actual = self.ruta_detallada[0] if self.ruta_detallada else None
            
    def actualizar_posicion(self):
            if self.ruta_detallada:
                if self.indice_destino < len(self.ruta_detallada):
                    x_destino, y_destino = self.ruta_detallada[self.indice_destino]

                    if self.posicion_actual is not None:
                        x_actual, y_actual = self.posicion_actual
                        dx = x_destino - x_actual
                        dy = y_destino - y_actual
                        distancia = (dx ** 2 + dy ** 2) ** 0.5

                        if distancia > 0:
                            pasos = self.velocidad  # Utilizamos la velocidad del vehículo directamente
                            x_nuevo = x_actual + dx * pasos / distancia
                            y_nuevo = y_actual + dy * pasos / distancia

                            # Verificar si el vehículo ha pasado el punto de destino
                            if (dx >= 0 and x_nuevo >= x_destino) or (dx < 0 and x_nuevo <= x_destino):
                                x_nuevo = x_destino
                            if (dy >= 0 and y_nuevo >= y_destino) or (dy < 0 and y_nuevo <= y_destino):
                                y_nuevo = y_destino

                            self.posicion_actual = (x_nuevo, y_nuevo)

                            # Verificar si estamos lo suficientemente cerca del punto de destino
                            umbral_distancia = 5  # Ajusta este valor según la precisión requerida
                            distancia_al_destino = ((x_nuevo - x_destino) ** 2 + (y_nuevo - y_destino) ** 2) ** 0.5
                            if distancia_al_destino < umbral_distancia:
                                if self.indice_destino == len(self.ruta_detallada) - 1:
                                    # Hemos llegado al último nodo
                                    self.esta_llegado = True
                                else:
                                    self.indice_destino += 1
                        else:
                            # Si estamos exactamente en el punto de destino, avanzamos al siguiente
                            if self.indice_destino == len(self.ruta_detallada) - 1:
                                # Hemos llegado al último nodo
                                self.esta_llegado = True
                            else:
                                self.indice_destino += 1
                    else:
                        # Si no hay posición actual, asignar la primera posición de la ruta
                        self.posicion_actual = self.ruta_detallada[0]
                        self.indice_destino = 1  # Inicializar indice_destino a 1
                    print(f"Velocidad actual del vehículo {self.id}: {self.velocidad}")
   
    def establecer_contenedores_permitidos(self):
        if self.tipo == "camioneta":
            return ["Tipo1", "Tipo2"]  # Ejemplo de contenedores permitidos para camioneta
        elif self.tipo == "blindado":
            return ["Tipo3", "Tipo4"]  # Ejemplo de contenedores permitidos para vehículo blindado
        else:
            raise ValueError("Tipo de vehículo no válido")
        
    def puede_llevar_contenedor(self, tipo_contenedor):
        return tipo_contenedor in self.contenedores_permitidos

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

class Ladrones:
        def __init__(self, id, velocidad, capacidad, escudo, ataque, escoltas_necesarias):
            self.id = id
            self.velocidad = velocidad
            self.capacidad = capacidad
            self.escudo = escudo
            self.ataque = ataque
            self.escoltas_necesarias = escoltas_necesarias