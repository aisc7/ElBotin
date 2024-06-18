# ElBotin
<!--  Explicacion de clase una por una 
 src/Botin.py 
 CentroDeOperacion:
Esta clase representa un centro de operaciones que maneja dinero, vehículos y escoltas.

Atributos:
id: Identificador del centro.
capacidad_dinero: Capacidad máxima de dinero que puede almacenar (por defecto 10000).
capacidad_vehiculos: Capacidad máxima de vehículos que puede tener (por defecto 7).
capacidad_escoltas: Capacidad máxima de escoltas que puede tener (por defecto 10).
dinero: Dinero almacenado actualmente (inicialmente 0).
vehiculos: Lista de vehículos en el centro (inicialmente vacía).
escoltas: Lista de escoltas en el centro (inicialmente vacía).
Métodos:
agregar_vehiculo(vehiculo): Agrega un vehículo a la lista si no se ha alcanzado la capacidad máxima.
agregar_escolta(escolta): Agrega un escolta a la lista si no se ha alcanzado la capacidad máxima.
almacenar_dinero(cantidad): Almacena una cantidad de dinero si no se excede la capacidad máxima; de lo contrario, lanza una excepción.
Cliente:
Esta clase representa un cliente que interactúa con el sistema.

Atributos:
id: Identificador del cliente.
dinero: Dinero que tiene el cliente (inicialmente 0).
Vehiculo:
Esta clase representa un vehículo con varias características.

Atributos:

id: Identificador del vehículo.
tipo: Tipo de vehículo (ej. "camioneta", "blindado").
velocidad: Velocidad del vehículo.
capacidad: Capacidad de carga del vehículo.
escudo: Nivel de protección del vehículo.
ataque: Capacidad ofensiva del vehículo.
escoltas_necesarias: Número de escoltas necesarios para el vehículo.
ruta_imagen: Ruta de la imagen del vehículo (opcional).
contenedores_permitidos: Tipos de contenedores que el vehículo puede llevar, determinado por el método establecer_contenedores_permitidos.
Métodos:

establecer_contenedores_permitidos(): Determina los tipos de contenedores permitidos según el tipo de vehículo.
puede_llevar_contenedor(tipo_contenedor): Verifica si el vehículo puede llevar un contenedor de un tipo específico.
Escolta:
Esta clase representa un escolta con capacidades defensivas y ofensivas.

Atributos:
id: Identificador del escolta.
escudo: Nivel de protección del escolta.
ataque: Capacidad ofensiva del escolta.
Contenedor:
Esta clase representa un contenedor con una capacidad de peso específica según su tipo.

Atributos:

id: Identificador del contenedor.
tipo_contenedor: Tipo de contenedor (ej. "pequeno", "mediano", "grande", "doble").
capacidad_peso: Capacidad máxima de peso del contenedor, determinada por el método establecer_capacidad_peso.
Métodos:

establecer_capacidad_peso(): Determina la capacidad de peso del contenedor según su tipo.
Puente:
Esta clase representa un puente que puede colapsar si se excede su peso máximo soportado.

Atributos:

id: Identificador del puente.
peso_maximo: Peso máximo que el puente puede soportar.
colapsado: Estado del puente, indicando si ha colapsado (inicialmente False).
Métodos:

puede_cruzar(peso_vehiculo): Verifica si un vehículo puede cruzar el puente sin exceder el peso máximo.
colapsar(): Marca el puente como colapsado.
Ladrones:
Esta clase representa a los ladrones con diversas características.

Atributos:
id: Identificador del ladrón.
velocidad: Velocidad del ladrón.
capacidad: Capacidad de carga del ladrón.
escudo: Nivel de protección del ladrón.
ataque: Capacidad ofensiva del ladrón.
escoltas_necesarias: Número de escoltas necesarios para el ladrón.

src/Rutas.py 
Rutas:
Esta clase está diseñada para planificar rutas en una ciudad utilizando diferentes algoritmos de búsqueda y determinar si los ladrones pueden interceptar un vehículo.

Atributos:
ciudad: Instancia de la clase Ciudad de view.Ciudad. Se inicializa y se configura con Pygame.
Métodos:
__init__():

Inicializa la instancia de Rutas y configura la ciudad con Pygame.
planificar_ruta_bfs(origen, destino, vehiculo_seleccionado, tiempo_estimado):

Implementa el algoritmo de búsqueda en anchura (BFS) para planificar una ruta.
Devuelve el costo de la ruta y el camino si el costo está dentro del tiempo estimado, de lo contrario, devuelve infinito y una lista vacía.
planificar_ruta_dfs(origen, destino, vehiculo_seleccionado, tiempo_estimado):

Implementa el algoritmo de búsqueda en profundidad (DFS) para planificar una ruta.
Devuelve el costo de la ruta y el camino si el costo está dentro del tiempo estimado, de lo contrario, devuelve infinito y una lista vacía.
planificar_ruta_dijkstra(origen, destino, vehiculo_seleccionado, tiempo_estimado):

Implementa el algoritmo de Dijkstra para encontrar la ruta más corta en términos de peso.
Devuelve el costo de la ruta y el camino si el costo está dentro del tiempo estimado, de lo contrario, devuelve infinito y una lista vacía.
planificar_ruta_bellman_ford(origen, destino, vehiculo_seleccionado, tiempo_estimado):

Implementa el algoritmo de Bellman-Ford para encontrar la ruta más corta, incluso en grafos con aristas de peso negativo.
Devuelve el costo de la ruta y el camino si el costo está dentro del tiempo estimado, de lo contrario, devuelve infinito y una lista vacía.
puente_dispo(nodo_actual, vecino, vehiculo_seleccionado):

Verifica si el vehículo puede cruzar un puente entre dos nodos, considerando el peso máximo que puede soportar el puente.
Devuelve True si el puente puede soportar el peso del vehículo, de lo contrario, False.
planificar_ruta(nombre, destino, dinero_a_enviar, tiempo_estimado):

Asigna un vehículo basado en la cantidad de dinero a enviar.
Planifica las rutas utilizando BFS, DFS, Dijkstra y Bellman-Ford.
Devuelve la mejor ruta dentro del tiempo estimado o indica que no se puede llegar al destino a tiempo.
planificar_ruta_con_paradas(metodo_planificacion, destinos, vehiculo_seleccionado, tiempo_estimado):

Planifica una ruta con múltiples paradas utilizando el método de planificación proporcionado.
Devuelve el costo total y el camino completo si el costo está dentro del tiempo estimado, de lo contrario, devuelve infinito y una lista vacía.
asignar_vehiculo(dinero_a_enviar):

Asigna un vehículo basado en la cantidad de dinero a enviar.
Devuelve una instancia de Vehiculo adecuada para transportar el dinero.
calcular_costo(camino):

Calcula el costo total de una ruta sumando los pesos de las aristas entre los nodos.
Devuelve el costo total de la ruta.
construir_camino(padre, origen, destino):

Construye un camino desde el origen al destino utilizando un diccionario de padres que almacena las rutas.
Devuelve la lista de nodos en el camino.
ladrones(cliente, vehiculo_asignado, mejor_ruta_cliente, dinero_a_enviar, tiempo_estimado, ataque_ladrones, escudo_ladrones):

Verifica si los ladrones pueden interceptar el vehículo asignado.
Devuelve un mensaje indicando si el ataque fue exitoso o no.
obtener_informacion_banda(ataque, escudo):

Devuelve una cadena con la información del ataque y el escudo de los ladrones.

view/Ciudad.py 
La clase Ciudad en el archivo view/Ciudad.py gestiona una ciudad virtual utilizando pygame para renderizar gráficos y networkx para manejar un grafo que representa la ciudad y sus conexiones. A continuación se presenta una explicación detallada de sus componentes y funciones:

Atributos de la Clase
background: Imagen de fondo de la ciudad.
vehiculos: Diccionario que almacena los vehículos presentes en la ciudad.
imagenes_vehiculos: Diccionario con las imágenes de los vehículos.
imagenes_personajes: Diccionario con las imágenes de los personajes.
ciudad: Grafo dirigido (DiGraph) que representa la estructura de la ciudad.
pygame_running: Booleano que indica si pygame está en ejecución.
render_thread: Hilo de renderizado para actualizar la visualización de la ciudad.
posiciones_nodos: Diccionario con las posiciones de los nodos en el grafo.
caminos_detallados: Diccionario con los caminos detallados entre nodos.
Métodos Principales
__init__(self)
Inicializa los atributos y carga las imágenes.

cargar_imagenes(self)
Carga las imágenes de los vehículos y personajes desde las rutas especificadas en rutas_imagenes.

iniciar_pygame(self)
Inicia pygame si no está ya corriendo y crea el grafo de la ciudad. Además, inicia el hilo de renderizado (RenderThread).

crear_grafo(self)
Construye el grafo de la ciudad:

Define las capacidades de los vehículos.
Crea instancias de puentes con diferentes capacidades.
Asigna posiciones a los nodos.
Establece caminos detallados entre los nodos.
Agrega nodos y aristas al grafo self.ciudad.
procesar_solicitudes(self, nombre, dinero_a_enviar, destino, tiempo_estimado)
Procesa las solicitudes para planificar rutas:

Selecciona el vehículo adecuado.
Planifica la mejor ruta usando uno de los algoritmos definidos.
Verifica y agrega el vehículo a la ciudad si no está registrado.
Asigna la ruta detallada al vehículo y actualiza la pantalla.
dibujar(self, screen)
Dibuja la ciudad, los nodos, las aristas, los vehículos y sus rutas detalladas en la pantalla pygame.

verificar_y_agregar_vehiculo(self, vehiculo)
Verifica si el vehículo ya está registrado en la ciudad y lo agrega si no lo está.

stop_pygame(self)
Detiene pygame y el hilo de renderizado.

src/Render_tread.py
La clase RenderThread en el archivo render.py maneja el renderizado gráfico en una hebra separada usando PySide6.QtCore.QThread y pygame. A continuación, se presenta una explicación detallada de sus componentes y funcionamiento:

Importaciones
pygame: Biblioteca para la creación de videojuegos y gráficos en tiempo real.
QThread y Signal de PySide6.QtCore: Para manejar la ejecución en hebras y señales en una aplicación Qt.
Atributos de la Clase
finished_signal: Señal emitida cuando el hilo de renderizado termina su ejecución.
ciudad: Instancia de la clase Ciudad que contiene los datos y métodos necesarios para renderizar la ciudad.
nodos_ruta_actual: Lista de nodos de la ruta actual (no se usa en el código proporcionado).
running: Booleano que indica si el hilo de renderizado está activo.
Métodos Principales
__init__(self, ciudad, parent=None)
Constructor que inicializa la instancia del hilo de renderizado.

ciudad: Instancia de la clase Ciudad.
parent: Objeto padre, opcional.
run(self)
Método principal que se ejecuta cuando se inicia el hilo.

Inicializa pygame y configura la pantalla.
Carga la imagen de fondo de la ciudad.
Entra en un bucle donde maneja eventos de pygame, dibuja la ciudad y actualiza la pantalla.
Si se recibe un evento QUIT, se detiene el bucle.
Al finalizar, emite la señal finished_signal.
stop(self)
Método para detener el hilo de renderizado.

Cambia self.running a False para salir del bucle de renderizado.
Llama a pygame.quit() para cerrar pygame.
Espera a que el hilo termine su ejecución con self.wait().

view/View.py
El archivo View.py implementa una interfaz gráfica para una aplicación de simulación de rutas. Usa PySide6 para la interfaz y pygame para la simulación gráfica. Aquí hay una explicación detallada de las clases y métodos del archivo:

Importaciones
Bibliotecas estándar: os, csv.
pygame: Para la simulación gráfica.
PySide6: Para la interfaz gráfica.
Clases personalizadas: Rutas y Ciudad.
Clases y Métodos
HomePageWidget
Un QWidget que muestra una imagen de fondo en la página de inicio.

init_ui: Carga y establece la imagen de fondo del widget. Si no se puede cargar la imagen, imprime un mensaje de error.
RegistroWidget
Un QWidget que permite al usuario registrar información de rutas.

init_ui: Configura la interfaz con varios QLabel, QLineEdit, QComboBox, QListWidget, y QPushButton para ingresar datos de ruta.
toggle_lista_destinos: Muestra u oculta la lista de destinos adicionales según la selección del destino.
on_guardar: Guarda la información ingresada en un archivo CSV y muestra un mensaje de confirmación o error.
BandaDialog
Un QDialog para configurar las propiedades de una banda.

init_ui: Configura la interfaz con QComboBox para seleccionar cliente, ataque y escudo.
get_values: Retorna los valores seleccionados.
obtener_clientes_del_csv: Carga los nombres de los clientes desde un archivo CSV.
SimulacionDialogoWidget
Un QWidget para manejar la simulación de rutas y la configuración de bandas.

init_ui: Configura la interfaz con botones para generar rutas y simular bandas.
showEvent: Carga los datos de clientes cada vez que se muestra la pestaña.
simular_pygame: Inicia la simulación gráfica con pygame.
simular_banda: Abre el diálogo de configuración de bandas, obtiene datos del cliente y ejecuta la simulación.
generar_ruta: Permite seleccionar un cliente y planificar la mejor ruta usando la clase Rutas.
cargar_datos_clientes: Carga datos de clientes desde un archivo CSV en un diccionario.
obtener_clientes_del_csv: Retorna una lista de nombres de clientes.
obtener_datos_cliente: Obtiene los datos de un cliente específico del diccionario.
MainWindow
La ventana principal de la aplicación.

init_ui: Configura la interfaz principal con un QTabWidget que contiene las pestañas de inicio, registro y simulación.
apply_styles: Aplica estilos personalizados a los widgets.
closeEvent: Maneja el cierre de la ventana principal, asegurando que el hilo de renderizado de pygame se cierre adecuadamente.
mostrar_dialogo_simulaciones: Muestra la pestaña de simulación.
mostrar_formulario: Muestra la pestaña de registro. -->