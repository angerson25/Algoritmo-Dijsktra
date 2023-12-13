##Se recibe un archivo de texto en el que se reciben las solicitudes de manejo de 5 documentos en donde se define el destino final de los mismos, la identificación y el nombre del solicitante, el vertice A es la oficina que recibe los documentos, determinar 

#1 cargas solicitudes
#opcion 2 calcular total de dias requeridos para todos los documentos
#3 generar estadistica de documentos requeridos por oficina
#4 numero de estadistica de numero de solicitudes por usuario 
#5 salir

import matplotlib.pyplot as plt
import networkx as nx
from itertools import permutations
import heapq
import json

def dijkstra(graph, inicio, destino):
    distancias = {nodo: float('inf') for nodo in graph}
    distancias[inicio] = 0
    cola_prioridad = [(0, inicio)]

    while cola_prioridad:
        distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)

        if nodo_actual == destino:
            # Hemos llegado al nodo de destino, devolvemos el camino óptimo
            camino = [nodo_actual]
            while nodo_actual != inicio:
                nodo_actual = nodos_anteriores[nodo_actual]
                camino.insert(0, nodo_actual)
            return camino

        for vecino, datos_arista in graph[nodo_actual].items():
            peso = datos_arista['weight']
            distancia = distancia_actual + peso

            if distancia < distancias[vecino]:
                distancias[vecino] = distancia
                nodos_anteriores[vecino] = nodo_actual
                heapq.heappush(cola_prioridad, (distancia, vecino))

    # No se encontró un camino al nodo de destino
    return None


##CAMINO OPTIMO
def calcular_suma_aristas(graph, camino):
    suma_aristas = 0

    for i in range(len(camino) - 1):
        nodo_actual = camino[i]
        nodo_siguiente = camino[i + 1]

        peso = graph[nodo_actual][nodo_siguiente]['weight']
        suma_aristas += peso

    return suma_aristas


# Crear un grafo ponderado
G = nx.Graph()

# Añadir nodos
nodes = ["A", "B", "C", "D", "E","F","G","H"]
G.add_nodes_from(nodes)

# Añadir aristas con pesos
edges_with_weights = [
    ("A", "C", 1),
    ("A", "B", 3),
    ("B", "G", 5),
    ("B", "D", 1),
    ("G", "E", 2),
    ("C", "D", 2),
    ("D", "F", 2),
    ("C", "F", 5),
    ("F", "H", 3),
    ("D", "E", 4),
    ("E","H",1)
]
G.add_weighted_edges_from(edges_with_weights)

# Especificar posiciones personalizadas para cada nodo
custom_positions = {"A": (0.112, 0.667), "B": (0.457, 0.457), "C": (1.2, 0.7), "D": (1.512, 0.457), "E": (1.7, 0.2), "F": (2, 0.7), "G": (0.10, 0.2), "H": (2.5, 0.5)}




# Dibujar el grafo con posiciones personalizadas
nx.draw(G, pos=custom_positions, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_color="black", font_weight="bold", arrowsize=20)
nx.draw_networkx_edge_labels(G, pos=custom_positions, edge_labels=nx.get_edge_attributes(G, 'weight'))

# Mostrar el grafo
plt.show()

# Mostrar el menú
print("\nMenú:\n1. Cargar solicitudes\n2. Calcular total de dias requeridos para todos los documentos\n3. Generar estadistica de documentos requeridos por oficina\n4. Numero de estadistica de numero de solicitudes por usuario\n5. Salir")


# Leer la opción del usuario
opcion = input("Ingrese una opción: ")

# Opción 1: Cargar solicitudes
if opcion == "1":

    # Leer los datos desde el archivo JSON
    with open("solicitudes.json", 'r') as archivo_json:
        solicitudes = json.load(archivo_json)
            
    print("\nSolicitudes cargadas con éxito.")
    
    ##crear archivos de texto con los datos de las solicitudes por usuario
    for diccionario in solicitudes:
        for key in diccionario:
            usuaritemp = diccionario[key]
            for value in usuaritemp:
                conta=0
                usuario = usuaritemp[value]
                for diccionario in solicitudes:
                    for key in diccionario:
                        usuaritemp = diccionario[key]
                        for value in usuaritemp:
                            if usuaritemp[value] == usuario:
                                conta=conta+1
                with open("A"+str(usuario)+".txt", "w") as archivo:
                    archivo.write("\nIdentificacion: "+str(usuario)+"\nNumero de envios: "+str(conta))
                    archivo.close()
                    
    
    print("\nMenú:\n1. Cargar solicitudes\n2. Calcular total de dias requeridos para todos los documentos\n3. Generar estadistica de documentos requeridos por oficina\n4. Numero de estadistica de numero de solicitudes por usuario\n5. Salir")
    opcion = input("Ingrese una opción: ")
    

if opcion == "2":
    acum = 0
    # Mostrar los datos importados
    for item in solicitudes:
        for key in item:
            ##aplicar algoritmo de dijkstra desde A hasta la key
            nodos_anteriores = {}
            camino_optimo = dijkstra(G, "A", key)
            if camino_optimo:
                print(f"Camino óptimo desde A hasta {key}: {camino_optimo}")
                suma_aristas_camino = calcular_suma_aristas(G, camino_optimo)
                acum = acum + suma_aristas_camino
            else:
                print(f"No hay un camino desde A hasta {key}.")
                
            
        
    print("\nEl total de dias requeridos para todos los documentos es: ",acum)
    print("\nMenú:\n1. Cargar solicitudes\n2. Calcular total de dias requeridos para todos los documentos\n3. Generar estadistica de documentos requeridos por oficina\n4. Numero de estadistica de numero de solicitudes por usuario\n5. Salir")
    opcion = input("Ingrese una opción: ")
    
if opcion == "3":
    oficina = input("Ingrese la oficina a buscar: ")
    # Verificar si el valor ingresado está presente en las claves del JSON
    valor_en_claves = any(oficina in diccionario for diccionario in solicitudes)
    cont=0
    
    if valor_en_claves:
        print("Oficina encontrada.")
        # Mostrar los datos importados
        for item in solicitudes:
            for key in item:
                if key == oficina:
                    cont=cont+1

        soliporoficina = {}
        soliporoficina[oficina] = cont
        print(soliporoficina)       
                    

    else:
        print("Oficina no encontrada.")
        
if opcion == "4":
    usuario = int(input("Ingrese el usuario a buscar: "))
    contu=0
    #Verificar si el valor ingresado está presente en los valores del JSON
    for diccionario in solicitudes:
        for key in diccionario:
            usuaritemp = diccionario[key]
            for value in usuaritemp:
                
                if usuaritemp[value] == usuario:
                    print("Usuario encontrado.")
                    contu=contu+1
            
    if contu == 0:
        print("Usuario no encontrado.")
        
    else:
        print("\nEl usuario tiene ",contu," solicitudes.")
        
                    
if opcion == "5":
    print("'Gracias por usar el programa.")

    
else:
    print("Opción no válida. Intente de nuevo.")