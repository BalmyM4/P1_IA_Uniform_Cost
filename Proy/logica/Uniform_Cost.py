import heapq
import networkx as nx

# Para mostrar el paso a paso
def paso_paso_str( nivel: int, frontera: list, paso_paso: str, nodo_actual: str ):
    
    # Agregando el nivel
    paso_paso += f"{nivel}"
    
    # Agregando la información de la frontera
    for tupla in enumerate(frontera):
        
        # Para el menor costo acumulado
        if tupla[0] == 0:
            # Parceando el camino
            camino_str = [nodo[:3] for nodo in tupla[1][2]]
            camino_str = " -> ".join(camino_str)
            
            paso_paso += f"\t\t{tupla[1][0]}"
            
            if nodo_actual is not None:
                paso_paso += f"\t\t{nodo_actual[:3]}"
            else:
                paso_paso += "\t\t"
            
            paso_paso += f"\t\t\t{camino_str} «\n"
        
        # Para los demás nodos
        else:
            # Parceando el camino
            camino_str = [nodo[:3] for nodo in tupla[1][2]]
            camino_str = " -> ".join(camino_str)
            
            paso_paso += f"\t\t{tupla[1][0]}"
            
            paso_paso += "\t\t"
                
            paso_paso += f"\t\t\t{camino_str}\n"
    
    paso_paso += "\n"
        
    return paso_paso
    
# Algoritmo de Uniform Cost Search
def uniform_cost_search(grafo: nx.Graph, inicio: str, objetivo: str):
    
    # Cola de prioridad: (costo acumulado, nodo actual, camino recorrido)
    frontera = [(0, inicio, [inicio])]
    visitados = set()
    
    # Para mostrar el progreso paso a paso
    paso_paso = ""
    nivel = 0
    nodo_actual = None

    while frontera:
        
        paso_paso = paso_paso_str(nivel, frontera, paso_paso, nodo_actual)
        
        # Extraer el nodo con menor costo acumulado
        costo_actual, nodo_actual, camino = heapq.heappop(frontera)

        if nodo_actual == objetivo:
            return camino, costo_actual, paso_paso

        if nodo_actual in visitados:
            continue
        
        
        visitados.add(nodo_actual)

        for vecino in grafo.neighbors(nodo_actual):
            if vecino not in visitados:
                peso = grafo[nodo_actual][vecino]['weight']
                heapq.heappush(frontera, (costo_actual + peso, vecino, camino + [vecino]))
                
        nivel += 1

    return None, float('inf'), ""  # Si no se encuentra camino


