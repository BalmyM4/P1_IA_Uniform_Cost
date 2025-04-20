from pyvis.network import Network
import networkx as nx

def pyvisGraph(graph: nx.Graph):
    # Crear la red de PyVis
    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")

    # Convertir el grafo de networkx a pyvis
    net.from_nx(graph)

    # Mostrar pesos en las aristas
    for edge in net.edges:
        source = edge['from']
        target = edge['to']
        edge['title'] = f"Costo: {graph[source][target]['width']}"
        edge['label'] = str(graph[source][target]['width'])
        edge['width'] = 2  # Grosor uniforme
    
    return net


def printGraph(net: Network):

    # Guardar y abrir en navegador
    net.show("grafo.html", notebook=False)

def printColorGraph(net: Network, ruta: list):

    # Mostrar pesos en las aristas
    for edge in net.edges:
        
        source = edge['from']
        target = edge['to']
        
        if ruta is not None:
            # Si la arista está en la ruta, cambiar el color a rojo
            if (source, target) in zip(ruta, ruta[1:]):
                edge['color'] = 'red'  # Color rojo para las aristas en la ruta
            elif (target, source) in zip(ruta, ruta[1:]):
                edge['color'] = 'red'  # También considerar el caso inverso (para rutas bidireccionales)
            else:
                edge['color'] = '#97c2fc'

    if ruta is not None:
        for node in net.nodes:
            if node['id'] in ruta:
                node['color'] = 'red'  # Color amarillo para los nodos en la ruta

    
    # Guardar y abrir en navegador
    net.show("grafo_coloreado.html", notebook=False)