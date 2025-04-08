import json
import networkx as nx
from pyvis.network import Network

# Leer el JSON
with open("Romania.json", "r") as archivo:
    data = json.load(archivo)

# Crear el grafo con networkx
G = nx.Graph()

for nodo in data["nodes"]:
    G.add_node(nodo["id"], color=nodo["color"])

for enlace in data["links"]:
    G.add_edge(enlace["source"], enlace["target"], weight=enlace["cost"])

# Crear la red de PyVis
net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")

# Convertir el grafo de networkx a pyvis
net.from_nx(G)

# Mostrar pesos en las aristas
for edge in net.edges:
    source = edge['from']
    target = edge['to']
    costo = G[source][target]['width']
    edge['title'] = f"Costo: {costo}"
    edge['label'] = str(costo)
    edge['width'] = 2

# Guardar y abrir en navegador

net.show_buttons()
net.show("grafo_interactivo.html", notebook=False)