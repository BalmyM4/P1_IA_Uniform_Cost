import json
import networkx as nx

def crearGraph():
    
    # Leer el JSON
    with open("recursos\\Romania.json", "r") as archivo:
        data = json.load(archivo)

    # Crear el grafo con networkx
    G = nx.Graph()

    # Agregar nodos con atributos
    for nodo in data["nodes"]:
        G.add_node(nodo["id"])

    # Agregar aristas con peso
    for enlace in data["links"]:
        G.add_edge(enlace["source"], enlace["target"], weight=enlace["cost"])
        
    return G

if __name__ == "__main__":
    
    # Crear el grafo
    G = crearGraph()
    
    # Mostrar información del grafo
    print("Grafo creado con éxito:", G.nodes(data=True), G.edges(data=True))
