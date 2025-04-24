from PySide6 import QtWidgets
import pyqtgraph as pg
import networkx as nx
import numpy as np
import json


def crearGraph( G ):

    # Mapear nombres de nodos a índices numéricos
    node_list = list(G.nodes())
    node_index = {node: i for i, node in enumerate(node_list)}

    # Calcular layout (posiciones de los nodos)
    pos = nx.spring_layout(G, weight='weight', seed=42)
    node_positions = np.array([pos[node] for node in node_list])

    # Preparar aristas como índices numéricos
    edges = np.array([(node_index[u], node_index[v]) for u, v in G.edges()], dtype=int)

    # Configuración visual
    node_colors = [pg.mkColor(0, 122, 255) for _ in node_list]  # azul brillante
    node_sizes = np.array([10 + 2 * G.degree(node) for node in node_list])

    # Pesos de las aristas
    edge_weights = [G.edges[edge]['weight'] for edge in G.edges()]
    max_weight = max(edge_weights)
    edge_widths = np.array([3 * (w/max_weight) for w in edge_weights])

    # Crear y configurar el grafo
    graph_item = pg.GraphItem()

    graph_item.setData(
        pos=node_positions,
        adj=edges,
        size=node_sizes,
        symbol='o',
        pxMode=True,
        brush=node_colors,
        pen={'color': 'w', 'width': 1},
        width=edge_widths,
        symbolPen='w'
    )

    # Añadir etiquetas a los nodos
    labels = []
    for node, (x, y) in zip(node_list, node_positions):
        label = pg.TextItem(
            text=node,
            color=(160, 244, 255),  # Texto blanco
            fill=(0, 0, 0, 150)     # Fondo negro semitransparente
        )
        labels.append(label)
        label.setPos(x + 0.01, y)

    # Mostrar pesos en las aristas
    texts = []
    for (u, v), weight in zip(G.edges(), edge_weights):
        x = (pos[u][0] + pos[v][0]) / 2
        y = (pos[u][1] + pos[v][1]) / 2
        text = pg.TextItem(
            text=f"{weight}",
            color=(255, 255, 255),  # Texto amarillo claro
            fill=(0, 0, 0, 150),    # Mismo fondo semitransparente
            anchor=(0.5, 0.5)      # Centrado
        )
        labels.append(text)
        text.setPos(x, y)
        
    return graph_item, labels, texts, node_positions, edges, node_sizes, node_colors, edge_widths