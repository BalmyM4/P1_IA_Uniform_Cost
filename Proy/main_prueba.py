import logica.Graph as Graph
import logica.Uniform_Cost as Uniform_Cost
from logica.printPP import printPP
from test.printGraph import printGraph
from test.printGraph import printColorGraph
from test.printGraph import pyvisGraph


# Crear el grafo
grafo = Graph.crearGraph()


# Definir los nodos de inicio y objetivo
inicio = "Hirsova"
objetivo = "Pitesti"

# Uniform Cost Search
camino, costo, paso_paso = Uniform_Cost.uniform_cost_search(grafo, inicio, objetivo)

# Crear el grafo para PyVis
net = pyvisGraph(grafo)

# Mostrar el grafo
printGraph(net)

# Mostrar el resultado
printPP(camino, costo, paso_paso)

# Mostrar el grafo con la ruta remarcada
printColorGraph(net, camino)
