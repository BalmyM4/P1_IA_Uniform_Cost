import json
import networkx as nx
import matplotlib.pyplot as plt

# Leer el archivo JSON
with open("Romania.json", "r") as archivo:
    data = json.load(archivo)

# Crear el grafo (no dirigido)
G = nx.Graph()

# Agregar nodos con atributos (como 'color', aunque networkx no lo usa por default)
for nodo in data["nodes"]:
    G.add_node(nodo["id"], color=nodo["color"])

# Agregar aristas con peso (cost)
for enlace in data["links"]:
    G.add_edge(enlace["source"], enlace["target"], weight=enlace["cost"])

# Dibujar el grafo
pos = nx.spring_layout(G, seed=42)  # Posiciones de los nodos
labels = nx.get_edge_attributes(G, 'weight')

plt.figure(figsize=(12, 8))
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1000, font_size=10)
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.title("Grafo cargado desde JSON")
plt.axis("off")
plt.show()
