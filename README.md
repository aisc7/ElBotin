# ElBotin
<!-- rutas.py
Resumen del Código
Lectura del CSV de Solicitudes:
El método procesar_solicitudes lee un archivo CSV que contiene las solicitudes de los clientes. Este archivo tiene las columnas Nombre, Dinero_a_enviar, Destino, y Tiempo_estimado.
Interpretación de la Dirección del Cliente:
Si el valor en la columna Destino es "Dirección del Cliente", se traduce automáticamente como una ruta de 'A' a 'K'.
Selección del Vehículo:
Según la cantidad de dinero que el cliente desea enviar, se selecciona un vehículo:
Si el dinero es menor o igual a 500, se selecciona una camioneta.
Si el dinero es mayor a 500, se selecciona un vehículo blindado.
Planificación de la Ruta:
Se implementan varios algoritmos de planificación de rutas:
BFS (Búsqueda en Anchura)
DFS (Búsqueda en Profundidad)
Dijkstra
Bellman-Ford
Cada algoritmo busca la mejor ruta desde el origen 'A' hasta el destino especificado.
Se selecciona la mejor ruta de todas las rutas posibles (la que tenga el menor costo dentro del tiempo estimado).
Resultados:
Si se encuentra una ruta dentro del tiempo estimado, se guarda la información de la ruta y el costo.
Si no se encuentra una ruta viable, se indica que no es posible llegar en el tiempo estimado.
Escritura del CSV de Resultados:
Los resultados de la planificación de rutas se escriben en un archivo CSV de salida, con las siguientes columnas:
nombre_cliente: Nombre del cliente.
origen: Origen de la ruta (siempre 'A').
destino: Destino de la ruta.
cantidad_dinero: Cantidad de dinero a enviar.
vehiculo: Tipo de vehículo seleccionado.
ruta: Secuencia de nodos que componen la ruta.
costo: Costo de la ruta en términos de la cantidad de nodos. -->